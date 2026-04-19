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
    
    def clean_old_data(self, seconds: int = 2592000) -> int:
        """
        清理超过指定秒数的历史数据
        
        删除 activate_ip.txt 文件中时间戳与当前时间差大于指定秒数的数据行。
        
        Args:
            seconds: 秒数阈值，默认为 2592000 秒（30天）
            
        Returns:
            int: 删除的行数
        """
        # 读取所有数据
        content = self.file_handler.read_file_content(self.file_path)
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # 计算截止时间戳（当前时间减去指定秒数）
        cutoff_timestamp = datetime.now().timestamp() - seconds
        
        # 保留的新数据列表
        new_lines = []
        deleted_count = 0
        
        for line in lines:
            parts = line.split()
            if len(parts) < 1:
                continue
            
            try:
                # 解析时间戳
                timestamp = float(parts[0])
                # 如果时间戳在截止时间之后，保留该行
                if timestamp >= cutoff_timestamp:
                    new_lines.append(line)
                else:
                    deleted_count += 1
            except (ValueError, IndexError):
                # 如果时间戳格式错误，保留该行（避免误删）
                new_lines.append(line)
        
        # 如果有数据被删除，重写文件
        if deleted_count > 0:
            # 将保留的数据写入文件（覆盖原有内容）
            new_content = '\n'.join(new_lines) + '\n' if new_lines else ''
            self.file_handler.write_file(self.file_path, new_content, mode='w')
        
        return deleted_count
