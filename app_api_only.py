"""
AiWorkShop IP 监控系统 - API 版本

提供网络扫描功能和数据查询 API，不包含 Web 页面渲染。
"""

from flask import Flask, jsonify
from utils.network_scanner import NetworkScanner
from utils.file_utils import FileHandler
from config import Config

app = Flask(__name__)

# 创建文件处理器实例
file_handler = FileHandler(file_path=Config.ACTIVATE_IP_FILE_PATH)

# 启动网络扫描器
NetworkScanner(file_handler=file_handler, file_path=Config.ACTIVATE_IP_FILE_PATH)


@app.route('/api/data')
def get_data():
    """
    获取 activate_ip.txt 的原始数据
    
    Returns:
        JSON 格式的 IP 扫描数据
    """
    content = file_handler.read_file_content(Config.ACTIVATE_IP_FILE_PATH)
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    
    data = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 2:
            timestamp = float(parts[0])
            ips = parts[1:]
            data.append({
                'timestamp': timestamp,
                'ips': ips
            })
    
    return jsonify(data)


if __name__ == '__main__':
    app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=Config.FLASK_DEBUG)
