#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows Defender 文件扫描工具
支持拖拽文件和右键菜单"发送到"功能
"""

import os
import sys
import subprocess
import glob
import shutil
from pathlib import Path
from datetime import datetime

def find_mpcmdrun_path():
    """
    查找 MpCmdRun.exe 的路径
    """
    # 常见的 Windows Defender 路径
    base_paths = [
        r"C:\ProgramData\Microsoft\Windows Defender\Platform",
        r"C:\Program Files\Windows Defender",
        r"C:\Program Files (x86)\Windows Defender"
    ]
    
    for base_path in base_paths:
        if os.path.exists(base_path):
            # 在 Platform 目录下查找版本子目录
            if "Platform" in base_path:
                version_dirs = glob.glob(os.path.join(base_path, "*"))
                for version_dir in version_dirs:
                    if os.path.isdir(version_dir):
                        mpcmdrun_path = os.path.join(version_dir, "MpCmdRun.exe")
                        if os.path.exists(mpcmdrun_path):
                            return mpcmdrun_path
            else:
                # 直接在目录下查找
                mpcmdrun_path = os.path.join(base_path, "MpCmdRun.exe")
                if os.path.exists(mpcmdrun_path):
                    return mpcmdrun_path
    
    # 如果上述路径都找不到，尝试使用 where 命令
    try:
        result = subprocess.run(["where", "MpCmdRun.exe"], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip().split('\n')[0]
    except:
        pass
    
    return None

def scan_file(file_path, mpcmdrun_path, copy_log=True):
    """
    使用 Windows Defender 扫描指定文件
    """
    # 转换为绝对路径
    abs_file_path = os.path.abspath(file_path)
    
    if not os.path.exists(abs_file_path):
        print(f"错误: 文件不存在 - {abs_file_path}")
        return False
    
    print(f"\n要扫描的文件位置: {abs_file_path}")
    print("正在扫描...")
    
    # 构建扫描命令
    cmd = [
        mpcmdrun_path,
        "-Scan",
        "-Scantype", "3",  # 自定义扫描
        "-File", abs_file_path
    ]
    
    try:
        # 执行扫描命令
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print("\n=== 扫描结果 ===")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("错误信息:", result.stderr)
        
        # 检查日志文件
        log_path = os.path.join(os.environ.get('TEMP', ''), 'MpCmdRun.log')
        if os.path.exists(log_path):
            print(f"\n详细日志文件: {log_path}")
            try:
                with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                    log_content = f.read()
                    if log_content.strip():
                        print("\n=== 详细日志 ===")
                        print(log_content)
                        
                # 只有在指定时才复制日志文件
                if copy_log:
                    copy_log_file(log_path)
                        
            except Exception as e:
                print(f"读取日志文件失败: {e}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"执行扫描命令失败: {e}")
        return False

def copy_log_file(log_path):
    """
    复制日志文件到当前目录的Log文件夹，并重命名为带时间戳的格式
    """
    try:
        # 获取当前脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(script_dir, 'Log')
        
        # 创建Log目录（如果不存在）
        os.makedirs(log_dir, exist_ok=True)
        
        # 生成带时间戳的文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_log_name = f'MpCmdRun_{timestamp}.log'
        new_log_path = os.path.join(log_dir, new_log_name)
        
        # 复制文件
        shutil.copy2(log_path, new_log_path)
        print(f"\n日志文件已复制到: {new_log_path}")
        
    except Exception as e:
        print(f"\n复制日志文件失败: {e}")

def create_sendto_shortcut():
    """
    在脚本目录创建bat文件，在SendTo文件夹中创建lnk快捷方式
    """
    try:
        import win32com.client
        
        # 获取当前脚本的完整路径和目录
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)
        
        # 在脚本目录下创建bat文件
        bat_name = "Windows Defender 扫描.bat"
        bat_path = os.path.join(script_dir, bat_name)
        script_name = os.path.basename(script_path)
        
        bat_content = f'''@echo off
chcp 65001 > nul
python "{script_name}" %*
pause
'''
        
        with open(bat_path, 'w', encoding='utf-8') as f:
            f.write(bat_content)
        
        print(f"已创建批处理文件: {bat_path}")
        
        # 获取 SendTo 文件夹路径
        sendto_path = os.path.join(os.environ['APPDATA'], 
                                  'Microsoft', 'Windows', 'SendTo')
        
        if not os.path.exists(sendto_path):
            print(f"SendTo 文件夹不存在: {sendto_path}")
            return False
        
        # 创建lnk快捷方式
        shortcut_name = "Windows Defender 扫描.lnk"
        shortcut_path = os.path.join(sendto_path, shortcut_name)
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = bat_path
        shortcut.WorkingDirectory = script_dir
        shortcut.IconLocation = bat_path
        shortcut.save()
        
        print(f"已创建 SendTo 快捷方式: {shortcut_path}")
        print("现在可以通过右键菜单 -> 发送到 -> Windows Defender 扫描 来使用此功能")
        return True
        
    except ImportError:
        print("错误: 需要安装 pywin32 库来创建快捷方式")
        print("请运行: pip install pywin32")
        return False
    except Exception as e:
        print(f"创建快捷方式失败: {e}")
        return False

def check_shortcuts_exist():
    """
    检查bat文件和lnk快捷方式是否存在
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bat_path = os.path.join(script_dir, "Windows Defender 扫描.bat")
    
    sendto_path = os.path.join(os.environ['APPDATA'], 
                              'Microsoft', 'Windows', 'SendTo')
    lnk_path = os.path.join(sendto_path, "Windows Defender 扫描.lnk")
    
    return os.path.exists(bat_path) and os.path.exists(lnk_path)

