"""
API 统一响应工具类

提供标准化的 API 响应格式，包括成功响应和错误响应。
"""

from typing import Any, Optional


class APIResponse:
    """
    API 统一响应类
    
    用于生成标准化的 API 响应数据，确保所有接口返回格式一致。
    """
    
    @staticmethod
    def success(data: Any = None, message: str = "操作成功") -> dict:
        """
        生成成功响应
        
        Args:
            data: 响应数据，可以是任意类型
            message: 成功提示信息，默认为 "操作成功"
            
        Returns:
            dict: 标准化的成功响应字典
            {
                "code": 200,
                "message": "操作成功",
                "data": data
            }
        """
        return {
            "code": 200,
            "message": message,
            "data": data
        }
    
    @staticmethod
    def error(message: str = "操作失败", code: int = 500, data: Any = None) -> dict:
        """
        生成错误响应
        
        Args:
            message: 错误提示信息，默认为 "操作失败"
            code: 错误状态码，默认为 500
            data: 可选的错误详情数据
            
        Returns:
            dict: 标准化的错误响应字典
            {
                "code": 500,
                "message": "操作失败",
                "data": data
            }
        """
        return {
            "code": code,
            "message": message,
            "data": data
        }
    
    @staticmethod
    def bad_request(message: str = "请求参数错误", data: Any = None) -> dict:
        """
        生成 400 错误响应（请求参数错误）
        
        Args:
            message: 错误提示信息，默认为 "请求参数错误"
            data: 可选的错误详情数据
            
        Returns:
            dict: 标准化的 400 错误响应字典
        """
        return APIResponse.error(message=message, code=400, data=data)
    
    @staticmethod
    def not_found(message: str = "资源不存在", data: Any = None) -> dict:
        """
        生成 404 错误响应（资源不存在）
        
        Args:
            message: 错误提示信息，默认为 "资源不存在"
            data: 可选的错误详情数据
            
        Returns:
            dict: 标准化的 404 错误响应字典
        """
        return APIResponse.error(message=message, code=404, data=data)
    
    @staticmethod
    def server_error(message: str = "服务器内部错误", data: Any = None) -> dict:
        """
        生成 500 错误响应（服务器内部错误）
        
        Args:
            message: 错误提示信息，默认为 "服务器内部错误"
            data: 可选的错误详情数据
            
        Returns:
            dict: 标准化的 500 错误响应字典
        """
        return APIResponse.error(message=message, code=500, data=data)
