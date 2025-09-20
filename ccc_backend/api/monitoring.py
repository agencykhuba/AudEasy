from flask import Blueprint, jsonify, request
import requests
import subprocess
import psycopg2
import os
import logging
import time
from datetime import datetime, timezone

monitoring_bp = Blueprint('monitoring', __name__)

class CCCMonitor:
    def __init__(self):
        self.render_api_key = os.environ.get('RENDER_API_KEY')
        self.service_id = os.environ.get('RENDER_SERVICE_ID') 
        self.base_url = "https://api.render.com/v1"
        self.audeasy_url = "https://audeasy.onrender.com"
    
    def check_service_health(self):
        """Check if all services are responding"""
        services = {
            "audeasy_main": f"{self.audeasy_url}/health",
            "audeasy_ccc": f"{self.audeasy_url}/api/health"
        }
        
        results = {}
        for service_name, url in services.items():
            try:
                start_time = time.time()
                response = requests.get(url, timeout=10)
                response_time = int((time.time() - start_time) * 1000)
                
                results[service_name] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "status_code": response.status_code,
                    "response_time_ms": response_time,
                    "last_check": datetime.now(timezone.utc).isoformat()
                }
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        results[service_name]["service_info"] = data
                    except:
                        results[service_name]["service_info"] = "Non-JSON response"
                        
            except Exception as e:
                results[service_name] = {
                    "status": "error",
                    "error": str(e),
                    "response_time_ms": 0,
                    "last_check": datetime.now(timezone.utc).isoformat()
                }
        
        return results
    
    def check_database_status(self):
        """Check database connectivity and CCC table status"""
        try:
            conn = psycopg2.connect(
                host=os.environ.get('DB_HOST', 'localhost'),
                database=os.environ.get('DB_NAME', 'audeasy_db'),
                user=os.environ.get('DB_USER', 'postgres'),
                password=os.environ.get('DB_PASSWORD', '')
            )
            cur = conn.cursor()
            
            # Check if CCC tables exist
            ccc_tables = ['verticals', 'projects', 'service_health', 'revenue_records', 'system_metrics']
            cur.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name = ANY(%s)
            """, (ccc_tables,))
            
            existing_tables = [row[0] for row in cur.fetchall()]
            missing_tables = [t for t in ccc_tables if t not in existing_tables]
            
            # Check table row counts
            table_counts = {}
            for table in existing_tables:
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                table_counts[table] = cur.fetchone()[0]
            
            # Test database performance
            start_time = time.time()
            cur.execute("SELECT 1")
            query_time = int((time.time() - start_time) * 1000)
            
            conn.close()
            
            return {
                "connected": True,
                "ccc_tables_ready": len(existing_tables),
                "missing_tables": missing_tables,
                "table_counts": table_counts,
                "query_performance_ms": query_time,
                "status": "healthy" if len(missing_tables) == 0 else "incomplete"
            }
            
        except Exception as e:
            return {
                "connected": False,
                "error": str(e),
                "status": "error"
            }
    
    def check_git_repository_status(self):
        """Check git repository status and recent commits"""
        try:
            # Get current branch and status
            branch_result = subprocess.run(['git', 'branch', '--show-current'], 
                                         capture_output=True, text=True, timeout=10)
            status_result = subprocess.run(['git', 'status', '--porcelain'], 
                                         capture_output=True, text=True, timeout=10)
            
            # Get recent commits
            log_result = subprocess.run(['git', 'log', '--oneline', '-5'], 
                                      capture_output=True, text=True, timeout=10)
            
            # Check if repo is ahead/behind remote
            remote_result = subprocess.run(['git', 'status', '-uno'], 
                                         capture_output=True, text=True, timeout=10)
            
            return {
                "current_branch": branch_result.stdout.strip(),
                "is_clean": len(status_result.stdout.strip()) == 0,
                "uncommitted_changes": status_result.stdout.strip().split('\n') if status_result.stdout.strip() else [],
                "recent_commits": log_result.stdout.strip().split('\n'),
                "remote_status": "up_to_date" if "up to date" in remote_result.stdout else "diverged",
                "status": "healthy"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def get_system_performance_metrics(self):
        """Get system performance metrics"""
        try:
            # Memory usage (approximate)
            import psutil
            
            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_usage_percent": psutil.disk_usage('/').percent,
                "status": "healthy"
            }
        except ImportError:
            # Fallback without psutil
            return {
                "status": "limited",
                "note": "Install psutil for detailed system metrics"
            }
        except Exception as e:
            return {
                "status": "error", 
                "error": str(e)
            }
    
    def get_render_deployment_status(self):
        """Get Render deployment status via API if configured"""
        if not self.render_api_key or not self.service_id:
            return {
                "status": "not_configured",
                "note": "Set RENDER_API_KEY and RENDER_SERVICE_ID for Render integration"
            }
        
        try:
            headers = {"Authorization": f"Bearer {self.render_api_key}"}
            
            # Get service info
            service_response = requests.get(f"{self.base_url}/services/{self.service_id}", 
                                          headers=headers, timeout=15)
            
            # Get recent deployments
            deploys_response = requests.get(f"{self.base_url}/services/{self.service_id}/deploys?limit=5", 
                                          headers=headers, timeout=15)
            
            return {
                "service_info": service_response.json() if service_response.status_code == 200 else None,
                "recent_deployments": deploys_response.json() if deploys_response.status_code == 200 else None,
                "status": "connected" if service_response.status_code == 200 else "error",
                "last_check": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

@monitoring_bp.route('/api/monitoring/dashboard', methods=['GET'])
def get_monitoring_dashboard():
    """Get comprehensive monitoring dashboard data"""
    monitor = CCCMonitor()
    
    # Collect all monitoring data
    dashboard_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "services": monitor.check_service_health(),
        "database": monitor.check_database_status(),
        "repository": monitor.check_git_repository_status(),
        "system": monitor.get_system_performance_metrics(),
        "render": monitor.get_render_deployment_status()
    }
    
    # Calculate overall health status
    service_health = all(s.get("status") == "healthy" for s in dashboard_data["services"].values())
    db_health = dashboard_data["database"]["status"] == "healthy"
    git_health = dashboard_data["repository"]["status"] == "healthy"
    
    overall_status = "healthy" if (service_health and db_health and git_health) else "degraded"
    
    dashboard_data["overall_status"] = overall_status
    dashboard_data["health_summary"] = {
        "services_healthy": service_health,
        "database_healthy": db_health,
        "repository_healthy": git_health,
        "last_update": datetime.now(timezone.utc).isoformat()
    }
    
    return jsonify(dashboard_data)

@monitoring_bp.route('/api/monitoring/trigger-deploy', methods=['POST'])
def trigger_deployment():
    """Trigger manual deployment via Render API"""
    monitor = CCCMonitor()
    
    if not monitor.render_api_key or not monitor.service_id:
        return jsonify({
            "success": False,
            "error": "Render API credentials not configured"
        }), 400
    
    try:
        headers = {"Authorization": f"Bearer {monitor.render_api_key}"}
        response = requests.post(f"{monitor.base_url}/services/{monitor.service_id}/deploys", 
                               headers=headers, timeout=30)
        
        return jsonify({
            "success": response.status_code in [200, 201],
            "deployment_id": response.json().get("id") if response.status_code in [200, 201] else None,
            "render_response": response.json(),
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 500

@monitoring_bp.route('/api/monitoring/health-check', methods=['GET'])
def quick_health_check():
    """Quick health check endpoint for external monitoring"""
    monitor = CCCMonitor()
    
    try:
        # Quick database check
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            database=os.environ.get('DB_NAME', 'audeasy_db'),
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASSWORD', ''),
            connect_timeout=5
        )
        conn.close()
        db_healthy = True
    except:
        db_healthy = False
    
    # Quick service check
    try:
        response = requests.get(f"{monitor.audeasy_url}/health", timeout=5)
        service_healthy = response.status_code == 200
    except:
        service_healthy = False
    
    overall_healthy = db_healthy and service_healthy
    
    return jsonify({
        "status": "healthy" if overall_healthy else "unhealthy",
        "database": db_healthy,
        "service": service_healthy,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200 if overall_healthy else 503
