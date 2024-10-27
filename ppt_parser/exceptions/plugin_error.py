# ppt_parser/exceptions/plugin_error.py

"""
插件错误异常类
用于处理插件相关的错误
"""

from typing import Dict, Any, Optional
from .base_exception import PPTParserBaseError


class PluginError(PPTParserBaseError):
    """插件错误异常类"""

    def __init__(
        self,
        message: str,
        plugin_name: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        """
        初始化插件错误异常

        Args:
            message: 错误信息
            plugin_name: 出错插件的名称
            details: 其他详细信息
        """
        error_details = details or {}
        if plugin_name:
            error_details["plugin_name"] = plugin_name

        super().__init__(
            message=message, error_code="PLUGIN_ERROR", details=error_details
        )
        self.plugin_name = plugin_name
