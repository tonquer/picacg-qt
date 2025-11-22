# CLAUDE.md - AI Assistant Guide for PicACG-Qt

## Project Overview

**PicACG-Qt** (哔咔漫画) is a cross-platform desktop client for a manga/comic reading platform. Built with Python and Qt (PySide6), it provides a full-featured manga reading experience with advanced image processing capabilities.

### Key Information
- **Language**: Python 3.9.13+
- **UI Framework**: PySide6 (Qt6)
- **Primary Purpose**: Comic/manga reading, downloading, and library management
- **Platforms**: Windows (7+), macOS (10.15.7+, including M1/ARM64), Linux
- **License**: See LICENSE file
- **Version**: v1.5.3.1 (as of 2025-11-13)

### Important Context
This is a third-party client application. The project is for technical research purposes only. Be mindful of this context when making changes or suggestions.

---

## Repository Structure

```
picacg-qttext/
├── src/                      # Main source code
│   ├── component/           # Reusable UI components (buttons, dialogs, etc.)
│   ├── config/              # Configuration management
│   ├── db/                  # Database files (SQLite)
│   ├── interface/           # UI definition files (generated from .ui)
│   ├── server/              # API client and request handling
│   ├── task/                # Async task management (download, conversion, etc.)
│   ├── tools/               # Utility modules
│   ├── view/                # Application views/screens
│   ├── start.py             # Application entry point
│   ├── qt_owner.py          # Qt application owner/manager
│   ├── images_rc.py         # Compiled Qt resources (large file)
│   └── requirements*.txt    # Platform-specific dependencies
├── ui/                      # Qt Designer UI files (.ui)
│   └── component/           # Component UI files
├── res/                     # Resources (icons, themes, translations)
│   ├── icon/               # Application icons
│   ├── theme/              # Qt stylesheets (QSS)
│   ├── tr/                 # Translation resources
│   └── images.qrc          # Qt resource collection file
├── script/                  # Build and utility scripts
│   ├── build_ui.py         # Compile .ui to .py
│   ├── build_qrc.py        # Compile .qrc to .py
│   ├── build_translate.py  # Build translations
│   └── build_universal2.py # macOS universal2 build helper
├── translate/               # Translation source files (.ts)
├── example/                 # Example screenshots/GIFs
├── .github/workflows/       # CI/CD pipelines
│   ├── release.yml         # Release builds for all platforms
│   └── CI.yml              # Continuous integration
├── README.md               # Chinese documentation
├── README_EN.md            # English documentation
└── CHANGELOG               # Version history

### Generated/Ignored Files
- `src/images_rc.py` - 13MB+ compiled resource file (regenerated from res/images.qrc)
- `build/`, `dist/` - PyInstaller build outputs
- `__pycache__/`, `*.pyc` - Python bytecode
- `config.ini`, `*.db` - User data and runtime files
```

---

## Architecture Overview

### Design Pattern
The application follows a **Model-View-Controller (MVC)** inspired architecture:

- **View** (`src/view/`): UI screens and user interaction
- **Component** (`src/component/`): Reusable UI widgets
- **Server** (`src/server/`): API communication and data management
- **Task** (`src/task/`): Background operations and async processing
- **Config** (`src/config/`): Application configuration and settings

### Key Modules

#### 1. Views (`src/view/`)
Each subdirectory represents a distinct screen or feature:
- `main/` - Main window and application shell
- `read/` - Comic reading interface
- `info/` - Comic details and metadata
- `download/` - Download management
- `search/` - Search functionality
- `category/` - Category browsing
- `setting/` - Application settings
- `user/` - User profile and authentication
- `convert/` - Format conversion tools
- `chat/`, `chat_new/` - Chat/community features
- `fried/` - Friends/social features
- `game/` - Game-related content
- `nas/` - Network storage integration
- `help/` - Help and documentation
- `tool/` - Utility tools (batch processing, etc.)
- `comment/` - Comment viewing and posting
- `index/` - Home/index screen

#### 2. Components (`src/component/`)
Reusable UI widgets organized by type:
- `box/` - Container widgets
- `button/` - Custom buttons
- `dialog/` - Dialog windows
- `label/` - Text labels
- `layout/` - Layout managers
- `line_edit/` - Text input fields
- `list/` - List widgets
- `progress_bar/` - Progress indicators
- `scroll/`, `scroll_area/` - Scrollable areas
- `tab/` - Tab widgets
- `widget/` - Generic widgets
- `system_tray_icon/` - System tray integration

