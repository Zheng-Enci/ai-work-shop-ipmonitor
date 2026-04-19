"""
自动安装 Python 依赖包脚本
使用多线程并行安装，并显示美观的进度条
"""
import os
import sys
import threading
import time

# 指定的 Python 版本
python_version = "3.13"

# 检查 Python 版本
current_version = f"{sys.version_info.major}.{sys.version_info.minor}"
if current_version != python_version:
    print(f"警告：当前 Python 版本为 {current_version}，但项目指定版本为 {python_version}")
    print("可能存在的问题：")
    print("  - 某些包可能不兼容当前 Python 版本")
    print("  - 安装过程中可能出现依赖冲突")
    print("  - 运行时可能出现语法或功能错误")
    print(f"  - 建议使用 Python {python_version} 以确保最佳兼容性")

    user_input = input("是否继续安装？(y/n): ").strip().lower()
    if user_input != "y":
        print("安装已取消")
        sys.exit(0)

# 配置下载源（使用清华镜像源加速下载）
download_source = "https://pypi.tuna.tsinghua.edu.cn/simple"

# 需要安装的包列表（包含所有依赖包及指定版本号）
packages = [
    "flask==3.1.2",           # Flask Web 框架
    "flask_cors==6.0.2",      # Flask CORS 跨域支持
    "apscheduler==3.11.1",    # APScheduler 定时任务调度器
    "werkzeug==3.1.4",        # Werkzeug WSGI 工具库
    "jinja2==3.1.6",          # Jinja2 模板引擎
    "markupsafe==3.0.3",      # MarkupSafe HTML 转义库
    "itsdangerous==2.2.0",    # itsdangerous 安全签名库
    "click==8.3.1",           # Click 命令行工具库
    "blinker==1.9.0",         # Blinker 信号库
    "tzlocal==5.3.1",         # tzlocal 时区库
    "tzdata==2025.2",         # tzdata 时区数据
]

# 为每个包创建线程并行安装
for package in packages:
    # 构建 pip 安装命令（>nul 2>&1 用于隐藏所有输出）
    install_cmd = f"pip install {package}"
    if download_source:
        install_cmd += f" -i {download_source}"
    install_cmd += " >nul 2>&1"  # 隐藏标准输出和错误输出
    
    # 在新线程中执行安装命令
    threading.Thread(
        target = os.system,
        args = (install_cmd,),
    ).start()

# 显示进度条，直到所有安装线程完成
while True:
    # 计算已完成和剩余的包数量
    completed = len(packages) - threading.active_count() + 1
    remaining = threading.active_count() - 1
    
    # 计算安装进度（0.0 到 1.0）
    progress = completed / len(packages) 
    
    # 构建进度条：已完成部分使用实心块，未完成部分使用浅色块
    progress_bar = "█" * completed + "░" * remaining
    
    # 计算百分比
    percentage = progress * 100
    
    # 输出进度条：\r 回到行首，\033[K 清除行尾，显示当前进度、进度条和百分比
    print(f"\r\033[K正在安装: {completed}/{len(packages)} [{progress_bar}] {percentage:.2f}%", end = "", flush = True)

    if threading.active_count() == 1:
        break
    
    # 短暂休眠，降低 CPU 占用
    time.sleep(0.1)

# 安装完成后换行，使输出更清晰
print()
print("安装完成！")
