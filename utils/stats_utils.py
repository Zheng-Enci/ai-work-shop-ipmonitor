from utils.file_utils import FileHandler
from typing import Optional
from collections import Counter
from datetime import datetime, timedelta


class ActivateIPData:
    """管理 activate_ip.txt 文件数据的类"""
    
    def __init__(self, file_handler: Optional[FileHandler], file_path: str):
        """
        初始化时读取 activate_ip.txt 文件的全部内容并保存到实例变量中
        
        Args:
            file_handler: 文件处理器实例
            file_path: 文件路径
        """
        self.data = None
        self.file_handler = file_handler
        self.file_path = file_path
        self.load_data()
    
    def load_data(self) -> None:
        """读取 activate_ip.txt 文件的全部内容，保存到实例变量中，如果已存在就覆盖"""
        # 使用线程安全的文件读取
        content = self.file_handler.read_file_content(self.file_path)
        # 按行分割并去除空行
        self.data = [line.strip() for line in content.split('\n') if line.strip()]
    
    def count_ip_occurrences(self) -> Counter:
        """
        统计 self.data 中每个IP出现的次数
        
        Returns:
            Counter: IP出现次数的计数器，键为IP地址，值为出现次数
        """
        ip_counter = Counter()
        
        if self.data is None:
            return ip_counter
        
        # 遍历所有行
        for line in self.data:
            # 按空格分割，第一项是时间戳，后面是IP地址
            parts = line.split()
            if len(parts) < 2:
                continue
            
            # 从第二项开始都是IP地址
            ips = parts[1:]
            for ip in ips:
                ip_counter[ip] += 1
        
        return ip_counter
    
    def count_recent_7d_scans(self) -> int:
        """
        统计最近7天的扫描次数
        
        Returns:
            int: 最近7天的扫描次数（即最近7天内的数据行数）
        """
        if self.data is None:
            return 0
        
        # 计算7天前的时间戳
        seven_days_ago = datetime.now() - timedelta(days = 7)
        cutoff_timestamp = seven_days_ago.timestamp()
        
        scan_count = 0
        
        # 从后往前遍历所有行，统计最近7天的扫描次数（因为时间是按顺序存储的，最新的在最后）
        for line in reversed(self.data):
            # 按空格分割，第一项是时间戳
            parts = line.split()
            if len(parts) < 1:
                continue
            
            try:
                # 解析时间戳
                timestamp = float(parts[0])
                # 如果时间戳在最近7天内，计数+1
                if timestamp >= cutoff_timestamp:
                    scan_count += 1
                else:
                    # 由于数据是按时间顺序存储的，如果当前行不在7天内，更早的行肯定也不在，可以提前退出
                    break
            except (ValueError, IndexError):
                # 如果时间戳格式错误，跳过这一行
                continue
        
        return scan_count
