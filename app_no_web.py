"""
AiWorkShop IP 监控系统 - 无 Web 界面版本
"""

import time
from utils.network_scanner import NetworkScanner
from utils.file_utils import FileHandler
from config import Config


# 创建文件处理器实例
file_handler = FileHandler(file_path=Config.ACTIVATE_IP_FILE_PATH)

# 启动网络扫描器（自动在后台线程执行定时扫描）
NetworkScanner(file_handler = file_handler, file_path=Config.ACTIVATE_IP_FILE_PATH)

# 保持程序运行
while True:
    time.sleep(60)
