"""
AiWorkShop IP 监控系统 - API 版本

提供网络扫描功能和数据查询 API，不包含 Web 页面渲染。
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from utils.network_scanner import NetworkScanner
from utils.file_utils import FileHandler
from utils.admin_utils import AdminChecker
from utils.stats_utils import ActivateIPData
from utils.response_utils import APIResponse
from config import Config

# 确保以管理员身份运行
AdminChecker.ensure_admin()

app = Flask(__name__)

# 启用 CORS，允许所有来源访问 API
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# 创建文件处理器实例
file_handler = FileHandler(file_path=Config.ACTIVATE_IP_FILE_PATH)

# 启动网络扫描器
NetworkScanner(file_handler=file_handler, file_path=Config.ACTIVATE_IP_FILE_PATH)

# 创建 ActivateIPData 实例并启动自动清理线程
# 使用同一个 file_handler 实例，确保线程锁机制正常工作
activate_ip_data = ActivateIPData(file_handler=file_handler, file_path=Config.ACTIVATE_IP_FILE_PATH)
activate_ip_data.start_auto_cleanup(
    file_handler=file_handler,
    seconds=Config.DATA_RETENTION_SECONDS,
    interval=Config.AUTO_CLEANUP_INTERVAL
)


@app.route('/api/data', methods=['GET'])
def get_data():
    """
    获取指定时间范围内的 IP 扫描数据
    
    通过 GET 请求传入开始时间戳和结束时间戳，返回该时间范围内的所有数据。
    
    请求参数:
        start_time: 开始时间戳（Unix 时间戳，秒）
        end_time: 结束时间戳（Unix 时间戳，秒）
    
    Returns:
        JSON 格式的 IP 扫描数据列表
    """
    # 获取请求参数
    start_time_str = request.args.get('start_time')
    end_time_str = request.args.get('end_time')
    
    # 参数验证
    if not start_time_str or not end_time_str:
        return jsonify(APIResponse.bad_request(message='缺少必要参数：start_time 和 end_time')), 400
    
    try:
        start_time = float(start_time_str)
        end_time = float(end_time_str)
    except ValueError:
        return jsonify(APIResponse.bad_request(message='时间戳格式错误，必须是数字')), 400
    
    # 使用 ActivateIPData 获取时间范围内的数据
    data = activate_ip_data.get_data_by_time_range(start_time, end_time)
    
    return jsonify(APIResponse.success(data=data, message='查询成功'))


if __name__ == '__main__':
    app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=Config.FLASK_DEBUG)