#### 3. Tasks (`src/task/`)
Background processing modules:
- `task_download.py` - Download management
- `task_waifu2x.py` - Image upscaling with waifu2x
- `task_convert.py`, `task_convert_epub.py`, `task_convert_zip.py` - Format conversion
- `task_http.py` - HTTP requests
- `task_qimage.py` - Image processing
- `task_sql.py` - Database operations
- `task_local.py` - Local file operations
- `task_upload.py` - File upload
- `upload_local.py`, `upload_smb.py`, `upload_webdav.py` - Various upload protocols
- `qt_task.py` - Qt task base class

#### 4. Server (`src/server/`)
API and data layer:
- `server.py` - Main API client
- `req.py` - Request handling
- `res.py` - Response parsing
- `sql_server.py` - Database interface
- `user_handler.py` - User session management

#### 5. Configuration (`src/config/`)
- `config.py` - API endpoints, constants, and app configuration
- `global_config.py` - Global runtime state
- `setting.py` - User settings management

---

## Development Workflows

### Prerequisites
```bash
# Python 3.9.13+ required (3.10 for GitHub Actions)
# For Windows 7: Python 3.8

# Install dependencies (choose based on platform/requirements)
cd src
pip install -r requirements.txt              # Standard (with waifu2x)
pip install -r requirements_nosr.txt         # Without waifu2x
pip install -r requirements_macos.txt        # macOS specific
pip install -r requirements_win7.txt         # Windows 7 specific
```

### Running the Application

```bash
cd src
python start.py
```

**Note**: The application uses a local socket server to prevent multiple instances. If already running, new instances will send a "restart" signal and exit.

### Building UI Files

When modifying UI files in the `ui/` directory:

```bash
cd script
python build_ui.py          # Compile all .ui files to Python
python build_qrc.py         # Compile resource files
python build_translate.py   # Build translation files
```

**Important**: After running `build_qrc.py`, the `src/images_rc.py` file will be regenerated (13MB+). This is expected and should be committed if resources changed.

### Building for Distribution

The project uses **PyInstaller** for packaging. GitHub Actions handle automated builds.

#### Local Build (Windows)
```bash
cd src
pyinstaller -F -w -i icon.ico start.py
```

#### Local Build (macOS)
```bash
cd src
pyinstaller --target-architecture=universal2 --clean --onedir --name PicACG \
    --hidden-import sr_ncnn_vulkan --hidden-import PySide6 \
    --hidden-import config --hidden-import component \
    --hidden-import server --hidden-import task \
    --hidden-import tools --hidden-import view \
    --strip --windowed -i Icon.icns start.py
```

#### GitHub Actions Build
Push a tag to trigger release builds:
```bash
git tag v1.5.4
git push origin v1.5.4
```

Or manually trigger via GitHub Actions workflow_dispatch with specific platform options.

### Testing

```bash
cd src/test
# Run test files (specific tests to be determined by examining test directory)
```

---

## Key Dependencies

### Core Dependencies
- **PySide6 (6.5.3)** - Qt6 Python bindings for UI
- **httpx** - Modern HTTP client with HTTP/2 and SOCKS support
- **websocket-client (0.59.0)** - WebSocket communication
- **pillow** - Image processing
- **Pysocks** - SOCKS proxy support
- **lxml** - XML/HTML parsing
- **natsort** - Natural sorting
- **tqdm** - Progress bars

### Optional/Platform-Specific
- **sr-vulkan** - Vulkan-based super-resolution (waifu2x)
  - `sr-vulkan-model-waifu2x`
  - `sr-vulkan-model-realcugan`
  - `sr-vulkan-model-realesrgan`
- **webdavclient3** - WebDAV support
- **pysmb** - SMB/CIFS file sharing

### Build Dependencies
- **PyInstaller** - Application packaging
- **nuitka** - Alternative Python compiler (used for some builds)
- **upx** - Executable compression

---

## Code Conventions

