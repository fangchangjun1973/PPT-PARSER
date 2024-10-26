"""
文档构建器模块
负责将验证后的数据构建为文档对象
"""

from typing import Dict, Any, List
from ..exceptions import BuildDocumentError
from ..models.document import Document, Slide, Element, Position, Style

class DocumentBuilder:
    """文档构建器，负责构建PPT文档对象"""

    async def build_document(self, data: Dict[str, Any]) -> Document:
        """
        构建文档对象
        
        Args:
            data: 验证后的数据字典
            
        Returns:
            Document: 构建的文档对象
            
        Raises:
            BuildDocumentError: 构建过程出错
        """
        try:
            document = Document(
                title=data["title"],
                metadata=data.get("metadata", {})
            )

            # 构建幻灯片
            if "slides" in data:
                for slide_data in data["slides"]:
                    slide = await self._build_slide(slide_data)
                    document.slides.append(slide)

            return document
            
        except KeyError as e:
            raise BuildDocumentError(f"缺少必需字段: {str(e)}")
        except Exception as e:
            raise BuildDocumentError(f"文档构建失败: {str(e)}")

    async def _build_slide(self, slide_data: Dict[str, Any]) -> Slide:
        """构建幻灯片对象"""
        try:
            slide = Slide(
                title=slide_data["title"],
                background=slide_data.get("background"),
                layout=slide_data.get("layout")
            )

            # 构建元素
            if "elements" in slide_data:
                for element_data in slide_data["elements"]:
                    element = await self._build_element(element_data)
                    slide.elements.append(element)

            return slide
            
        except KeyError as e:
            raise BuildDocumentError(f"幻灯片缺少必需字段: {str(e)}")
        except Exception as e:
            raise BuildDocumentError(f"幻灯片构建失败: {str(e)}")

    async def _build_element(self, element_data: Dict[str, Any]) -> Element:
        """构建元素对象"""
        try:
            position = Position(**element_data["position"])
            style = Style(**(element_data.get("style", {})))
            
            element = Element(
                type=element_data["type"],
                content=element_data["content"],
                position=position,
                style=style,
                size=element_data.get("size")
            )
            return element
            
        except KeyError as e:
            raise BuildDocumentError(f"元素缺少必需字段: {str(e)}")
        except Exception as e:
            raise BuildDocumentError(f"元素构建失败: {str(e)}")