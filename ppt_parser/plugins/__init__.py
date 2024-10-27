"""
PPT解析器插件系统
提供了基础插件接口和具体的解析器插件实现
"""

from .base_plugin import BasePlugin
from .json_plugin import JSONPlugin

__all__ = ["BasePlugin", "JSONPlugin"]
