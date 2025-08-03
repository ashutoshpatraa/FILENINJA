# 🥷 FileNinja

**Intelligent File Organization System with Nothing OS-Inspired Interface**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Nothing OS Style](https://img.shields.io/badge/UI-Nothing%20OS-00d4ff.svg)](https://nothing.tech/)

FileNinja is a modern, intelligent file organization system that automatically sorts your files into clean categories while providing a beautiful Nothing OS-inspired web interface for browsing and managing your organized content.

![FileNinja Demo](Screenshot%202025-08-03%20192409.png)

## ✨ Features

### 🎯 **Core Functionality**
- **Automatic File Organization** - Smart categorization into 4 simplified categories (PDFs, Documents, Images, Other)
- **Real-time File Monitoring** - Watches your folders and organizes files as they're added
- **Intelligent File Type Detection** - Advanced file extension mapping and categorization
- **Database Logging** - SQLite database tracks all file movements and metadata
- **File Size & Health Monitoring** - Track storage usage and file system health

### 🎨 **Nothing OS-Inspired Interface**
- **Glassmorphism Design** - Translucent panels with advanced blur effects
- **Neon Accent Colors** - Cyan and blue highlights with glowing animations
- **Smooth Animations** - Cubic-bezier transitions and micro-interactions
- **Dark Theme** - Modern dark interface with subtle ambient lighting
- **Responsive Design** - Works beautifully on desktop, tablet, and mobile
- **Interactive Elements** - Hover effects, status indicators, and button animations

### 📊 **Dashboard Features**
- **Ninja Score System** - Gamified organization scoring with level progression
- **Real-time Statistics** - File counts, categories, and health metrics
- **Quick Wins Panel** - Smart suggestions for improving organization
- **Recent Files Thumbnails** - Visual preview of recently organized files
- **Storage Analytics** - Breakdown by category with visual progress bars
- **Activity Logs** - Detailed history of all file movements

### 🔧 **Advanced Tools**
- **File Browser** - Navigate organized files with folder/file views
- **Smart Actions** - Auto-organize, smart cleanup, and file finding tools
- **Connection Status** - Real-time system monitoring and health checks
- **Extensible Architecture** - Modular design for easy feature additions

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/FileNinja.git
   cd FileNinja
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

4. **Run FileNinja**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000` to access the FileNinja interface

## 📁 Project Structure

```
FileNinja/
├── 📄 app.py                 # Flask web application
├── 🧠 core.py               # Core file organization logic
├── 💾 db_manager.py         # SQLite database operations
├── ⚙️ config.json           # Application configuration
├── 📋 requirements.txt      # Python dependencies
├── 🗂️ Organized_Files/      # Default organized files directory
├── 🌐 web/
│   └── index.html           # Nothing OS-inspired web interface
├── 🗃️ fileninja.db          # SQLite database file
└── 📸 Screenshot*.png       # Demo screenshots
```

## ⚙️ Configuration

FileNinja uses a `config.json` file for configuration:

```json
{
  "watch_folders": [
    "C:\\Users\\YourName\\Downloads"
  ],
  "organized_folder": "Organized_Files",
  "file_categories": {
    "PDFs": [".pdf"],
    "Documents": [".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".csv", ".ppt", ".pptx"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff"],
    "Other": ["*"]
  }
}
```

## 🎮 Usage

### Dashboard
- **View Statistics** - Monitor your file organization progress
- **Check Ninja Score** - See your organization level and progress
- **Quick Actions** - Use smart tools for bulk operations
- **Recent Activity** - Track latest file movements

### File Browser
- **Navigate Folders** - Browse organized files by category
- **Open Files** - Click to open files with system default applications
- **Folder Navigation** - Use breadcrumbs and back buttons

### Activity Logs
- **Movement History** - See all file movements with timestamps
- **File Metadata** - View file sizes, types, and tags
- **Search & Filter** - Find specific file movements

## 🎨 UI Design Philosophy

FileNinja's interface is inspired by Nothing OS design principles:

- **Glassmorphism** - Translucent elements with backdrop blur
- **Minimalism** - Clean, uncluttered layouts with purposeful white space
- **Ambient Lighting** - Subtle gradients and glow effects
- **Micro-interactions** - Smooth animations and hover effects
- **Typography** - Inter font family for clean, readable text
- **Color Palette** - Dark backgrounds with cyan accent colors

## 🔧 Technical Details

### Backend
- **Flask** - Lightweight Python web framework
- **SQLite** - Embedded database for file movement logging
- **Watchdog** - Cross-platform file system monitoring
- **Threading** - Non-blocking file operations

### Frontend
- **TailwindCSS** - Utility-first CSS framework
- **Lucide Icons** - Beautiful, consistent icon set
- **Vanilla JavaScript** - No heavy frameworks, pure performance
- **CSS Animations** - Smooth, hardware-accelerated transitions

### File Organization Logic
1. **File Detection** - Monitor watched directories for new files
2. **Type Classification** - Analyze file extensions and MIME types
3. **Smart Naming** - Handle duplicates with intelligent numbering
4. **Database Logging** - Record all movements with metadata
5. **Error Handling** - Graceful handling of locked or inaccessible files

## 🛠️ Development

### Adding New File Types
Edit the `_get_file_type_mapping()` method in `core.py`:

```python
def _get_file_type_mapping(self) -> Dict[str, str]:
    return {
        '.pdf': 'PDFs',
        '.doc': 'Documents',
        '.jpg': 'Images',
        '.mp4': 'Other',  # Add new extensions here
        # ... more mappings
    }
```

### Customizing the Interface
The web interface is in `web/index.html` with:
- **TailwindCSS classes** for rapid styling
- **CSS custom properties** for theme consistency
- **Modular JavaScript functions** for easy feature additions

### Database Schema
FileNinja uses SQLite with these main tables:
- **file_logs** - File movement history
- **app_settings** - Application configuration

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 for Python code
- Use semantic commit messages
- Add tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Nothing Technology** - Design inspiration from Nothing OS
- **TailwindCSS** - Excellent utility-first CSS framework
- **Lucide** - Beautiful open-source icons
- **Flask Community** - Robust web framework and ecosystem

## 📞 Support

- **Issues** - Report bugs or request features via GitHub Issues
- **Discussions** - Join community discussions in GitHub Discussions
- **Documentation** - Check the wiki for detailed guides

---

<div align="center">

**Made with 🥷 by the FileNinja team**

*Transform your file chaos into organized zen with Nothing OS aesthetics*

</div>
