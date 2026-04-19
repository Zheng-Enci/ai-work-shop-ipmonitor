"""
管理员权限检测工具模块

提供检测当前程序是否以管理员身份运行的功能，
以及以管理员身份重新启动程序的功能。
"""

import ctypes
import os
import sys


class AdminChecker:
    """
    管理员权限检测类
    
    用于检测当前程序是否以管理员身份运行，
    以及以管理员身份重新启动程序。
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
    
    @staticmethod
    def restart_as_admin() -> None:
        """
        以管理员身份重新启动当前程序
        
        使用 ShellExecute 以管理员权限重新启动当前脚本，
        然后退出当前进程。
        """
        try:
            # 获取当前 Python 解释器路径和脚本路径
            python_exe = sys.executable
            script_path = sys.argv[0]
            
            # 构建命令行参数（如果有的话）
            params = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
            
            # 使用 ShellExecute 以管理员权限运行
            ctypes.windll.shell32.ShellExecuteW(
                None,  # 父窗口句柄
                "runas",  # 以管理员身份运行
                python_exe,  # 可执行文件
                f'"{script_path}" {params}',  # 参数
                None,  # 工作目录
                1  # 显示窗口
            )
            
            # 退出当前进程
            sys.exit(0)
        except Exception as e:
            print(f"以管理员身份重新启动失败: {e}")
            sys.exit(1)
    
    @staticmethod
    def ensure_admin() -> None:
        """
        确保程序以管理员身份运行
        
        检测当前程序是否以管理员身份运行，如果不是，
        则自动以管理员身份重新启动程序。
        
        使用示例:
            if __name__ == '__main__':
                AdminChecker.ensure_admin()
                # 以下代码将以管理员身份执行
                main()
        """
        if not AdminChecker.is_admin():
            print("需要管理员权限，正在重新启动...")
            AdminChecker.restart_as_admin()
        # 如果已经是管理员，则继续执行