### Python Style
- **Encoding**: UTF-8 with BOM in some files (`# -*- coding: utf-8 -*-`)
- **Naming**:
  - Classes: PascalCase (e.g., `MainView`, `QtOwner`)
  - Functions/Methods: PascalCase (e.g., `SetApp`, `OnNewConnection`)
  - Variables: camelCase or snake_case (mixed throughout codebase)
  - Constants: UPPER_SNAKE_CASE (e.g., `BaseUrl`, `ThreadNum`)
- **Imports**: Organized but not strictly ordered
- **Docstrings**: Minimal; some Chinese comments throughout

### Qt Conventions
- UI files use Qt Designer format (.ui)
- Compiled UI modules in `src/interface/` prefixed with `ui_`
- Resources compiled to `src/images_rc.py` from `res/images.qrc`
- Signal/slot connections typically in view initialization

### File Organization
- One class per file generally preferred
- View classes match their directory name
- UI files in `ui/` mirror view structure in `src/view/`

### Configuration Management
- **DO NOT** hardcode values; use `src/config/config.py`
- API endpoints, URLs, and constants defined in `config.py`
- User settings managed through `Setting` class in `config/setting.py`
- Runtime state in `config/global_config.py`

### Error Handling
- Custom error dialogs: `qt_error.py` (`showError`, `showError2`)
- Logging via `tools.log.Log` class
- Exceptions caught at application level in `start.py`

### Threading
- Use Qt's signal/slot mechanism for thread communication
- Task-based async operations in `src/task/` modules
- Thread pool configuration in `config.py` (`ThreadNum`, `DownloadThreadNum`)

---

## Critical Areas to Understand

### 1. Application Initialization (`src/start.py`)
- Sets up logging, settings, Qt application
- Checks for single instance via QLocalSocket
- Initializes waifu2x if available (graceful degradation if not)
- Loads main view and starts event loop
- Global exception handler installed

### 2. Resource Management
- Large `images_rc.py` file contains all embedded images
- Must be imported before Qt widgets to register resources
- Regenerate with `script/build_qrc.py` after modifying `res/images.qrc`

### 3. Database (`src/db/`)
- SQLite database: `book.db`
- Downloaded from GitHub releases during build
- Managed via `server/sql_server.py` (DbBook class)
- Contains book metadata and user data

### 4. Waifu2x Integration
- Optional image super-resolution feature
- Vulkan-based, requires GPU support
- Graceful fallback if unavailable (`config.CanWaifu2x = False`)
- Models: waifu2x, RealCUGAN, RealESRGAN
- Configuration in `task/task_waifu2x.py`

### 5. API Communication (`src/server/`)
- Base URL and endpoints in `config/config.py`
- Request signing with ApiKey
- Multiple domain support for failover
- Proxy and CDN configuration supported
- HTTP/2 and SOCKS proxy via httpx

### 6. Multi-language Support
- Translation files in `translate/` (.ts format)
- `str_en.ts`, `str_hk.ts` - String translations
- `ui_en.ts`, `ui_hk.ts` - UI translations
- Qt Linguist format
- Compiled via `script/build_translate.py`

---

## Common Tasks for AI Assistants

### Adding a New Feature
1. **Understand existing patterns**: Review similar features in `src/view/`
2. **Create UI** (if needed):
   - Design in Qt Designer, save to `ui/`
   - Run `script/build_ui.py` to generate Python code
3. **Implement view**:
   - Create new directory in `src/view/` if major feature
   - Inherit from appropriate base widget
   - Connect signals/slots
4. **Add task handler** (if async operation):
   - Create task class in `src/task/`
   - Use Qt signals for completion/progress
5. **Update configuration**:
   - Add constants to `config/config.py`
   - Add settings to `config/setting.py` if user-configurable
6. **Test** across platforms if possible

### Fixing Bugs
1. **Check logs**: Application uses `tools.log.Log`
2. **Reproduce**: Understand the workflow triggering the bug
3. **Identify affected modules**: Likely in views, tasks, or server
4. **Fix and test**: Ensure no regressions in related features
5. **Update CHANGELOG**: Document the fix

### Modifying UI
1. **Never edit `src/interface/ui_*.py` directly** - these are generated
2. **Edit corresponding `.ui` file** in `ui/` directory
3. **Rebuild**: Run `python script/build_ui.py`
4. **Commit both** `.ui` and generated `.py` files

### Updating Dependencies
1. **Modify appropriate `requirements*.txt`** in `src/`
2. **Test locally** before committing
3. **Update GitHub Actions** if build process affected
4. **Document** in CHANGELOG if user-visible changes

