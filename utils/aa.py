"""
管理员权限检测工具模块

提供检测当前程序是否以管理员身份运行的功能。
"""

import ctypes
import os


class AdminChecker:
    """
    管理员权限检测类
    
    用于检测当前程序是否以管理员/ root 身份运行。
    """
    
    @staticmethod
    def is_admin() -> bool:
        """
        检测当前程序是否以管理员身份运行
        
        Returns:
            bool: 如果以管理员身份运行返回 True，否则返回 False
        """
        try:
            # Windows 系统使用 ctypes 检查管理员权限
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            # 如果检测失败，默认返回 False
            return False
