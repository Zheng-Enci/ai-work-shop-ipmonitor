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
    SCAN_INTERVAL = 480  # 扫描间隔（秒），默认 8 分钟 = 480 秒
    IP_PATTERN = "10.0.48.\\d+"  # IP 查找正则表达式，用于从 ARP 表中匹配 IP 地址
    
    # 数据保留配置
    DATA_RETENTION_SECONDS = 6 * 30 * 24 * 60 * 60  # 数据保留时间（秒），6个月 = 6 * 30天 * 24小时 * 60分钟 * 60秒
    AUTO_CLEANUP_INTERVAL = 1 * 24 * 60 * 60  # 自动清理间隔（秒），1天 = 1 * 24小时 * 60分钟 * 60秒
    
    # Flask 运行配置
    FLASK_HOST = '0.0.0.0'
    FLASK_PORT = 5000
    FLASK_DEBUG = False
