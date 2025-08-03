"""
FileNinja Core Module - Consolidated File Organization System

This module combines file watching, moving, and tagging functionality
into a single, streamlined module for easier maintenance and deployment.
"""

import os
import shutil
import time
import platform
import re
import hashlib
import threading
import json
from pathlib import Path
from typing import List, Set, Dict, Callable, Optional, Tuple
from datetime import datetime

# Import watchdog components with Windows compatibility
from watchdog.events import FileSystemEventHandler, FileSystemEvent

# Windows compatibility - use polling observer
if platform.system() == "Windows":
    try:
        from watchdog.observers.polling import PollingObserver as Observer
        print("🔧 Using PollingObserver for Windows compatibility")
    except ImportError:
        from watchdog.observers import Observer
else:
    from watchdog.observers import Observer


class FileNinjaCore:
    """
    Core FileNinja class that handles file watching, organization, and tagging.
    Combines all essential functionality in a single class.
    """
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize FileNinja Core with configuration."""
        self.config = self._load_config(config_path)
        self.base_folder = Path(self.config.get("organized_folder", "./Organized_Files"))
        self.watched_folders = self.config.get("watched_folders", [])
        
        # File organization mappings
        self.file_type_mapping = self._get_file_type_mapping()
        self.organization_structure = self._get_organization_structure()
        self.tag_rules = self._get_tag_rules()
        
        # File watcher components
        self.observer = Observer()
        self.watched_paths = {}
        self.is_running = False
        self.pending_files = {}
        self.processed_files = set()
        self.lock = threading.Lock()
        
        # Ensure base folder exists
        self.base_folder.mkdir(parents=True, exist_ok=True)
        
        print(f"🥷 FileNinja Core initialized")
        print(f"📁 Organized folder: {self.base_folder}")
        print(f"👀 Watched folders: {len(self.watched_folders)}")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from file."""
        default_config = {
            "watched_folders": [str(Path.home() / "Downloads")],
            "organized_folder": "./Organized_Files",
            "auto_organize": True,
            "delay_seconds": 2,
            "max_file_size_mb": 1000,
            "ignore_patterns": [
                "*.tmp", "*.temp", "*.part", "*.crdownload",
                ".DS_Store", "Thumbs.db", "*.lock"
            ]
        }
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
        except Exception as e:
            print(f"⚠️ Error loading config: {e}")
        
        return default_config
    
    def _get_file_type_mapping(self) -> Dict[str, str]:
        """Get mapping of file extensions to file types."""
        return {
            # PDFs
            '.pdf': 'PDFs',
            
            # Documents (Word, text, presentations, spreadsheets)
            '.doc': 'Documents', '.docx': 'Documents', '.txt': 'Documents', 
            '.rtf': 'Documents', '.odt': 'Documents', '.xls': 'Documents', 
            '.xlsx': 'Documents', '.csv': 'Documents', '.ppt': 'Documents', 
            '.pptx': 'Documents',
            
            # Images
            '.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images',
            '.gif': 'Images', '.bmp': 'Images', '.svg': 'Images',
            '.webp': 'Images', '.tiff': 'Images',
            
            # Everything else goes to Other
            '.mp4': 'Other', '.avi': 'Other', '.mkv': 'Other',
            '.mov': 'Other', '.wmv': 'Other', '.webm': 'Other',
            '.mp3': 'Other', '.wav': 'Other', '.flac': 'Other',
            '.aac': 'Other', '.ogg': 'Other', '.m4a': 'Other',
            '.zip': 'Other', '.rar': 'Other', '.7z': 'Other',
            '.tar': 'Other', '.gz': 'Other',
            '.py': 'Other', '.js': 'Other', '.html': 'Other',
            '.css': 'Other', '.json': 'Other', '.xml': 'Other',
            '.exe': 'Other', '.msi': 'Other'
        }
    
    def _get_organization_structure(self) -> Dict[str, List[str]]:
        """Get folder organization structure."""
        return {
            'PDFs': ['PDFs'],
            'Documents': ['Documents'],
            'Images': ['Images'],
            'Other': ['Other']
        }
    
    def _get_tag_rules(self) -> Dict[str, Dict]:
        """Get tagging rules for intelligent file organization."""
        return {
            "finance": {
                "keywords": ["invoice", "receipt", "bill", "payment", "tax", "bank", "statement"]
            },
            "work": {
                "keywords": ["project", "meeting", "presentation", "report", "proposal", "contract"]
            },
            "personal": {
                "keywords": ["family", "vacation", "holiday", "birthday", "photo", "travel"]
            },
            "education": {
                "keywords": ["homework", "assignment", "exam", "notes", "lecture", "study"]
            }
        }
    
    # FILE TAGGING METHODS
    def get_file_tags(self, file_path: str) -> List[str]:
        """Get tags for a file based on filename analysis."""
        filename = os.path.basename(file_path).lower()
        name_without_ext = os.path.splitext(filename)[0]
        tags = set()
        
        # Check tag rules
        for category, rules in self.tag_rules.items():
            for keyword in rules.get("keywords", []):
                if keyword in name_without_ext:
                    tags.add(category)
                    break
        
        # Add file type tag
        file_extension = Path(file_path).suffix.lower()
        if file_extension:
            tags.add(f"type_{file_extension[1:]}")
        
        # Add date tags
        date_patterns = [r"(19|20)\d{2}", r"jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec"]
        for pattern in date_patterns:
            if re.search(pattern, name_without_ext):
                tags.add("dated")
                break
        
        return sorted(list(tags))
    
    # FILE ORGANIZATION METHODS
    def get_file_type(self, file_path: str) -> str:
        """Determine file type based on extension."""
        extension = Path(file_path).suffix.lower()
        return self.file_type_mapping.get(extension, 'Other')
    
    def get_destination_folder(self, file_path: str, tags: List[str] = None) -> Path:
        """Get destination folder for a file."""
        file_type = self.get_file_type(file_path)
        
        # Check for priority tags
        if tags:
            priority_tags = ['finance', 'work', 'personal', 'education']
            for priority_tag in priority_tags:
                if priority_tag in tags:
                    return self.base_folder / f"{priority_tag.title()}_Files"
        
        # Use file type folder
        return self.base_folder / file_type
    
    def handle_filename_conflict(self, dest_path: Path) -> Path:
        """Handle filename conflicts by appending numbers."""
        if not dest_path.exists():
            return dest_path
        
        base = dest_path.stem
        suffix = dest_path.suffix
        parent = dest_path.parent
        counter = 1
        
        while counter <= 1000:
            new_name = f"{base}_{counter}{suffix}"
            new_path = parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1
        
        # Fallback with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return parent / f"{base}_{timestamp}{suffix}"
    
    def move_file(self, source_path: str, tags: List[str] = None) -> Tuple[bool, str, str]:
        """Move a file to its organized location."""
        try:
            source = Path(source_path)
            if not source.exists() or not source.is_file():
                return False, "", f"Invalid source file: {source_path}"
            
            # Get destination
            dest_folder = self.get_destination_folder(source_path, tags)
            dest_path = dest_folder / source.name
            dest_path = self.handle_filename_conflict(dest_path)
            
            # Create destination folder
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Move file
            shutil.move(str(source), str(dest_path))
            return True, str(dest_path), f"Moved to: {dest_path.name}"
            
        except Exception as e:
            return False, "", f"Error moving file: {str(e)}"
    
    # FILE WATCHING METHODS
    def should_ignore_file(self, file_path: str) -> bool:
        """Check if file should be ignored based on patterns."""
        filename = os.path.basename(file_path).lower()
        ignore_patterns = self.config.get("ignore_patterns", [])
        
        for pattern in ignore_patterns:
            if pattern.startswith('*') and filename.endswith(pattern[1:]):
                return True
            elif pattern.endswith('*') and filename.startswith(pattern[:-1]):
                return True
            elif pattern in filename:
                return True
        
        return False
    
    def should_process_file(self, file_path: str) -> bool:
        """Check if file should be processed."""
        try:
            if self.should_ignore_file(file_path):
                return False
            
            # Check file size
            max_size = self.config.get("max_file_size_mb", 1000) * 1024 * 1024
            if os.path.getsize(file_path) > max_size:
                return False
            
            return True
        except Exception:
            return False
    
    def process_file(self, file_path: str, event_type: str = "created"):
        """Process a detected file."""
        try:
            if not self.should_process_file(file_path):
                return
            
            print(f"📂 Processing {event_type} file: {os.path.basename(file_path)}")
            
            # Get tags
            tags = self.get_file_tags(file_path)
            
            # Move file
            success, dest_path, message = self.move_file(file_path, tags)
            
            if success:
                print(f"✅ {message}")
                # Log to database if available
                self.log_file_movement(file_path, dest_path, tags)
            else:
                print(f"❌ {message}")
                
        except Exception as e:
            print(f"❌ Error processing file {file_path}: {e}")
    
    def log_file_movement(self, source_path: str, dest_path: str, tags: List[str]):
        """Log file movement to database."""
        try:
            from db_manager import DatabaseManager
            import os
            
            db = DatabaseManager()
            if db.connect():
                # Get file information
                original_name = os.path.basename(source_path)
                file_size = os.path.getsize(source_path) if os.path.exists(source_path) else 0
                file_type = self.get_file_type(source_path)
                
                db.log_file_movement(original_name, dest_path, file_type, file_size, tags)
        except Exception as e:
            print(f"⚠️ Could not log to database: {e}")
    
    # FILE WATCHER EVENT HANDLER
    def create_event_handler(self):
        """Create file system event handler."""
        class FileNinjaHandler(FileSystemEventHandler):
            def __init__(self, core_instance):
                self.core = core_instance
                super().__init__()
            
            def on_created(self, event):
                if not event.is_directory:
                    self.core.schedule_file_processing(event.src_path, 'created')
            
            def on_moved(self, event):
                if not event.is_directory:
                    self.core.schedule_file_processing(event.dest_path, 'moved')
        
        return FileNinjaHandler(self)
    
    def schedule_file_processing(self, file_path: str, event_type: str):
        """Schedule file processing with delay."""
        delay = self.config.get("delay_seconds", 2)
        
        with self.lock:
            # Cancel previous timer if exists
            if file_path in self.pending_files:
                self.pending_files[file_path].cancel()
            
            # Schedule new processing
            timer = threading.Timer(delay, self.process_file, args=[file_path, event_type])
            self.pending_files[file_path] = timer
            timer.start()
    
    # MAIN CONTROL METHODS
    def start_watching(self) -> bool:
        """Start file watching."""
        try:
            if self.is_running:
                print("⚠️ Already running")
                return False
            
            # Add watched folders
            handler = self.create_event_handler()
            for folder in self.watched_folders:
                if os.path.exists(folder):
                    watch = self.observer.schedule(handler, folder, recursive=True)
                    self.watched_paths[folder] = watch
                    print(f"👀 Watching: {folder}")
                else:
                    print(f"⚠️ Folder not found: {folder}")
            
            if not self.watched_paths:
                print("❌ No valid folders to watch")
                return False
            
            self.observer.start()
            self.is_running = True
            print(f"🎯 FileNinja started - monitoring {len(self.watched_paths)} folder(s)")
            return True
            
        except Exception as e:
            print(f"❌ Error starting: {e}")
            return False
    
    def stop_watching(self):
        """Stop file watching."""
        try:
            if not self.is_running:
                return
            
            self.observer.stop()
            self.observer.join(timeout=5)
            self.is_running = False
            
            # Cancel pending timers
            with self.lock:
                for timer in self.pending_files.values():
                    timer.cancel()
                self.pending_files.clear()
            
            print("🛑 FileNinja stopped")
            
        except Exception as e:
            print(f"❌ Error stopping: {e}")
    
    def get_status(self) -> Dict:
        """Get current status."""
        return {
            'is_running': self.is_running,
            'watched_folders': list(self.watched_paths.keys()),
            'watched_count': len(self.watched_paths),
            'base_folder': str(self.base_folder),
            'pending_files': len(self.pending_files)
        }
    
    def organize_existing_files(self, folder_path: str = None):
        """Organize existing files in watched folders."""
        folders_to_scan = [folder_path] if folder_path else self.watched_folders
        
        for folder in folders_to_scan:
            if not os.path.exists(folder):
                continue
            
            print(f"🔍 Scanning existing files in: {folder}")
            processed_count = 0
            
            for root, dirs, files in os.walk(folder):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    
                    if self.should_process_file(file_path):
                        self.process_file(file_path, 'existing')
                        processed_count += 1
            
            print(f"✅ Processed {processed_count} existing files from {folder}")
    
    def get_organization_stats(self) -> Dict:
        """Get statistics about organized files."""
        stats = {
            'total_files': 0,
            'total_size': 0,
            'by_type': {},
            'recent_activity': []
        }
        
        if not self.base_folder.exists():
            return stats
        
        for file_path in self.base_folder.rglob('*'):
            if file_path.is_file():
                stats['total_files'] += 1
                try:
                    file_size = file_path.stat().st_size
                    stats['total_size'] += file_size
                    
                    file_type = self.get_file_type(str(file_path))
                    if file_type not in stats['by_type']:
                        stats['by_type'][file_type] = {'count': 0, 'size': 0}
                    
                    stats['by_type'][file_type]['count'] += 1
                    stats['by_type'][file_type]['size'] += file_size
                    
                except Exception:
                    pass
        
        return stats


# Test function
if __name__ == "__main__":
    print("🥷 FileNinja Core Testing")
    print("=" * 40)
    
    # Initialize core
    core = FileNinjaCore()
    
    # Test file type detection
    test_files = ["document.pdf", "image.jpg", "video.mp4", "song.mp3"]
    for filename in test_files:
        file_type = core.get_file_type(filename)
        tags = core.get_file_tags(filename)
        print(f"📄 {filename} → Type: {file_type}, Tags: {tags}")
    
    # Test status
    status = core.get_status()
    print(f"\n📊 Status: {status}")
    
    print("\n✅ Core testing completed!")
