"""
Smart Defaults System - Learn user patterns and pre-fill forms
Research shows: Simplified workflows create lasting wow experiences
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sqlite3

class SmartDefaultsEngine:
    """Learn from user behavior to predict and pre-fill audit fields"""
    
    def __init__(self):
        self.db_path = "user_patterns.db"
        self._init_database()
    
    def _init_database(self):
        """Initialize pattern storage database"""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS audit_patterns (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                location_type TEXT,
                time_of_day INTEGER,
                day_of_week INTEGER,
                field_name TEXT,
                field_value TEXT,
                frequency INTEGER DEFAULT 1,
                last_used TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def learn_pattern(self, user_id: str, location_context: Dict, audit_data: Dict):
        """Learn from completed audit to predict future defaults"""
        conn = sqlite3.connect(self.db_path)
        now = datetime.now()
        
        for field_name, field_value in audit_data.items():
            # Skip empty or invalid values
            if not field_value or field_value in ['', 'null', None]:
                continue
            
            # Extract context
            location_type = location_context.get('type', 'general')
            time_of_day = now.hour
            day_of_week = now.weekday()
            
            # Check if pattern exists
            existing = conn.execute('''
                SELECT frequency FROM audit_patterns 
                WHERE user_id = ? AND location_type = ? AND field_name = ? 
                AND field_value = ? AND time_of_day BETWEEN ? AND ?
            ''', (user_id, location_type, field_name, field_value, time_of_day-1, time_of_day+1)).fetchone()
            
            if existing:
                # Increment frequency
                conn.execute('''
                    UPDATE audit_patterns 
                    SET frequency = frequency + 1, last_used = ? 
                    WHERE user_id = ? AND location_type = ? AND field_name = ? AND field_value = ?
                ''', (now, user_id, location_type, field_name, field_value))
            else:
                # Create new pattern
                conn.execute('''
                    INSERT INTO audit_patterns 
                    (user_id, location_type, time_of_day, day_of_week, field_name, field_value, last_used)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (user_id, location_type, time_of_day, day_of_week, field_name, field_value, now))
        
        conn.commit()
        conn.close()
    
    def get_smart_defaults(self, user_id: str, location_context: Dict) -> Dict:
        """Get predicted defaults based on learned patterns"""
        conn = sqlite3.connect(self.db_path)
        now = datetime.now()
        
        location_type = location_context.get('type', 'general')
        time_of_day = now.hour
        day_of_week = now.weekday()
        
        # Get most frequent patterns for current context
        patterns = conn.execute('''
            SELECT field_name, field_value, frequency, 
                   ABS(time_of_day - ?) as time_diff,
                   ABS(day_of_week - ?) as day_diff
            FROM audit_patterns 
            WHERE user_id = ? AND location_type = ?
            ORDER BY frequency DESC, time_diff ASC, day_diff ASC
        ''', (time_of_day, day_of_week, user_id, location_type)).fetchall()
        
        conn.close()
        
        # Build defaults dictionary (most frequent value per field)
        defaults = {}
        for field_name, field_value, frequency, time_diff, day_diff in patterns:
            if field_name not in defaults:
                # Only suggest if pattern has been used multiple times
                if frequency >= 2:
                    defaults[field_name] = {
                        'value': field_value,
                        'confidence': min(frequency / 10.0, 1.0),  # Max confidence of 1.0
                        'context': f"Used {frequency} times in similar conditions"
                    }
        
        return defaults
    
    def get_predictive_suggestions(self, user_id: str, current_field: str, partial_value: str = "") -> List[Dict]:
        """Get real-time suggestions as user types"""
        conn = sqlite3.connect(self.db_path)
        
        suggestions = conn.execute('''
            SELECT field_value, frequency, COUNT(*) as usage_count
            FROM audit_patterns 
            WHERE user_id = ? AND field_name = ? AND field_value LIKE ?
            GROUP BY field_value
            ORDER BY frequency DESC, usage_count DESC
            LIMIT 5
        ''', (user_id, current_field, f"{partial_value}%")).fetchall()
        
        conn.close()
        
        return [
            {
                'value': value,
                'confidence': min(frequency / 10.0, 1.0),
                'usage_count': usage_count
            }
            for value, frequency, usage_count in suggestions
        ]
