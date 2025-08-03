# 🥷 FileNinja

**Intelligent File Organization System with Nothing OS-Inspired Interface**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Nothing OS Style](https://img.shields.io/badge/UI-Nothing%20OS-00d4ff.svg)](https://nothing.tech/)

FileNinja is a modern, intelligent file organization system that automatically sorts your files into clean categories while providing a beautiful Nothing OS-inspired web interface for browsing and managing your organized content.

![FileNinja Demo](Screenshot%202025-08-03%20192409.png)

## ✨ Features

### 🎯 **Core Functionality**
- **Automatic File Organization** - Smart categorization by file type with customizable rules
- **Real-time File Monitoring** - Watches your folders and organizes files as they're added using Watchdog
- **Intelligent File Type Detection** - Advanced file extension mapping and categorization logic
- **SQLite Database Logging** - Comprehensive tracking of all file movements and metadata
- **Cross-Platform Support** - Works on Windows, macOS, and Linux with platform-specific optimizations

### 🎨 **Nothing OS-Inspired Web Interface**
- **Glassmorphism Design** - Translucent panels with advanced blur effects and modern aesthetics
- **Neon Accent Colors** - Cyan and blue highlights with subtle glowing animations
- **Smooth Animations** - Cubic-bezier transitions and micro-interactions throughout the interface
- **Dark Theme** - Modern dark interface with ambient lighting effects
- **Responsive Design** - Optimized for desktop, tablet, and mobile devices
- **Interactive Elements** - Hover effects, status indicators, and animated button states

### 📊 **Dashboard & Analytics**
- **Real-time Statistics** - Live file counts, categories, and organization metrics
- **Storage Analytics** - Detailed breakdown by category with visual progress indicators
- **File Health Monitoring** - Track large files, duplicates, and storage optimization opportunities
- **Recent Activity Feed** - Visual timeline of file movements and system activities
- **Quick Actions Panel** - One-click tools for common file management tasks

### 🔧 **Management Tools**
- **File Browser** - Navigate organized files with intuitive folder/file views
- **System Integration** - Open files directly with system default applications
- **Manual Organization** - Trigger organization of existing files on demand
- **Connection Monitoring** - Real-time system status and health indicators
- **RESTful API** - Complete API for integration with other tools and automation

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ashutoshpatraa/FILENINJA.git
   cd FILENINJA
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure FileNinja (Optional)**
   Edit `config.json` to customize watched folders and organization settings:
   ```json
   {
     "watched_folders": ["C:\\Users\\YourName\\Downloads"],
     "organized_folder": "./Organized_Files",
     "auto_organize": true
   }
   ```

5. **Run FileNinja**
   ```bash
   python app.py --web
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000` to access the FileNinja interface

## 📁 Project Structure

```
FILENINJA/
├── 📄 app.py                 # Flask web application and main entry point
├── 🧠 core.py               # Core file organization and watching logic
├── 💾 db_manager.py         # SQLite database operations and management
├── ⚙️ config.json           # Application configuration and settings
├── 📋 requirements.txt      # Python dependencies
├── 🗂️ Organized_Files/      # Default organized files directory
├── 🌐 web/
│   └── index.html           # Nothing OS-inspired web interface
├── 🗃️ fileninja.db          # SQLite database file
└── 📸 Screenshot*.png       # Demo screenshots and documentation
```

## ⚙️ Configuration

FileNinja uses a `config.json` file for customization. Here are the key configuration options:

```json
{
  "watched_folders": [
    "C:\\Users\\YourName\\Downloads"
  ],
  "organized_folder": "./Organized_Files",
  "auto_organize": true,
  "organization_mode": "type_and_tag",
  "ignore_patterns": [
    "*.tmp", "*.temp", "*.part", "*.crdownload",
    ".DS_Store", "Thumbs.db", "*.lock"
  ],
  "delay_seconds": 2,
  "max_file_size_mb": 1000,
  "web_interface": {
    "enabled": true,
    "host": "127.0.0.1",
    "port": 5000,
    "debug": false
  }
}
```

### Configuration Options:
- **`watched_folders`** - List of directories to monitor for new files
- **`organized_folder`** - Destination folder for organized files
- **`auto_organize`** - Enable/disable automatic file organization
- **`ignore_patterns`** - File patterns to ignore during organization
- **`delay_seconds`** - Wait time before processing new files
- **`max_file_size_mb`** - Maximum file size to process (in MB)

## 🎮 Usage

### Command Line Options
FileNinja supports several command-line modes:

```bash
# Start complete system with web interface (default)
python app.py --web

# Start only file watching (no web interface)
python app.py --watch-only

# Organize existing files and exit
python app.py --organize

# Custom host and port
python app.py --web --host 0.0.0.0 --port 8080
```

### Web Interface
- **Dashboard** - Monitor file organization progress and system health
- **File Browser** - Navigate organized files by category with search capabilities
- **Activity Logs** - Track file movements with detailed timestamps and metadata
- **Quick Actions** - Manual organization triggers and system maintenance tools

### API Endpoints
FileNinja provides a RESTful API for automation:
- `GET /api/status` - System status and health
- `GET /api/stats` - Organization statistics and analytics
- `GET /api/files` - Browse organized files
- `POST /api/organize` - Trigger manual organization
- `GET /api/logs` - File movement history

## 🎨 UI Design Philosophy

FileNinja's interface is inspired by Nothing OS design principles:

- **Glassmorphism** - Translucent elements with backdrop blur
- **Minimalism** - Clean, uncluttered layouts with purposeful white space
- **Ambient Lighting** - Subtle gradients and glow effects
- **Micro-interactions** - Smooth animations and hover effects
- **Typography** - Inter font family for clean, readable text
- **Color Palette** - Dark backgrounds with cyan accent colors

## 🔧 Technical Details

### Architecture
FileNinja uses a modular architecture with clear separation of concerns:

- **Flask Backend** - Lightweight Python web server with RESTful API
- **SQLite Database** - Embedded database for file movement logging and metadata
- **Watchdog Integration** - Cross-platform file system monitoring with polling fallback
- **Threaded Processing** - Non-blocking file operations and web interface

### Key Components
1. **FileNinjaCore** (`core.py`) - File watching, organization logic, and type detection
2. **DatabaseManager** (`db_manager.py`) - SQLite operations and data persistence
3. **Flask Application** (`app.py`) - Web interface and API endpoints
4. **Web Interface** (`web/index.html`) - Nothing OS-inspired frontend

### File Organization Process
1. **Detection** - Watchdog monitors configured directories for file system events
2. **Filtering** - Ignore temporary files and patterns based on configuration
3. **Classification** - Analyze file extensions and apply organization rules
4. **Processing** - Move files to appropriate categories with duplicate handling
5. **Logging** - Record all operations in SQLite database with metadata

### Frontend Technologies
- **TailwindCSS** - Utility-first CSS framework for rapid UI development
- **Lucide Icons** - Consistent, beautiful icon system
- **Vanilla JavaScript** - Lightweight, framework-free frontend code
- **CSS Glassmorphism** - Modern UI effects with backdrop filters

## 🛠️ Development

### Setting Up Development Environment
1. **Fork and clone the repository**
2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run in development mode**
   ```bash
   python app.py --web --host 127.0.0.1 --port 5000
   ```

### Project Structure & Customization

#### Adding New File Types
Modify the file type mapping in `core.py`:
```python
def _get_file_type_mapping(self) -> Dict[str, str]:
    return {
        '.pdf': 'Documents',
        '.doc': 'Documents', 
        '.jpg': 'Images',
        '.mp4': 'Media',  # Add new types here
        # ... more mappings
    }
```

#### Customizing Organization Rules
Update the organization structure in `core.py`:
```python
def _get_organization_structure(self) -> Dict[str, List[str]]:
    return {
        'Documents': ['.pdf', '.doc', '.docx', '.txt'],
        'Images': ['.jpg', '.jpeg', '.png', '.gif'],
        'Media': ['.mp4', '.avi', '.mov'],  # New category
        # ... more categories
    }
```

#### Extending the Web Interface
The web interface (`web/index.html`) uses:
- **Modular JavaScript functions** for easy feature additions
- **TailwindCSS utility classes** for consistent styling
- **CSS custom properties** for theme management

### API Integration
FileNinja provides comprehensive REST endpoints for integration:

```javascript
// Example API usage
const response = await fetch('/api/stats');
const stats = await response.json();
console.log(`Organized ${stats.total_files} files`);
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Guidelines
- **Code Style** - Follow PEP 8 for Python, use meaningful variable names
- **Commit Messages** - Use conventional commits (feat:, fix:, docs:, etc.)
- **Testing** - Add tests for new features in the future test suite
- **Documentation** - Update README and code comments for new features
- **Performance** - Consider file system impact and memory usage for large directories

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Nothing Technology** - Design inspiration from Nothing OS
- **TailwindCSS** - Excellent utility-first CSS framework
- **Lucide** - Beautiful open-source icons
- **Flask Community** - Robust web framework and ecosystem

## 📞 Support & Community

- **🐛 Issues** - Report bugs or request features via [GitHub Issues](https://github.com/ashutoshpatraa/FILENINJA/issues)
- **💬 Discussions** - Join community discussions in [GitHub Discussions](https://github.com/ashutoshpatraa/FILENINJA/discussions)
- **📖 Documentation** - Check the [Wiki](https://github.com/ashutoshpatraa/FILENINJA/wiki) for detailed guides
- **⭐ Star the Project** - Show your support by starring the repository

### Frequently Asked Questions

**Q: Does FileNinja work on Windows/Mac/Linux?**
A: Yes! FileNinja is cross-platform and includes platform-specific optimizations.

**Q: Can I customize the file organization categories?**
A: Absolutely! Edit the `config.json` file or modify the organization rules in `core.py`.

**Q: Is my data safe? Does FileNinja delete files?**
A: FileNinja only moves files, never deletes them. All operations are logged in the SQLite database.

**Q: Can I use FileNinja programmatically?**
A: Yes! FileNinja provides a complete REST API for automation and integration.

---

<div align="center">

**Made with 🥷 by [Ashutosh Patra](https://github.com/ashutoshpatraa)**

*Transform your file chaos into organized zen with Nothing OS aesthetics*

[⭐ Star this project](https://github.com/ashutoshpatraa/FILENINJA) • [🍴 Fork](https://github.com/ashutoshpatraa/FILENINJA/fork) • [📝 Report Issues](https://github.com/ashutoshpatraa/FILENINJA/issues)

<br>

**Made by Ashu with ❤️**

</div>
