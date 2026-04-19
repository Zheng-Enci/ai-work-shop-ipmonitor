"""
项目配置文件
包含 IP 范围配置和 Flask 运行配置
"""
import os


class Config:
    """项目配置类"""
    
    # 文件路径配置
    # activate_ip.txt 文件路径（相对于项目根目录）
    ACTIVATE_IP_FILE_PATH = os.path.join(os.path.dirname(__file__), 'activate_ip.txt')
    
    # 坊内IP定义
    FANG_IPS = []
    FANG_IPS.extend(range(153, 175))
    FANG_IPS.extend(range(176, 181))
    FANG_IPS.extend(range(185, 191))
    FANG_IPS.extend(range(226, 250))
    
    # 扫描IP范围
    IP_RANGE = list(range(151, 251))
    
    # 网络扫描配置
    SCAN_INTERVAL = 60  # 扫描间隔（秒），默认 60 秒
    IP_PATTERN = "10.0.48.\\d+"  # IP 查找正则表达式，用于从 ARP 表中匹配 IP 地址
    
    # 数据保留配置
    DATA_RETENTION_SECONDS = 2592000  # 数据保留时间（秒），默认 2592000 秒（30天）
    
    # Flask 运行配置
    FLASK_HOST = '0.0.0.0'
    FLASK_PORT = 5000
    FLASK_DEBUG = False
