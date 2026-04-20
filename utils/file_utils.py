import threading
import os


class FileHandler:
    """线程安全的文件操作类"""
    
    def __init__(self, file_path: str) -> None:
        """初始化文件处理器，创建文件锁"""
        self._file_lock = threading.Lock()
        self._file_path = file_path
    
    def write_file(self, content: str, mode: str = 'a+', encoding: str = 'utf-8') -> None:
        """
        线程安全的文件写入
        
        Args:
            content: 要写入的内容
            mode: 文件打开模式，默认为 'a+'（追加模式）
            encoding: 文件编码，默认为 'utf-8'
        """
        with self._file_lock:
            with open(self._file_path, mode, encoding = encoding) as f:
                f.write(content)
                f.flush()  # 确保数据立即写入磁盘
    
    def read_file_content(self, encoding: str = 'utf-8-sig') -> str:
        """
        线程安全的文件读取（返回完整内容字符串）
        
        Args:
            encoding: 文件编码，默认为 'utf-8-sig'
        
        Returns:
            str: 文件的完整内容
        """
        with self._file_lock:
            if not os.path.exists(self._file_path):
                return ''
            with open(self._file_path, 'r', encoding = encoding) as f:
                return f.read()
