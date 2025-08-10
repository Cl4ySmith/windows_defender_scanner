# Windows Defender File Scanner

A Python-based Windows Defender file scanning tool for detecting whether specified files are flagged as malicious by Windows Defender.

> 📋 **中文文档**: For Chinese documentation, please refer to [README.md](README.md)

## Table of Contents

- [Features](#features)
- [Installation and Deployment](#installation-and-deployment)
  - [System Requirements](#system-requirements)
  - [Installation Steps](#installation-steps)
    - [1. Install uv Package Manager](#1-install-uv-package-manager)
    - [2. Verify uv Installation](#2-verify-uv-installation)
    - [3. Clone or Download Project](#3-clone-or-download-project)
    - [4. Create Virtual Environment](#4-create-virtual-environment)
    - [5. Install Project Dependencies](#5-install-project-dependencies)
    - [6. Verify Installation](#6-verify-installation)
- [Usage](#usage)
  - [Initial Setup (Important)](#initial-setup-important)
  - [Method 1: Right-click Menu Scanning (Recommended)](#method-1-right-click-menu-scanning-recommended)
  - [Method 2: Drag & Drop Scanning](#method-2-drag--drop-scanning)
  - [Method 3: Command Line Scanning](#method-3-command-line-scanning)
- [Directory Structure](#directory-structure)
- [Important Notes](#important-notes)
- [Technical Implementation](#technical-implementation)
- [Troubleshooting](#troubleshooting)
  - [Common Issues](#common-issues)
  - [Uninstallation](#uninstallation)
  - [Updates](#updates)
- [File Descriptions](#file-descriptions)
- [Technical Support](#technical-support)

## Features

1. **Auto-detect MpCmdRun.exe Path**: Automatically searches for Windows Defender command-line tool in common locations
2. **Drag & Drop Scanning**: Directly drag files onto the bat program for scanning
3. **Right-click Menu Integration**: Create SendTo shortcuts for scanning via right-click menu "Send to" function
4. **Automatic Log Saving**: Automatically copies log files to Log directory after each scan, named with timestamps for tracking
5. **Smart Shortcut Management**: Automatically detects if shortcuts exist to avoid duplicate creation
6. **Multi-file Support**: Supports scanning multiple files in a single operation

## Installation and Deployment

### System Requirements

- **Operating System**: Windows 10/11
- **Python Version**: Python 3.11 or higher
- **Windows Defender**: Installed and enabled
- **Permissions**: Administrator privileges (required to access Windows Defender command-line tool)

### Installation Steps

#### 1. Install uv Package Manager

**Method 1: PowerShell Installation (Recommended)**

```powershell
# Use official installation script
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Method 2: Install via pip**

```bash
pip install uv
```

**Method 3: Download Pre-compiled Binary**

1. Visit [uv GitHub Releases](https://github.com/astral-sh/uv/releases)
2. Download the latest version for Windows
3. Add the executable to system PATH

#### 2. Verify uv Installation

```powershell
uv --version
```

#### 3. Clone or Download Project

```bash
# If using Git
git clone <repository-url>
cd windows-defender-scanner

# Or download and extract project files directly
```

#### 4. Create Virtual Environment

```bash
# Execute in project root directory
uv venv
```

This will create a `.venv` folder in the project directory.

#### 5. Install Project Dependencies

```bash
# Sync install all dependencies
uv sync
```

This will automatically install all dependencies defined in `pyproject.toml`, including:
- `pywin32>=311`: For creating Windows shortcuts

#### 6. Verify Installation

```bash
# Test if the program runs normally
uv run python windows_defender_scanner.py
```

## Usage

### Initial Setup (Important)

Before first use, it's recommended to run the program once for initialization:

```bash
# Use uv to run (recommended)
uv run python windows_defender_scanner.py

# Or use Python directly
python windows_defender_scanner.py
```

The program will ask whether to create SendTo shortcuts. **It's recommended to choose "Yes"** (press Enter or type `y`), which will:
- Create `Windows Defender 扫描.bat` batch file in the project directory
- Create shortcuts in Windows SendTo folder
- Automatically create `Log` directory for storing scan logs

### Method 1: Right-click Menu Scanning (Recommended)

After completing initial setup, you can quickly scan via right-click menu:
1. Right-click on any file
2. Select "Send to" → "Windows Defender 扫描"
3. The program will automatically open and start scanning

### Method 2: Drag & Drop Scanning

1. Drag files onto the `Windows Defender 扫描.bat` file
2. The program will automatically call Windows Defender for scanning
3. Supports multiple file selection for batch scanning

### Method 3: Command Line Scanning

```bash
# Single file scanning
uv run python windows_defender_scanner.py "file_path"

# Multiple files scanning
uv run python windows_defender_scanner.py "file1_path" "file2_path" "file3_path"

# Or use Python directly
python windows_defender_scanner.py "file_path"
```

## Directory Structure

After deployment, the project directory structure is as follows:

```
windows-defender-scanner/
├── .venv/                          # Virtual environment directory
├── Log/                            # Scan log directory
│   ├── MpCmdRun_20240101_120000.log
│   └── ...
├── Windows Defender 扫描.bat        # Batch call file
├── windows_defender_scanner.py     # Main program
├── pyproject.toml                  # Project configuration
├── uv.lock                         # Dependency lock file
├── README.md                       # Chinese documentation
├── README_EN.md                    # English documentation (this file)
└── DEPLOY.md                       # Deployment guide
```

## Important Notes

⚠️ **Important Reminders**:
- **Administrator Privileges**: The program requires administrator privileges to access Windows Defender command-line tool
- **First Run**: It's recommended to create shortcuts on first run for more convenient subsequent use
- **Log Saving**: Logs are automatically saved to the `Log` directory after each scan, with filenames containing timestamps
- **Shortcut Detection**: The program automatically detects if shortcuts already exist to avoid duplicate creation
- **Windows Defender**: Ensure Windows Defender is installed and running normally
- **Multi-file Support**: The program now supports scanning multiple files in a single operation

## Technical Implementation

- **Path Detection**: Automatically searches for MpCmdRun.exe in multiple possible locations
- **Absolute Path Processing**: Ensures absolute paths are passed to the scanning program
- **Log Display**: Shows scan results and detailed log information
- **Log Saving**: Automatically copies MpCmdRun.log to local Log directory, with filename format MpCmdRun_YYYYMMDD_HHMMSS.log
- **SendTo Integration**: Implements right-click menu integration through batch files and shortcuts
- **Relative Path Calling**: Batch file uses relative paths to call Python scripts for better portability
- **Batch Processing**: Supports multiple file scanning with progress tracking and result summary

## Troubleshooting

### Common Issues

1. **Cannot find MpCmdRun.exe**
   - Ensure Windows Defender is installed and enabled
   - Run the program with administrator privileges

2. **pywin32 import error**
   - Ensure dependencies are correctly installed: `uv sync`
   - Check if virtual environment is activated

3. **Insufficient permissions**
   - Run PowerShell or Command Prompt with administrator privileges
   - Ensure you have permission to access SendTo folder

4. **Batch file cannot run**
   - Check if Python is in system PATH
   - Ensure `windows_defender_scanner.py` file exists

5. **Multiple file scanning issues**
   - Ensure all file paths are valid
   - Check if files are accessible and not locked by other processes

### Uninstallation

To uninstall, follow these steps:

1. Delete SendTo shortcut:
   ```powershell
   Remove-Item "$env:APPDATA\Microsoft\Windows\SendTo\Windows Defender 扫描.lnk"
   ```

2. Delete project directory:
   ```bash
   rm -rf windows-defender-scanner
   ```

### Updates

Update project to latest version:

```bash
# Pull latest code (if using Git)
git pull

# Update dependencies
uv sync
```

## File Descriptions

- `windows_defender_scanner.py`: Main program file
- `Windows Defender 扫描.bat`: Batch file for right-click menu invocation
- `Log/`: Log file directory, stores historical logs of each scan
  - `MpCmdRun_YYYYMMDD_HHMMSS.log`: Scan log files named with timestamps
- `README.md`: Chinese documentation
- `README_EN.md`: English documentation (this file)
- `pyproject.toml`: Project configuration file

## Technical Support

If you encounter issues, please check:
1. Windows Defender service status
2. Python and uv version compatibility
3. System permission settings
4. Firewall and security software settings

---

**Note**: This tool requires administrator privileges to properly access Windows Defender command-line tool. Please ensure to run as administrator on first use.