"""
FileNinja - Streamlined File Organization System

A modern, consolidated file organization system that automatically sorts files
and provides a beautiful web interface for browsing organized content.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import subprocess
import threading
import time

# Import consolidated core
from core import FileNinjaCore
from db_manager import DatabaseManager


class FileNinjaApp:
    """Main FileNinja Application class."""
    
    def __init__(self):
        """Initialize the FileNinja application."""
        self.core = FileNinjaCore()
        self.db = DatabaseManager()
        self.flask_app = Flask(__name__)
        CORS(self.flask_app)  # Enable CORS for web interface
        
        # Setup Flask routes
        self._setup_routes()
        
        print("🥷 FileNinja Application initialized")
    
    def _setup_routes(self):
        """Setup Flask web routes."""
        
        @self.flask_app.route('/')
        def index():
            """Serve the main web interface."""
            web_dir = os.path.join(os.path.dirname(__file__), 'web')
            return send_from_directory(web_dir, 'index.html')
        
        @self.flask_app.route('/api/status')
        def api_status():
            """Get system status."""
            try:
                core_status = self.core.get_status()
                db_status = self.db.get_connection_status() if hasattr(self.db, 'get_connection_status') else True
                
                return jsonify({
                    'status': 'running' if core_status['is_running'] else 'stopped',
                    'core': core_status,
                    'database': 'connected' if db_status else 'disconnected'
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.flask_app.route('/api/stats')
        def api_stats():
            """Get enhanced file organization statistics."""
            try:
                stats = self.core.get_organization_stats()
                base_path = self.core.base_folder
                
                # Enhanced stats for real usefulness
                enhanced_stats = {
                    **stats,
                    'storage_by_category': {},
                    'largest_files': [],
                    'recently_accessed': [],
                    'file_health': {
                        'duplicates': 0,
                        'large_files': 0,
                        'old_files': 0
                    },
                    'ninja_score': 0,
                    'connection_info': {
                        'type': 'Local System',
                        'status': 'Active',
                        'location': str(base_path) if base_path.exists() else 'Not Found'
                    },
                    'quick_wins': [],
                    'user_flow_step': 'initial'
                }
                
                if base_path.exists():
                    all_files = list(base_path.rglob('*'))
                    file_objects = [f for f in all_files if f.is_file()]
                    
                    # Storage by category
                    category_sizes = {}
                    largest_files = []
                    # Storage by category
                    for file_path in file_objects:
                        try:
                            size = file_path.stat().st_size
                            category = file_path.parent.name
                            
                            # Category storage
                            if category not in category_sizes:
                                category_sizes[category] = 0
                            category_sizes[category] += size
                            
                            # Largest files
                            largest_files.append({
                                'name': file_path.name,
                                'size': size,
                                'category': category,
                                'path': str(file_path).replace('\\', '/'),
                                'modified': file_path.stat().st_mtime
                            })
                            
                            # File health checks
                            if size > 50 * 1024 * 1024:  # >50MB
                                enhanced_stats['file_health']['large_files'] += 1
                            
                            if (time.time() - file_path.stat().st_mtime) > (365 * 24 * 3600):  # >1 year old
                                enhanced_stats['file_health']['old_files'] += 1
                                
                        except (OSError, PermissionError):
                            continue
                    
                    # Format storage by category (in MB)
                    for category, size in category_sizes.items():
                        enhanced_stats['storage_by_category'][category] = {
                            'size_mb': round(size / (1024 * 1024), 1),
                            'size_bytes': size,
                            'files': len([f for f in file_objects if f.parent.name == category])
                        }
                    
                    # Top 5 largest files
                    enhanced_stats['largest_files'] = sorted(
                        largest_files, key=lambda x: x['size'], reverse=True
                    )[:5]
                    
                    # Ninja score calculation (0-100) with quick wins
                    total_files = len(file_objects)
                    organized_files = len([f for f in file_objects if 'Organized_Files' in str(f)])
                    if total_files > 0:
                        enhanced_stats['ninja_score'] = min(100, int((organized_files / total_files) * 100))
                    
                    # Generate quick wins for user engagement
                    quick_wins = []
                    if enhanced_stats['file_health']['large_files'] > 0:
                        quick_wins.append({
                            'title': "Free up space",
                            'description': f"Clean {enhanced_stats['file_health']['large_files']} large files",
                            'action': 'cleanup_large',
                            'impact': 'high',
                            'time': '2 min'
                        })
                    
                    if enhanced_stats['ninja_score'] < 50:
                        quick_wins.append({
                            'title': "Boost your score",
                            'description': "Auto-organize unorganized files",
                            'action': 'auto_organize',
                            'impact': 'high',
                            'time': '30 sec'
                        })
                    
                    if len(category_sizes) == 0:
                        quick_wins.append({
                            'title': "Get started",
                            'description': "Drop files to organize them",
                            'action': 'onboarding',
                            'impact': 'medium',
                            'time': '1 min'
                        })
                        enhanced_stats['user_flow_step'] = 'first_time'
                    
                    enhanced_stats['quick_wins'] = quick_wins[:3]  # Top 3 quick wins
                
                # Add database stats if available
                if self.db.connect():
                    try:
                        recent_files = self.db.get_file_logs(limit=5)
                        enhanced_stats['recent_activity'] = recent_files
                        
                        # Recently accessed (mock data for now)
                        enhanced_stats['recently_accessed'] = recent_files[:3]
                    except Exception:
                        enhanced_stats['recent_activity'] = []
                        enhanced_stats['recently_accessed'] = []
                
                return jsonify(enhanced_stats)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.flask_app.route('/api/files')
        def api_files():
            """Get files in organized folders."""
            try:
                path = request.args.get('path', 'Organized_Files')
                base_path = self.core.base_folder
                
                # Handle path navigation
                if path != 'Organized_Files':
                    # Remove 'Organized_Files/' prefix if present
                    clean_path = path.replace('Organized_Files/', '').replace('Organized_Files', '')
                    if clean_path:
                        full_path = base_path / clean_path
                    else:
                        full_path = base_path
                else:
                    full_path = base_path
                
                if not full_path.exists():
                    # Create the organized folder if it doesn't exist
                    full_path.mkdir(parents=True, exist_ok=True)
                
                files = []
                folders = []
                
                for item in full_path.iterdir():
                    if item.is_file():
                        # Use forward slashes for JSON compatibility, convert in backend
                        absolute_path = item.resolve()
                        path_str = str(absolute_path).replace('\\', '/')
                        files.append({
                            'name': item.name,
                            'path': path_str,
                            'size': item.stat().st_size,
                            'modified': item.stat().st_mtime,
                            'extension': item.suffix.lower()
                        })
                    elif item.is_dir():
                        folder_files = list(item.rglob('*'))
                        file_count = len([f for f in folder_files if f.is_file()])
                        # Format folder path for web navigation
                        relative_folder_path = str(item.relative_to(base_path)).replace('\\', '/')
                        folders.append({
                            'name': item.name,
                            'path': f"Organized_Files/{relative_folder_path}",
                            'count': file_count
                        })
                
                return jsonify({
                    'success': True,
                    'files': files,
                    'folders': folders,
                    'current_path': str(full_path),
                    'base_path': str(base_path)
                })
                
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
        
        @self.flask_app.route('/api/open-file', methods=['POST'])
        def api_open_file():
            """Open a file with system default application."""
            try:
                data = request.get_json()
                file_path = data.get('path')
                
                if not file_path:
                    return jsonify({'success': False, 'error': 'No file path provided'})
                
                print(f"🔍 Received file path: {repr(file_path)}")  # Debug log
                
                # Convert forward slashes to backslashes for Windows
                if sys.platform.startswith('win'):
                    file_path = file_path.replace('/', '\\')
                
                print(f"🔧 Converted file path: {repr(file_path)}")  # Debug log
                
                # Convert to Path object for better handling
                path_obj = Path(file_path)
                
                # Check if file exists
                if not path_obj.exists():
                    # Try searching for the file in the organized folder
                    base_path = self.core.base_folder
                    print(f"🔍 File not found, searching in: {base_path}")
                    for possible_file in base_path.rglob(path_obj.name):
                        if possible_file.is_file():
                            path_obj = possible_file
                            print(f"✅ Found file at: {path_obj}")
                            break
                    else:
                        return jsonify({'success': False, 'error': f'File not found: {path_obj}'})
                
                # Convert back to string for subprocess
                file_path_str = str(path_obj.resolve())
                print(f"🚀 Opening file: {file_path_str}")  # Debug log
                
                # Open file with system default
                if sys.platform.startswith('darwin'):  # macOS
                    subprocess.call(['open', file_path_str])
                elif sys.platform.startswith('win'):  # Windows
                    os.startfile(file_path_str)
                else:  # Linux
                    subprocess.call(['xdg-open', file_path_str])
                
                return jsonify({'success': True, 'message': f'Opened: {path_obj.name}'})
                
            except Exception as e:
                print(f"❌ Error opening file: {e}")  # Debug log
                return jsonify({'success': False, 'error': f'Error opening file: {str(e)}'})
        
        @self.flask_app.route('/api/logs')
        def api_logs():
            """Get file movement logs."""
            try:
                logs = []
                if self.db.connect():
                    try:
                        logs = self.db.get_file_logs(limit=50)
                    except Exception:
                        pass

                return jsonify({'logs': logs})

            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @self.flask_app.route('/api/recent-files')
        def api_recent_files():
            """Get recent files for thumbnail display."""
            try:
                recent_files = []
                
                # Try to get from database first
                if self.db.connect():
                    try:
                        db_files = self.db.get_file_logs(limit=20)
                        for file_record in db_files:
                            if isinstance(file_record, dict):
                                original_path = file_record.get('original_path', '')
                                if original_path and Path(original_path).exists():
                                    file_path = Path(original_path)
                                    recent_files.append({
                                        'path': str(file_path),
                                        'name': file_path.name,
                                        'extension': file_path.suffix.lstrip('.'),
                                        'size': file_path.stat().st_size,
                                        'created_at': file_record.get('created_at', '')
                                    })
                    except Exception as db_error:
                        print(f"Database error in recent-files: {db_error}")
                
                # Fallback: get files from organized folder
                if not recent_files:
                    base_path = self.core.base_folder
                    if base_path.exists():
                        all_files = list(base_path.rglob('*'))
                        file_objects = [f for f in all_files if f.is_file()]
                        file_objects.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                        
                        for file_path in file_objects[:20]:
                            try:
                                recent_files.append({
                                    'path': str(file_path),
                                    'name': file_path.name,
                                    'extension': file_path.suffix.lstrip('.'),
                                    'size': file_path.stat().st_size,
                                    'created_at': file_path.stat().st_mtime
                                })
                            except (OSError, PermissionError):
                                continue

                return jsonify(recent_files)

            except Exception as e:
                print(f"Error in recent-files API: {e}")
                return jsonify([])        @self.flask_app.route('/api/organize', methods=['POST'])
        def api_organize():
            """Manually trigger organization of existing files."""
            try:
                data = request.get_json() or {}
                folder_path = data.get('folder')
                
                # Run organization in background thread
                def organize_files():
                    self.core.organize_existing_files(folder_path)
                
                threading.Thread(target=organize_files, daemon=True).start()
                
                return jsonify({'success': True, 'message': 'Organization started'})
                
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
    
    def start_web_interface(self, host='127.0.0.1', port=5000, debug=False):
        """Start the web interface."""
        print(f"🌐 Starting web interface at http://{host}:{port}")
        self.flask_app.run(host=host, port=port, debug=debug)
    
    def start_file_watching(self):
        """Start file watching in background."""
        if self.core.start_watching():
            print("✅ File watching started")
            return True
        else:
            print("❌ Failed to start file watching")
            return False
    
    def run_complete_system(self, host='127.0.0.1', port=5000):
        """Run both file watching and web interface."""
        print("🚀 Starting complete FileNinja system...")
        
        # Initialize database
        if self.db.connect():
            self.db.initialize_tables()
            print("✅ Database initialized")
        
        # Start file watching in background thread
        def start_watcher():
            time.sleep(1)  # Small delay to let Flask start
            self.start_file_watching()
        
        watcher_thread = threading.Thread(target=start_watcher, daemon=True)
        watcher_thread.start()
        
        # Start web interface (blocks)
        self.start_web_interface(host=host, port=port)
    
    def organize_existing(self):
        """Organize existing files in watched folders."""
        print("🔍 Organizing existing files...")
        self.core.organize_existing_files()
        print("✅ Existing file organization completed")
    
    def get_status(self):
        """Get application status."""
        return {
            'core': self.core.get_status(),
            'database': self.db.connect() if hasattr(self.db, 'connect') else True
        }


def main():
    """Main entry point for FileNinja."""
    parser = argparse.ArgumentParser(description='FileNinja - File Organization System')
    parser.add_argument('--web', action='store_true', help='Start with web interface')
    parser.add_argument('--watch-only', action='store_true', help='Only start file watching')
    parser.add_argument('--organize', action='store_true', help='Organize existing files and exit')
    parser.add_argument('--host', default='127.0.0.1', help='Web interface host')
    parser.add_argument('--port', type=int, default=5000, help='Web interface port')
    
    args = parser.parse_args()
    
    # Initialize application
    app = FileNinjaApp()
    
    try:
        if args.organize:
            # Organize existing files and exit
            app.organize_existing()
        elif args.watch_only:
            # Only start file watching
            if app.start_file_watching():
                print("🎯 File watching active. Press Ctrl+C to stop.")
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n🛑 Stopping file watching...")
                    app.core.stop_watching()
        elif args.web:
            # Start complete system (default)
            app.run_complete_system(host=args.host, port=args.port)
        else:
            # Default: start complete system
            app.run_complete_system(host=args.host, port=args.port)
            
    except KeyboardInterrupt:
        print("\n🛑 FileNinja stopped by user")
        app.core.stop_watching()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