### Performance Optimization
- **Image loading**: Check `PreLoading`, `PreLook` settings in `config.py`
- **Threading**: Adjust `ThreadNum`, `DownloadThreadNum` constants
- **Caching**: Managed via `IsUseCache`, `CachePathDir` in `config.py`
- **Database queries**: Optimize in `server/sql_server.py`

---

## Platform-Specific Considerations

### Windows
- **Windows 7**: Use Python 3.8 and `requirements_win7.txt`
- **Windows 10+**: Python 3.10, standard requirements
- **Dependencies**: May require VC Runtime and Vulkan Runtime for waifu2x
- **Build**: Single executable with UPX compression

### macOS
- **Universal2**: Builds for both Intel and Apple Silicon
- **Script**: `build_universal2.py` creates fat wheels for dependencies
- **Packaging**: Creates .dmg with create-dmg tool
- **Icon**: Uses .icns format in `res/icon/Icon.icns`
- **Code signing**: Extended attributes cleared with xattr

### Linux
- **Dependencies**: May need xcb-util library
- **Vulkan**: Install mesa-vulkan-drivers for waifu2x
- **Build**: tar.gz or 7z archive
- **ARM64**: Special Docker-based build process with Nuitka

---

## Build System Details

### GitHub Actions Workflows

#### `release.yml` - Release Builds
- **Trigger**: Git tag push or manual workflow_dispatch
- **Platforms**:
  - macOS (universal2): with and without waifu2x
  - Windows x64: with and without waifu2x
  - Windows 7 x64: with and without waifu2x
  - Linux ARM64: without waifu2x only
- **Artifacts**: .dmg (macOS), .7z (Windows/Linux)
- **Database**: Downloads `book.db` from bika-robot/picacg-database releases
- **Compression**: UPX for executables, 7z for archives

#### `CI.yml` - Continuous Integration
- Automated testing on commits (details in CI.yml)

### PyInstaller Configuration
- **Entry point**: `src/start.py`
- **Mode**: Onedir (macOS), onefile (Windows)
- **Hidden imports**: PySide6, sr_ncnn_vulkan, all src modules
- **Resources**: Database copied to dist directory
- **Icons**: Platform-specific (icon.ico for Windows, Icon.icns for macOS)
- **Strip**: Enabled to reduce size

---

## Important Files and Their Roles

| File/Directory | Purpose | Edit Frequency |
|---|---|---|
| `src/start.py` | Application entry point | Rare |
| `src/qt_owner.py` | App-wide Qt object manager | Rare |
| `src/config/config.py` | URLs, constants, API config | Occasional |
| `src/config/setting.py` | User settings schema | Occasional |
| `src/server/server.py` | Main API client | Occasional |
| `src/view/*` | Feature implementations | Frequent |
| `src/component/*` | Reusable UI components | Moderate |
| `src/task/*` | Background operations | Moderate |
| `ui/*.ui` | UI designs | Frequent |
| `src/interface/ui_*.py` | Generated UI code | Never (auto-generated) |
| `src/images_rc.py` | Compiled resources | Never (auto-generated) |
| `res/images.qrc` | Resource manifest | Occasional |
| `requirements*.txt` | Dependencies | Rare |
| `.github/workflows/*.yml` | CI/CD pipelines | Rare |
| `CHANGELOG` | Version history | Frequent |

---

## Security and Privacy Considerations

### Authentication
- User credentials handled in `src/server/user_handler.py`
- Session management via API tokens
- **NEVER** log sensitive information

### Network Communication
- API requests signed with ApiKey (in `config.py`)
- HTTPS for all API calls
- Proxy support for regions with access restrictions
- **DO NOT** expose API keys or user tokens in logs/errors

### Local Data
- User data stored in local SQLite database
- Downloaded comics in configurable directory (`SavePathDir`)
- Cache in separate directory (`CachePathDir`)
- **Config.ini** contains user preferences, may include sensitive settings

### Content Considerations
- This is a client for adult-oriented content platform
- Be mindful of content policy implications when working on display/caching features

---

## Troubleshooting Common Issues

### Waifu2x Not Working
1. Check if Vulkan is available: GPU drivers installed
2. Verify `config.CanWaifu2x` flag in runtime
3. Windows: Install VC Runtime and Vulkan Runtime
4. Linux: Install mesa-vulkan-drivers
5. Fallback: Use `requirements_nosr.txt` version without super-resolution

