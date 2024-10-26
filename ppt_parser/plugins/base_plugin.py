"""
基础插件接口模块
定义了所有解析器插件必须实现的接口
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

class BasePlugin(ABC):
    """
    解析器插件的基类
    所有具体的解析器插件都必须继承此类并实现其抽象方法
    
    示例:
        ```python
        class CustomPlugin(BasePlugin):
            def get_format_type(self) -> str:
                return "custom"
                
            async def parse(self, input_data: str) -> Dict[str, Any]:
                # 实现解析逻辑
                pass
        ```
    """
    
    @abstractmethod
    def get_format_type(self) -> str:
        """
        获取插件支持的格式类型
        
        Returns:
            str: 格式类型标识符（如 'json', 'yaml' 等）
        """
        pass
        
    @abstractmethod
    async def parse(self, input_data: str) -> Dict[str, Any]:
        """
        解析输入数据
        
        Args:
            input_data: 要解析的数据字符串
            
        Returns:
            Dict[str, Any]: 解析后的数据字典
            
        Raises:
            ParseError: 解析过程中出现错误
        """
        pass
    
    @abstractmethod
    async def validate_format(self, input_data: str) -> bool:
        """
        验证输入数据格式是否符合要求
        
        Args:
            input_data: 要验证的数据字符串
            
        Returns:
            bool: 格式是否有效
        """
        pass
    
    def get_plugin_info(self) -> Dict[str, str]:
        """
        获取插件信息
        
        Returns:
            Dict[str, str]: 包含插件信息的字典
        """
        return {
            "type": self.get_format_type(),
            "name": self.__class__.__name__,
            "version": getattr(self, "VERSION", "1.0.0")
        }