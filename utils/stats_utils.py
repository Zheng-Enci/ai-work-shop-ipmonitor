from utils.file_utils import FileHandler
from typing import Optional
from collections import Counter
from datetime import datetime, timedelta
import threading
import time


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
    
    def _cleanup_worker(self, file_handler: FileHandler, seconds: int, interval: int) -> None:
        """
        清理工作线程函数
        
        在后台定期执行数据清理任务。
        
        Args:
            file_handler: 文件处理器实例（独立的，避免与主线程冲突）
            seconds: 秒数阈值，超过此时间的数据将被删除
            interval: 清理间隔（秒）
        """
        while True:
            try:
                self._do_cleanup(file_handler, seconds)
            except Exception as e:
                # 清理过程中出现异常，记录错误但不影响线程继续运行
                print(f"[清理线程] 清理数据时出错: {e}")
            
            # 等待指定的间隔时间
            time.sleep(interval)
    
    def _do_cleanup(self, file_handler: FileHandler, seconds: int) -> int:
        """
        执行实际的清理操作
        
        Args:
            file_handler: 文件处理器实例
            seconds: 秒数阈值
            
        Returns:
            int: 删除的行数
        """
        # 读取所有数据
        content = file_handler.read_file_content(self.file_path)
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
            
            # 解析时间戳
            timestamp = float(parts[0])
            # 如果时间戳在截止时间之后，保留该行
            if timestamp >= cutoff_timestamp:
                new_lines.append(line)
            else:
                deleted_count += 1
        
        # 如果有数据被删除，重写文件
        if deleted_count > 0:
            # 将保留的数据写入文件（覆盖原有内容）
            new_content = '\n'.join(new_lines) + '\n' if new_lines else ''
            file_handler.write_file(self.file_path, new_content, mode='w')
            print(f"[清理线程] 已清理 {deleted_count} 行过期数据")
        
        return deleted_count
    
    def start_auto_cleanup(self, file_handler: FileHandler, seconds: int = 2592000, interval: int = 3600) -> None:
        """
        启动自动清理线程
        
        创建一个后台守护线程，定期清理超过指定秒数的历史数据。
        该线程不会阻碍主线程的运行，主线程退出时自动结束。
        
        Args:
            file_handler: 文件处理器实例（建议传入独立的实例以避免冲突）
            seconds: 秒数阈值，默认为 2592000 秒（30天）
            interval: 清理间隔（秒），默认为 3600 秒（1小时）
        """
        # 创建并启动清理线程
        cleanup_thread = threading.Thread(
            target=self._cleanup_worker,
            args=(file_handler, seconds, interval),
            name="DataCleanupThread",
            daemon=True  # 设置为守护线程，主线程退出时自动结束
        )
        cleanup_thread.start()
        print(f"[清理线程] 已启动，每隔 {interval} 秒清理一次超过 {seconds} 秒的数据")
    
    def get_data_by_time_range(self, start_time: float, end_time: float) -> list:
        """
        获取指定时间范围内的数据
        
        返回在 start_time 和 end_time 之间（包含边界）的所有数据行。
        
        Args:
            start_time: 开始时间戳（Unix 时间戳，秒）
            end_time: 结束时间戳（Unix 时间戳，秒）
            
        Returns:
            list: 符合条件的数据行列表，每行是一个字典包含 timestamp 和 ips
            例如：[{'timestamp': 1776585378.4079862, 'ips': ['10.0.48.241', '10.0.48.153']}, ...]
        """
        data = self._load_data()
        result = []
        
        for line in data:
            parts = line.split()
            if len(parts) < 2:
                continue
            
            timestamp = float(parts[0])
            # 检查时间戳是否在指定范围内
            if start_time <= timestamp <= end_time:
                ips = parts[1:]
                result.append({
                    'timestamp': timestamp,
                    'ips': ips
                })
        
        return result
