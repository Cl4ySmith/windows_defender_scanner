# Windows Defender 文件扫描工具

这是一个基于 Python 的 Windows Defender 文件扫描工具，用于扫描指定文件是否被 Windows Defender 检测为恶意文件。

> 📋 **English Documentation**: For English documentation, please refer to [README_EN.md](README_EN.md)

## 目录

- [功能特性](#功能特性)
- [安装和部署](#安装和部署)
  - [系统要求](#系统要求)
  - [安装步骤](#安装步骤)
    - [1. 安装 uv 包管理器](#1-安装-uv-包管理器)
    - [2. 验证 uv 安装](#2-验证-uv-安装)
    - [3. 克隆或下载项目](#3-克隆或下载项目)
    - [4. 创建虚拟环境](#4-创建虚拟环境)
    - [5. 安装项目依赖](#5-安装项目依赖)
    - [6. 验证安装](#6-验证安装)
- [使用方法](#使用方法)
  - [首次设置（重要）](#首次设置重要)
  - [方法一：右键菜单扫描（推荐）](#方法一右键菜单扫描推荐)
  - [方法二：拖拽扫描](#方法二拖拽扫描)
  - [方法三：命令行扫描](#方法三命令行扫描)
- [目录结构](#目录结构)
- [注意事项](#注意事项)
- [技术实现](#技术实现)
- [故障排除](#故障排除)
  - [常见问题](#常见问题)
  - [卸载](#卸载)
  - [更新](#更新)
- [文件说明](#文件说明)
- [技术支持](#技术支持)

## 功能特性

1. **自动查找 MpCmdRun.exe 路径**：程序会自动在常见位置查找 Windows Defender 命令行工具
2. **拖拽扫描**：可以直接将文件拖拽到 bat 程序上进行扫描
3. **右键菜单集成**：支持创建 SendTo 快捷方式，通过右键菜单"发送到"功能进行扫描
4. **日志自动保存**：每次扫描后自动将日志文件复制到 Log 目录，按时间戳命名便于追踪
5. **智能快捷方式管理**：自动检测快捷方式是否存在，避免重复创建
6. **多文件支持**：支持一次扫描多个文件，提高工作效率

## 安装和部署

### 系统要求

- **操作系统**：Windows 10/11
- **Python 版本**：Python 3.11 或更高版本
- **Windows Defender**：已安装并启用
- **权限**：管理员权限（用于访问 Windows Defender 命令行工具）

### 安装步骤

#### 1. 安装 uv 包管理器

**方法一：使用 PowerShell 安装（推荐）**

```powershell
# 使用官方安装脚本
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**方法二：使用 pip 安装**

```bash
pip install uv
```

**方法三：下载预编译二进制文件**

1. 访问 [uv GitHub Releases](https://github.com/astral-sh/uv/releases)
2. 下载适合 Windows 的最新版本
3. 将可执行文件添加到系统 PATH

#### 2. 验证 uv 安装

```powershell
uv --version
```

#### 3. 克隆或下载项目

```bash
# 如果使用 Git
git clone <repository-url>
cd windows-defender-scanner

# 或者直接下载并解压项目文件
```

#### 4. 创建虚拟环境

```bash
# 在项目根目录下执行
uv venv
```

这将在项目目录下创建 `.venv` 文件夹。

#### 5. 安装项目依赖

```bash
# 同步安装所有依赖
uv sync
```

这将自动安装 `pyproject.toml` 中定义的所有依赖包，包括：
- `pywin32>=311`：用于创建 Windows 快捷方式

#### 6. 验证安装

```bash
# 测试程序是否正常运行
uv run python windows_defender_scanner.py
```

## 使用方法

### 首次设置（重要）

在开始使用前，建议先运行一次程序进行初始化设置：

```bash
# 使用 uv 运行（推荐）
uv run python windows_defender_scanner.py

# 或直接使用 Python
python windows_defender_scanner.py
```

程序会询问是否创建 SendTo 快捷方式，**建议选择 "是"**（直接回车或输入 `y`），这将：
- 在项目目录下创建 `Windows Defender 扫描.bat` 批处理文件
- 在 Windows SendTo 文件夹中创建快捷方式
- 自动创建 `Log` 目录用于存储扫描日志

### 方法一：右键菜单扫描（推荐）

完成首次设置后，可以通过右键菜单快速扫描：
1. 右键点击任意文件
2. 选择 "发送到" → "Windows Defender 扫描"
3. 程序会自动打开并开始扫描

### 方法二：拖拽扫描

1. 将文件拖拽到 `Windows Defender 扫描.bat` 文件上
2. 程序会自动调用 Windows Defender 进行扫描

### 方法三：命令行扫描

```bash
# 单文件扫描
uv run python windows_defender_scanner.py "文件路径"

# 多文件扫描
uv run python windows_defender_scanner.py "文件1路径" "文件2路径" "文件3路径"

# 或直接使用 Python
python windows_defender_scanner.py "文件路径"
```

## 目录结构

部署完成后，项目目录结构如下：

```
windows-defender-scanner/
├── .venv/                          # 虚拟环境目录
├── Log/                            # 扫描日志目录
│   ├── MpCmdRun_20240101_120000.log
│   └── ...
├── Windows Defender 扫描.bat        # 批处理调用文件
├── windows_defender_scanner.py     # 主程序
├── pyproject.toml                  # 项目配置
├── uv.lock                         # 依赖锁定文件
├── README.md                       # 使用说明文档（本文件）
├── README_EN.md                    # 英文说明文档
└── DEPLOY.md                       # 部署指南
```

## 注意事项

⚠️ **重要提醒**：
- **管理员权限**：程序需要管理员权限才能访问 Windows Defender 命令行工具
- **首次运行**：建议首次运行时创建快捷方式，这样后续使用更加便捷
- **日志保存**：每次扫描后会自动保存日志到 `Log` 目录，文件名包含时间戳
- **快捷方式检测**：程序会自动检测快捷方式是否已存在，避免重复创建
- **Windows Defender**：确保 Windows Defender 已安装并正常运行
- **多文件支持**：程序现在支持一次扫描多个文件，提高工作效率

## 技术实现

- **路径查找**：自动在多个可能的位置查找 MpCmdRun.exe
- **绝对路径处理**：确保传递给扫描程序的是绝对路径
- **日志显示**：显示扫描结果和详细日志信息
- **日志保存**：自动复制 MpCmdRun.log 到本地 Log 目录，文件名格式为 MpCmdRun_YYYYMMDD_HHMMSS.log
- **SendTo 集成**：通过批处理文件和快捷方式实现右键菜单集成
- **相对路径调用**：批处理文件使用相对路径调用 Python 脚本，提高可移植性
- **批量处理**：支持多文件扫描，带进度跟踪和结果汇总

## 故障排除

### 常见问题

1. **找不到 MpCmdRun.exe**
   - 确保 Windows Defender 已安装并启用
   - 以管理员权限运行程序

2. **pywin32 导入错误**
   - 确保已正确安装依赖：`uv sync`
   - 检查虚拟环境是否激活

3. **权限不足**
   - 以管理员权限运行 PowerShell 或命令提示符
   - 确保有权限访问 SendTo 文件夹

4. **批处理文件无法运行**
   - 检查 Python 是否在系统 PATH 中
   - 确保 `windows_defender_scanner.py` 文件存在

5. **多文件扫描问题**
   - 确保所有文件路径都有效
   - 检查文件是否可访问且未被其他进程锁定

### 卸载

如需卸载，请执行以下步骤：

1. 删除 SendTo 快捷方式：
   ```powershell
   Remove-Item "$env:APPDATA\Microsoft\Windows\SendTo\Windows Defender 扫描.lnk"
   ```

2. 删除项目目录：
   ```bash
   rm -rf windows-defender-scanner
   ```

### 更新

更新项目到最新版本：

```bash
# 拉取最新代码（如果使用 Git）
git pull

# 更新依赖
uv sync
```

## 文件说明

- `windows_defender_scanner.py`：主程序文件
- `Windows Defender 扫描.bat`：批处理文件，用于右键菜单调用
- `Log/`：日志文件目录，存储每次扫描的历史日志
  - `MpCmdRun_YYYYMMDD_HHMMSS.log`：按时间戳命名的扫描日志文件
- `README.md`：中文使用说明文档（本文件）
- `README_EN.md`：英文使用说明文档
- `pyproject.toml`：项目配置文件

## 技术支持

如遇到问题，请检查：
1. Windows Defender 服务状态
2. Python 和 uv 版本兼容性
3. 系统权限设置
4. 防火墙和安全软件设置

---

**注意**：本工具需要管理员权限才能正常访问 Windows Defender 命令行工具。首次运行时请确保以管理员身份运行。
