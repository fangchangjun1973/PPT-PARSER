"""
JSON格式解析插件
实现了对JSON格式数据的解析支持
"""

import json
from typing import Dict, Any
from ..exceptions import ParseError
from .base_plugin import BasePlugin

class JSONPlugin(BasePlugin):
    """JSON格式解析插件"""
    
    VERSION = "1.0.0"
    MAX_DEPTH = 10  # 最大递归深度限制
    
    def get_format_type(self) -> str:
        """获取插件支持的格式类型"""
        return "json"
    
    async def validate_format(self, input_data: str) -> bool:
        """验证JSON格式是否有效"""
        try:
            # 使用自定义的JSON解码器检查深度
            json.loads(input_data, cls=DepthLimitedJSONDecoder, max_depth=self.MAX_DEPTH)
            return True
        except (json.JSONDecodeError, RecursionError):
            return False
            
    async def parse(self, input_data: str) -> Dict[str, Any]:
        """解析JSON数据"""
        try:
            # 使用自定义的JSON解码器进行解析
            data = json.loads(
                input_data, 
                cls=DepthLimitedJSONDecoder, 
                max_depth=self.MAX_DEPTH
            )
            
            if not isinstance(data, dict):
                raise ParseError("JSON根节点必须是对象")
                
            required_fields = ["title", "slides"]
            for field in required_fields:
                if field not in data:
                    raise ParseError(f"缺少必需字段: {field}")
                    
            # 验证slides数组
            if not isinstance(data["slides"], list):
                raise ParseError("slides必须是数组")
                
            for slide in data["slides"]:
                self._validate_slide(slide)
                
            return data
            
        except json.JSONDecodeError as e:
            raise ParseError(f"JSON解析错误: {str(e)}")
        except RecursionError:
            raise ParseError("JSON结构嵌套深度超过限制")
        except ParseError:
            raise
        except Exception as e:
            raise ParseError(f"解析过程出错: {str(e)}")

class DepthLimitedJSONDecoder(json.JSONDecoder):
    """带深度限制的JSON解码器"""
    
    def __init__(self, *args, max_depth=None, **kwargs):
        """
        初始化解码器
        
        Args:
            max_depth: 最大递归深度
        """
        self.max_depth = max_depth
        super().__init__(*args, **kwargs)
        
    def decode(self, s: str) -> Any:
        """
        解码JSON字符串
        
        Args:
            s: JSON字符串
            
        Returns:
            解码后的Python对象
            
        Raises:
            RecursionError: 超过最大递归深度
        """
        def check_depth(obj, current_depth=0):
            """检查对象的嵌套深度"""
            if current_depth > self.max_depth:
                raise RecursionError("Exceeded maximum depth")
                
            if isinstance(obj, dict):
                return {k: check_depth(v, current_depth + 1) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [check_depth(item, current_depth + 1) for item in obj]
            return obj
            
        obj = super().decode(s)
        return check_depth(obj)