import re
import subprocess
import time
import threading
from utils.file_utils import FileHandler
from typing import Optional
from config import Config


class NetworkScanner:
    """网络扫描器类"""
    
    def __init__(self, file_handler: Optional[FileHandler], file_path: str) -> None:
        """
        初始化网络扫描器
        
        Args:
            file_handler: 文件处理器实例（必须与其他类共享同一个实例）
            file_path: 文件路径
        """
        self.file_handler = file_handler
        self.file_path = file_path
        # 使用配置文件中的坊内IP列表，确保与前端显示一致
        self.ai_workshop_own_ip = ["10.0.48." + str(i) for i in Config.FANG_IPS]
        # 使用配置文件中的扫描间隔
        scan_interval = Config.SCAN_INTERVAL
        threading.Thread(
            target = self._periodic_scan,
            args = (scan_interval,),
        ).start()
        print(f"定时任务已启动：每 {scan_interval} 秒自动执行一次网络扫描")

    def _get_all_active_ips(self) -> list:
        """从ARP表中获取所有激活的IP地址"""
        result = subprocess.run(
            ["arp", "-a"],
            capture_output = True,  # capture_output 捕获输出
            text = True,  # text 输出文本
            encoding = 'gbk'  # Windows 中文系统
        )
        # 使用配置文件中的正则表达式
        pattern = Config.IP_PATTERN
        return re.findall(pattern, result.stdout)

    def _ping_ip(self, ip: str) -> None:
        """ping指定的IP地址，用于检测IP是否在线"""
        subprocess.run(
            ["ping", "-n", "1", ip],
            stdout = subprocess.DEVNULL,  # 丢弃标准输出（ ping 的正常结果）
            stderr = subprocess.DEVNULL,  # 丢弃标准错误（ ping 的错误提示，如超时）
            check = False  # 避免 ping 返回非 0 码时抛出异常（可选，但建议加）
        )
    
    def _scan_network(self) -> None:
        """扫描网络，检测激活的IP地址并写入activate_ip.txt"""
        # 清除 arp 缓存
        subprocess.run(
            ["arp", "-d"],
            stdout = subprocess.DEVNULL,  # 丢弃标准输出（ ping 的正常结果）
            stderr = subprocess.DEVNULL,  # 丢弃标准错误（ ping 的错误提示，如超时）
            check = False  # 避免 ping 返回非 0 码时抛出异常（可选，但建议加）
        )
        
        # 并发 ping 所有坊内IP，并保存线程引用
        ping_threads = []
        for ip in self.ai_workshop_own_ip:
            thread = threading.Thread(
                target = self._ping_ip,
                args = (ip,),
            )
            thread.start()
            ping_threads.append(thread)
        # 等待所有ping线程完成
        for thread in ping_threads:
            thread.join()
    
        all_activate_ip = self._get_all_active_ips()
        
        # 构建要写入的内容
        content = str(time.time()) + " "
        for ip in all_activate_ip:
            if ip in self.ai_workshop_own_ip:
                content += ip + " "
        content += "\n"
        
        # 使用线程安全的文件写入
        self.file_handler.write_file(self.file_path, content)

    def _periodic_scan(self, seconds: int) -> None:
        """
        定期执行网络扫描的循环函数，用于在子线程中运行
        
        该函数会先立即执行一次网络扫描，然后每隔指定秒数重复执行扫描。
        此函数设计为在后台线程中运行，实现定时自动扫描功能。
        
        Args:
            seconds: 每次扫描之间的间隔时间（秒）
        
        Note:
            此函数会无限循环执行，通常应在独立的线程中调用
        """
        # 立即执行一次扫描
        self._scan_network()
        time.sleep(seconds)
        # 进入无限循环，定期执行扫描
        while True:
            self._scan_network()
            time.sleep(seconds)