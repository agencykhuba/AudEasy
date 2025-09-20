import requests
import time
import psycopg2
import os
import logging
from datetime import datetime

class HealthMonitor:
    def __init__(self):
        self.services = {
            'audeasy': 'https://audeasy.onrender.com/health',
            # Add other services as they're deployed
        }
    
    def get_db_connection(self):
        try:
            return psycopg2.connect(
                host=os.environ.get('DB_HOST', 'localhost'),
                database=os.environ.get('DB_NAME', 'audeasy_db'),
                user=os.environ.get('DB_USER', 'postgres'),
                password=os.environ.get('DB_PASSWORD', '')
            )
        except Exception as e:
            logging.error(f"Database connection failed: {e}")
            return None
    
    def check_service_health(self, vertical_id, service_url):
        """Check health of a single service"""
        try:
            start_time = time.time()
            response = requests.get(service_url, timeout=10)
            response_time = int((time.time() - start_time) * 1000)
            
            return {
                'vertical_id': vertical_id,
                'status_code': response.status_code,
                'response_time_ms': response_time,
                'error_message': None if response.status_code == 200 else f"HTTP {response.status_code}"
            }
        except Exception as e:
            return {
                'vertical_id': vertical_id,
                'status_code': 0,
                'response_time_ms': 0,
                'error_message': str(e)
            }
    
    def log_health_check(self, health_data):
        """Log health check results to database"""
        conn = self.get_db_connection()
        if not conn:
            return False
        
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO service_health (vertical_id, status_code, response_time_ms, error_message)
                VALUES (%s, %s, %s, %s)
            """, (
                health_data['vertical_id'],
                health_data['status_code'],
                health_data['response_time_ms'],
                health_data['error_message']
            ))
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Failed to log health check: {e}")
            return False
        finally:
            conn.close()
    
    def monitor_all_services(self):
        """Monitor all active services"""
        conn = self.get_db_connection()
        if not conn:
            return
        
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, name FROM verticals WHERE status = 'live'")
            active_verticals = cur.fetchall()
            
            for vertical_id, vertical_name in active_verticals:
                if vertical_name in self.services:
                    health_data = self.check_service_health(
                        vertical_id, 
                        self.services[vertical_name]
                    )
                    self.log_health_check(health_data)
                    
                    logging.info(f"Health check for {vertical_name}: "
                               f"Status {health_data['status_code']}, "
                               f"Response time {health_data['response_time_ms']}ms")
        
        except Exception as e:
            logging.error(f"Health monitoring error: {e}")
        finally:
            conn.close()

if __name__ == '__main__':
    monitor = HealthMonitor()
    monitor.monitor_all_services()