### UI Not Updating After Changes
1. Ensure `.ui` file was saved
2. Run `python script/build_ui.py`
3. Restart application (Python caches imports)
4. Check for errors in generated `src/interface/ui_*.py`

### Build Failures
1. Check Python version matches target platform
2. Verify all dependencies installed
3. Review PyInstaller hidden imports
4. Check UPX availability and version
5. Ensure database download succeeded

### Network/Proxy Issues
1. Check proxy settings in application
2. Verify API domain accessibility
3. Try alternative domains (configured in `config.py`)
4. Check firewall/antivirus blocking

### Database Errors
1. Ensure `db/book.db` exists
2. Check file permissions
3. Verify database version compatibility
4. Re-download from releases if corrupted

---

## Git Workflow

### Branch Strategy
- **main/master**: Stable releases
- **Feature branches**: Named descriptively
- **AI assistant branches**: Prefix with `claude/` (as per git operations requirements)

### Commit Messages
- Clear, descriptive messages
- Reference issue numbers when applicable
- Chinese or English both acceptable (codebase is mixed)

### Pull Requests
- Test on target platform before submitting
- Update CHANGELOG for user-facing changes
- Include screenshots for UI changes
- Ensure CI passes

---

## Testing Guidelines

### Manual Testing Checklist
- [ ] Application launches without errors
- [ ] Login/authentication works
- [ ] Browsing and search functional
- [ ] Comic reading and page navigation
- [ ] Download and local library management
- [ ] Waifu2x upscaling (if enabled)
- [ ] Settings save and persist
- [ ] Multi-language switching

### Platform Testing
- Test on target platforms when possible
- Use GitHub Actions for cross-platform builds
- Check platform-specific features (system tray, file dialogs)

### Performance Testing
- Large library handling (1000+ comics)
- Memory usage during long sessions
- Download performance with many concurrent downloads
- Image loading speed in reading view

---

## Documentation Standards

### Code Comments
- Use English or Chinese (codebase uses both)
- Comment complex algorithms and business logic
- Document API expectations and data formats
- Explain non-obvious UI behavior

### Docstrings
- Not consistently used in current codebase
- When adding new modules, consider adding docstrings
- Follow PEP 257 if adding docstrings

### External Documentation
- Update README.md/README_EN.md for user-facing changes
- Update CHANGELOG for all releases
- Update this CLAUDE.md for architectural changes

---

## Resources and References

### Project Links
- **GitHub**: https://github.com/tonquer/picacg-qt
- **Issues**: https://github.com/tonquer/picacg-qt/issues
- **Releases**: https://github.com/tonquer/picacg-qt/releases
- **Database**: https://github.com/bika-robot/picacg-database

### Dependencies Documentation
- **PySide6**: https://doc.qt.io/qtforpython/
- **PyInstaller**: https://pyinstaller.readthedocs.io/
- **waifu2x**: https://github.com/nagadomi/waifu2x
- **sr-vulkan**: https://github.com/tonquer/waifu2x-vulkan

### Related Projects
- **JMComic-qt**: https://github.com/tonquer/JMComic-qt
- **ehentai-qt**: https://github.com/tonquer/ehentai-qt

---

## Final Notes for AI Assistants

### What to Prioritize
1. **Code quality**: Maintain consistency with existing patterns
2. **User experience**: This is a GUI application - UX matters
3. **Cross-platform compatibility**: Test or note platform-specific changes
4. **Performance**: Image-heavy application, optimize where possible
5. **Documentation**: Keep CHANGELOG and this file updated

### What to Avoid
1. **Breaking changes**: This is a user-facing application
2. **Hardcoded values**: Use configuration system
3. **Direct .py edits** of generated UI files
4. **Ignoring existing architecture**: Follow established patterns
5. **Security issues**: Handle credentials and API keys carefully

### When in Doubt
1. Check similar existing implementations
2. Review issue tracker for known problems
3. Test on multiple platforms if possible
4. Ask for clarification before major architectural changes
5. Document assumptions and decisions

---

**Last Updated**: 2025-11-22
**For**: Claude and other AI assistants working with this codebase
**Maintainer**: Update this file when making significant architectural changes