def main():
    print("Windows Defender 文件扫描工具")
    print("=" * 40)
    
    # 查找 MpCmdRun.exe
    mpcmdrun_path = find_mpcmdrun_path()
    if not mpcmdrun_path:
        print("错误: 无法找到 MpCmdRun.exe")
        print("请确保 Windows Defender 已正确安装")
        input("按回车键退出...")
        return
    
    print(f"MpCmdRun.exe 位置: {mpcmdrun_path}")
    
    # 检查命令行参数
    if len(sys.argv) < 2:
        print("使用方法:")
        print("1. 将文件拖拽到此程序上")
        print("2. 运行程序并选择创建 SendTo 快捷方式")
        
        # 检查快捷方式是否已存在
        if check_shortcuts_exist():
            print("\n快捷方式已存在，无需重复创建。")
        else:
            print("\n是否要创建 SendTo 快捷方式? (直接回车默认为yes, n取消): ", end="")
            
            try:
                choice = input().strip().lower()
                # 如果用户直接回车或输入yes相关内容，则创建快捷方式
                if choice == '' or choice in ['y', 'yes', '是']:
                    create_sendto_shortcut()
                elif choice in ['n', 'no', '否']:
                    print("已取消创建快捷方式。")
            except EOFError:
                # 如果是通过管道输入，自动创建快捷方式
                print("y")
                create_sendto_shortcut()
        
        try:
            input("\n按回车键退出...")
        except EOFError:
            pass
        return
    
    # 获取要扫描的文件路径列表（支持多个文件）
    file_paths = sys.argv[1:]
    
    print(f"\n共需要扫描 {len(file_paths)} 个文件")
    
    # 执行扫描，记录结果
    scan_results = []
    for i, file_path in enumerate(file_paths, 1):
        print(f"\n[{i}/{len(file_paths)}] 开始扫描文件...")
        # 扫描时不复制日志文件
        success = scan_file(file_path, mpcmdrun_path, copy_log=False)
        scan_results.append((file_path, success))
    
    # 所有文件扫描完成后，复制最后的日志文件
    print("\n=== 所有文件扫描完成 ===")
    log_path = os.path.join(os.environ.get('TEMP', ''), 'MpCmdRun.log')
    if os.path.exists(log_path):
        copy_log_file(log_path)
    
    # 显示扫描结果汇总
    print("\n=== 扫描结果汇总 ===")
    success_count = 0
    for file_path, success in scan_results:
        status = "成功" if success else "失败"
        print(f"{status}: {file_path}")
        if success:
            success_count += 1
    
    print(f"\n总计: {success_count}/{len(file_paths)} 个文件扫描成功")
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()