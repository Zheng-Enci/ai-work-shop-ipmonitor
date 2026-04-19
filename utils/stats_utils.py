from utils.file_utils import FileHandler
from typing import Optional
from collections import Counter
from datetime import datetime, timedelta


class ActivateIPData:
    """管理 activate_ip.txt 文件数据的类"""
    
    def __init__(self, file_handler: Optional[FileHandler], file_path: str):
        """
        初始化
        
        Args:
            file_handler: 文件处理器实例
            file_path: 文件路径
        """
        self.file_handler = file_handler
        self.file_path = file_path
    
    def _load_data(self) -> list:
        """
        读取 activate_ip.txt 文件的全部内容
        
        Returns:
            list: 文件内容按行分割后的列表
        """
        content = self.file_handler.read_file_content(self.file_path)
        return [line.strip() for line in content.split('\n') if line.strip()]
    
    def count_ip_occurrences(self) -> Counter:
        """
        统计 activate_ip.txt 中每个IP出现的次数
        
        Returns:
            Counter: IP出现次数的计数器，键为IP地址，值为出现次数
        """
        ip_counter = Counter()
        data = self._load_data()
        
        # 遍历所有行
        for line in data:
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
        data = self._load_data()
        
        # 计算7天前的时间戳
        seven_days_ago = datetime.now() - timedelta(days = 7)
        cutoff_timestamp = seven_days_ago.timestamp()
        
        scan_count = 0
        
        # 从后往前遍历所有行，统计最近7天的扫描次数（因为时间是按顺序存储的，最新的在最后）
        for line in reversed(data):
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
