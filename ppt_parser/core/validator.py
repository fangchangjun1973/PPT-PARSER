"""
数据验证器模块
负责验证解析后的数据是否符合要求
"""

from typing import Dict, Any, List, Optional
from ..exceptions import ValidationError
from ..models.document import Document, Slide, Element

class Validator:
    """数据验证器，负责验证解析后的数据"""

    async def validate(self, data: Dict[str, Any]) -> bool:
        """
        验证数据是否符合要求
        
        Args:
            data: 要验证的数据字典
            
        Returns:
            bool: 验证是否通过
            
        Raises:
            ValidationError: 验证失败
        """
        try:
            # 验证基本结构
            self._validate_structure(data)
            
            # 验证文档属性
            self._validate_document(data)
            
            # 验证幻灯片
            if "slides" in data:
                for slide_data in data["slides"]:
                    self._validate_slide(slide_data)
                    
            return True
            
        except ValidationError:
            raise
        except Exception as e:
            raise ValidationError(f"验证过程出错: {str(e)}")

    def _validate_structure(self, data: Dict[str, Any]) -> None:
        """验证数据基本结构"""
        required_fields = ["title", "slides"]
        for field in required_fields:
            if field not in data:
                raise ValidationError(f"缺少必需字段: {field}")

        if not isinstance(data["slides"], list):
            raise ValidationError("slides必须是列表类型")

    def _validate_document(self, data: Dict[str, Any]) -> None:
        """验证文档属性"""
        if not isinstance(data["title"], str) or not data["title"].strip():
            raise ValidationError("文档标题不能为空")

        if "metadata" in data and not isinstance(data["metadata"], dict):
            raise ValidationError("metadata必须是字典类型")

    def _validate_slide(self, slide_data: Dict[str, Any]) -> None:
        """验证幻灯片数据"""
        if not isinstance(slide_data, dict):
            raise ValidationError("幻灯片数据必须是字典类型")

        required_fields = ["title", "elements"]
        for field in required_fields:
            if field not in slide_data:
                raise ValidationError(f"幻灯片缺少必需字段: {field}")

        if not isinstance(slide_data["elements"], list):
            raise ValidationError("elements必须是列表类型")

        for element_data in slide_data["elements"]:
            self._validate_element(element_data)

    def _validate_element(self, element_data: Dict[str, Any]) -> None:
        """验证元素数据"""
        if not isinstance(element_data, dict):
            raise ValidationError("元素数据必须是字典类型")

        required_fields = ["type", "content", "position"]
        for field in required_fields:
            if field not in element_data:
                raise ValidationError(f"元素缺少必需字段: {field}")

        # 验证position
        if not isinstance(element_data["position"], dict):
            raise ValidationError("position必须是字典类型")
        if "x" not in element_data["position"] or "y" not in element_data["position"]:
            raise ValidationError("position必须包含x和y坐标")

        # 验证style
        if "style" in element_data and not isinstance(element_data["style"], dict):
            raise ValidationError("style必须是字典类型")