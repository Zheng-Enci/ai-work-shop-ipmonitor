from flask import Flask, render_template
from utils.network_scanner import NetworkScanner
from utils.stats_utils import ActivateIPData
from utils.file_utils import FileHandler
from utils.admin_utils import AdminChecker
from config import Config

# 确保以管理员身份运行
AdminChecker.ensure_admin()

app = Flask(__name__)

# 创建文件处理器实例（用于文件操作）
file_handler = FileHandler(file_path = Config.ACTIVATE_IP_FILE_PATH)

# 创建 ActivateIPData 实例
activate_ip_data = ActivateIPData(
    file_handler = file_handler, file_path = Config.ACTIVATE_IP_FILE_PATH
)

# 网络扫描器实例（使用同一个文件处理器实例）
NetworkScanner(file_handler = file_handler, file_path = Config.ACTIVATE_IP_FILE_PATH)

@app.route('/')
def index():
    """
    首页路由，渲染IP统计页面
    
    Returns:
        渲染后的HTML页面，包含IP统计信息
    """
    # 每次请求时重新加载数据
    activate_ip_data.load_data()
    
    return render_template(
        'index.html',
        ip_range = Config.IP_RANGE,  # IP范围（151-250）
        ip_counter = activate_ip_data.count_ip_occurrences(),  # IP出现次数统计
        fang_ips = Config.FANG_IPS,  # 坊内IP列表
        recent_7d_scans = activate_ip_data.count_recent_7d_scans()  # 最近7天扫描次数
    )

if __name__ == '__main__':
    app.run(host = Config.FLASK_HOST, port = Config.FLASK_PORT, debug = Config.FLASK_DEBUG)
