"""
AiWorkShop IP 监控系统 - 无 Web 界面版本

这是一个纯后台运行的 IP 监控程序，不包含 Flask Web 服务器功能。
程序启动后会自动在后台执行定时网络扫描任务，将结果保存到 activate_ip.txt 文件中。

使用方法:
    python run.py

功能说明:
    - 自动扫描指定 IP 范围（10.0.48.151-250）
    - 每 60 秒执行一次扫描（可在 config.py 中配置）
    - 扫描结果保存到 activate_ip.txt 文件
    - 支持通过 stats_cli.py 查看统计信息

作者: 郑恩赐、陈堉坤、苏静铷
许可证: MIT
"""

import time
import signal
import sys
from utils.network_scanner import NetworkScanner
from utils.file_utils import FileHandler
from config import Config


# 全局变量，用于控制程序运行状态
running = True


def signal_handler(signum, frame):
    """
    信号处理函数，用于优雅地停止程序
    
    Args:
        signum: 信号编号
        frame: 当前栈帧
    """
    global running
    print("\n收到停止信号，正在关闭程序...")
    running = False


def main():
    """
    主函数，初始化并启动 IP 监控系统
    
    该函数会:
    1. 注册信号处理器，支持 Ctrl+C 优雅退出
    2. 创建文件处理器实例
    3. 启动网络扫描器（自动在后台线程执行定时扫描）
    4. 保持主线程运行，等待用户中断
    """
    global running
    
    # 注册信号处理器，支持 Ctrl+C 优雅退出
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("=" * 60)
    print("AiWorkShop IP 监控系统 - 无 Web 界面版本")
    print("=" * 60)
    print(f"扫描间隔: {Config.SCAN_INTERVAL} 秒")
    print(f"数据文件: {Config.ACTIVATE_IP_FILE_PATH}")
    print(f"监控范围: 10.0.48.{Config.IP_RANGE[0]}-{Config.IP_RANGE[-1]}")
    print("=" * 60)
    print("程序已启动，按 Ctrl+C 停止...")
    print()
    
    # 创建文件处理器实例
    file_handler = FileHandler(file_path=Config.ACTIVATE_IP_FILE_PATH)
    
    # 启动网络扫描器（自动在后台线程执行定时扫描）
    NetworkScanner(file_handler=file_handler, file_path=Config.ACTIVATE_IP_FILE_PATH)
    
    # 主循环，保持程序运行
    try:
        while running:
            # 每秒检查一次是否需要退出
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    finally:
        print("程序已停止")


if __name__ == '__main__':
    main()
