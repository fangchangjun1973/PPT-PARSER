"""
插件管理器模块
负责管理和加载不同格式的解析插件
"""

from typing import List  # 添加此行
from typing import Dict, Optional
from ..plugins.base_plugin import BasePlugin
from ..exceptions import PluginError

class PluginManager:
    """插件管理器，负责管理解析器插件"""

    def __init__(self):
        """初始化插件管理器"""
        self.plugins: Dict[str, BasePlugin] = {}

    def register_plugin(self, plugin: BasePlugin) -> None:
        """
        注册插件
        
        Args:
            plugin: 要注册的插件实例
            
        Raises:
            PluginError: 插件注册失败
        """
        try:
            format_type = plugin.get_format_type()
            self.plugins[format_type] = plugin
        except Exception as e:
            raise PluginError(f"插件注册失败: {str(e)}", plugin_name=str(plugin))

    def get_plugin(self, format_type: str) -> Optional[BasePlugin]:
        """
        获取指定格式的插件
        
        Args:
            format_type: 格式类型
            
        Returns:
            Optional[BasePlugin]: 对应的插件实例，如果不存在返回None
        """
        return self.plugins.get(format_type)

    def unregister_plugin(self, format_type: str) -> None:
        """
        注销插件
        
        Args:
            format_type: 要注销的插件格式类型
        """
        if format_type in self.plugins:
            del self.plugins[format_type]
            
    def get_supported_formats(self) -> List[str]:
        """
        获取所有支持的格式类型
        
        Returns:
            List[str]: 支持的格式类型列表
        """
        return list(self.plugins.keys())