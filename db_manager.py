"""
Database Manager for FileNinja Application

This module handles all database operations including:
- Database connection and initialization
- Creating tables for file logs
- CRUD operations for file movement records
- Query operations for the frontend
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import json
import os
from pathlib import Path


class DatabaseManager:
    """
    Manages SQLite database operations for FileNinja application.
    
    Handles connection management, table creation, and all CRUD operations
    for tracking file movements and maintaining application logs.
    """
    
    def __init__(self, database_path: str = "fileninja.db"):
        """Initialize database connection parameters."""
        self.database_path = database_path
        self.connection = None
        
    def connect(self) -> bool:
        """
        Establish connection to SQLite database.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Create database directory if it doesn't exist
            db_dir = Path(self.database_path).parent
            db_dir.mkdir(parents=True, exist_ok=True)
            
            self.connection = sqlite3.connect(
                self.database_path,
                check_same_thread=False,
                timeout=30.0
            )
            
            # Enable foreign keys and row factory for dict-like access
            self.connection.execute("PRAGMA foreign_keys = ON")
            self.connection.row_factory = sqlite3.Row
            
            print(f"✅ Connected to SQLite database: {self.database_path}")
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Error connecting to SQLite: {e}")
            return False
    
    def create_database_if_not_exists(self):
        """Create the FileNinja database if it doesn't exist."""
        # For SQLite, this is handled automatically by connect()
        print(f"✅ Database will be created automatically: {self.database_path}")
    
    def initialize_tables(self):
        """
        Create necessary tables for FileNinja application.
        
        Tables created:
        - file_logs: Main table for tracking file movements
        - app_settings: Configuration settings storage
        """
        if not self.connection:
            if not self.connect():
                return False
        
        try:
            cursor = self.connection.cursor()
            
            # File logs table
            create_file_logs_table = """
            CREATE TABLE IF NOT EXISTS file_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_name TEXT NOT NULL,
                new_path TEXT NOT NULL,
                file_type TEXT NOT NULL,
                file_size INTEGER,
                tags TEXT,
                moved_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            # App settings table
            create_settings_table = """
            CREATE TABLE IF NOT EXISTS app_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_key TEXT UNIQUE NOT NULL,
                setting_value TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            # Create indexes for better performance
            create_indexes = [
                "CREATE INDEX IF NOT EXISTS idx_moved_at ON file_logs(moved_at)",
                "CREATE INDEX IF NOT EXISTS idx_file_type ON file_logs(file_type)",
                "CREATE INDEX IF NOT EXISTS idx_original_name ON file_logs(original_name)",
                "CREATE INDEX IF NOT EXISTS idx_setting_key ON app_settings(setting_key)"
            ]
            
            cursor.execute(create_file_logs_table)
            cursor.execute(create_settings_table)
            
            for index_sql in create_indexes:
                cursor.execute(index_sql)
            
            self.connection.commit()
            cursor.close()
            
            print("✅ Database tables initialized successfully")
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Error creating tables: {e}")
            return False
    
    def log_file_movement(self, original_name: str, new_path: str, 
                         file_type: str, file_size: int, tags: List[str]) -> bool:
        """
        Log a file movement to the database.
        
        Args:
            original_name (str): Original filename
            new_path (str): New file path after organization
            file_type (str): Type of file (e.g., 'pdf', 'image', 'video')
            file_size (int): Size of file in bytes
            tags (List[str]): List of tags assigned to the file
            
        Returns:
            bool: True if logged successfully, False otherwise
        """
        if not self.connection:
            if not self.connect():
                return False
        
        try:
            cursor = self.connection.cursor()
            
            insert_query = """
            INSERT INTO file_logs (original_name, new_path, file_type, file_size, tags, moved_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            
            tags_json = json.dumps(tags) if tags else json.dumps([])
            values = (original_name, new_path, file_type, file_size, tags_json, datetime.now().isoformat())
            
            cursor.execute(insert_query, values)
            self.connection.commit()
            cursor.close()
            
            print(f"✅ Logged file movement: {original_name} → {new_path}")
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Error logging file movement: {e}")
            return False
    
    def get_file_logs(self, limit: int = 100, offset: int = 0, 
                     file_type: Optional[str] = None, 
                     tag_filter: Optional[str] = None,
                     date_from: Optional[datetime] = None,
                     date_to: Optional[datetime] = None) -> List[Dict]:
        """
        Retrieve file movement logs with optional filtering.
        
        Args:
            limit (int): Maximum number of records to return
            offset (int): Number of records to skip
            file_type (str, optional): Filter by file type
            tag_filter (str, optional): Filter by specific tag
            date_from (datetime, optional): Filter from date
            date_to (datetime, optional): Filter to date
            
        Returns:
            List[Dict]: List of file log records
        """
        if not self.connection:
            if not self.connect():
                return []
        
        try:
            cursor = self.connection.cursor()
            
            # Base query
            query = "SELECT * FROM file_logs WHERE 1=1"
            params = []
            
            # Add filters
            if file_type:
                query += " AND file_type = ?"
                params.append(file_type)
            
            if tag_filter:
                query += " AND tags LIKE ?"
                params.append(f'%"{tag_filter}"%')
            
            if date_from:
                query += " AND moved_at >= ?"
                params.append(date_from.isoformat())
            
            if date_to:
                query += " AND moved_at <= ?"
                params.append(date_to.isoformat())
            
            query += " ORDER BY moved_at DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            # Convert to list of dictionaries
            columns = [description[0] for description in cursor.description]
            logs = []
            for row in results:
                log_entry = dict(zip(columns, row))
                # Parse JSON tags back to lists
                if log_entry['tags']:
                    log_entry['tags'] = json.loads(log_entry['tags'])
                else:
                    log_entry['tags'] = []
                logs.append(log_entry)
            
            cursor.close()
            return logs
            
        except sqlite3.Error as e:
            print(f"❌ Error retrieving file logs: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about file movements.
        
        Returns:
            Dict: Statistics including total files, files by type, recent activity
        """
        if not self.connection:
            if not self.connect():
                return {}
        
        try:
            cursor = self.connection.cursor()
            
            stats = {}
            
            # Total files moved
            cursor.execute("SELECT COUNT(*) FROM file_logs")
            stats['total_files'] = cursor.fetchone()[0]
            
            # Files by type
            cursor.execute("""
                SELECT file_type, COUNT(*) as count 
                FROM file_logs 
                GROUP BY file_type 
                ORDER BY count DESC
            """)
            results = cursor.fetchall()
            stats['by_type'] = [{'file_type': row[0], 'count': row[1]} for row in results]
            
            # Recent activity (last 7 days)
            cursor.execute("""
                SELECT DATE(moved_at) as date, COUNT(*) as count
                FROM file_logs 
                WHERE moved_at >= DATE('now', '-7 days')
                GROUP BY DATE(moved_at)
                ORDER BY date DESC
            """)
            results = cursor.fetchall()
            stats['recent_activity'] = [{'date': row[0], 'count': row[1]} for row in results]
            
            # Most common tags (simplified for SQLite)
            cursor.execute("""
                SELECT tags, COUNT(*) as count
                FROM file_logs 
                WHERE tags IS NOT NULL AND tags != '[]'
                GROUP BY tags
                ORDER BY count DESC
                LIMIT 10
            """)
            results = cursor.fetchall()
            
            # Process tags to extract individual tags
            tag_counts = {}
            for row in results:
                try:
                    tags_list = json.loads(row[0])
                    for tag in tags_list:
                        if tag in tag_counts:
                            tag_counts[tag] += row[1]
                        else:
                            tag_counts[tag] = row[1]
                except:
                    continue
            
            # Sort and format popular tags
            popular_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            stats['popular_tags'] = [{'tag': tag, 'count': count} for tag, count in popular_tags]
            
            cursor.close()
            return stats
            
        except sqlite3.Error as e:
            print(f"❌ Error retrieving statistics: {e}")
            return {}
    
    def save_setting(self, key: str, value) -> bool:
        """
        Save application setting to database.
        
        Args:
            key (str): Setting identifier
            value: Setting value (will be JSON encoded)
            
        Returns:
            bool: True if saved successfully
        """
        if not self.connection:
            if not self.connect():
                return False
        
        try:
            cursor = self.connection.cursor()
            
            # SQLite UPSERT
            query = """
            INSERT OR REPLACE INTO app_settings (setting_key, setting_value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            """
            
            cursor.execute(query, (key, json.dumps(value)))
            self.connection.commit()
            cursor.close()
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Error saving setting: {e}")
            return False
    
    def get_setting(self, key: str, default_value=None):
        """
        Retrieve application setting from database.
        
        Args:
            key (str): Setting identifier
            default_value: Default value if setting not found
            
        Returns:
            Setting value or default_value
        """
        if not self.connection:
            if not self.connect():
                return default_value
        
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("SELECT setting_value FROM app_settings WHERE setting_key = ?", (key,))
            result = cursor.fetchone()
            
            cursor.close()
            
            if result:
                return json.loads(result[0])
            return default_value
            
        except sqlite3.Error as e:
            print(f"❌ Error getting setting: {e}")
            return default_value
    
    def close_connection(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            print("🔌 Database connection closed")


# Test function
if __name__ == "__main__":
    db = DatabaseManager()
    db.create_database_if_not_exists()
    
    if db.connect():
        db.initialize_tables()
        print("Database setup completed successfully!")
    else:
        print("Failed to setup database")
