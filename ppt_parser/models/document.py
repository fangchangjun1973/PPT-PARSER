"""
PPT文档数据模型
定义文档、幻灯片和元素的基本结构

使用示例:
    ```python
    # 创建一个文档
    doc = Document(
        title="示例演示",
        slides=[
            Slide(
                title="第一页",
                elements=[
                    Element(
                        type="text",
                        content="Hello World",
                        position=Position(x=100, y=100),
                        style=Style(font_size=24, color="#000000")
                    )
                ]
            )
        ]
    )
    ```
"""
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field, field_validator


class Position(BaseModel):
    """
    元素位置信息

    Attributes:
        x: X坐标 (0-1000)
        y: Y坐标 (0-1000)
        unit: 单位 ("px", "pt", "in", "cm")
    """

    x: float = Field(ge=0, le=1000, description="X坐标")
    y: float = Field(ge=0, le=1000, description="Y坐标")
    unit: Literal["px", "pt", "in", "cm"] = Field(default="px", description="单位")


class Style(BaseModel):
    """
    元素样式信息

    Attributes:
        font_size: 字体大小 (1-1000)
        font_family: 字体系列
        color: 颜色(十六进制，例如 #FF0000)
        bold: 是否加粗
        italic: 是否斜体
        underline: 是否下划线
        background_color: 背景颜色(十六进制)
        opacity: 透明度 (0-1)
        rotation: 旋转角度 (0-360)
    """

    font_size: Optional[int] = Field(None, ge=1, le=1000, description="字体大小")
    font_family: Optional[str] = Field(None, description="字体系列")
    color: Optional[str] = Field(
        None, pattern="^#[0-9A-Fa-f]{6}$", description="颜色(十六进制，例如 #FF0000)"
    )
    bold: Optional[bool] = Field(False, description="是否加粗")
    italic: Optional[bool] = Field(False, description="是否斜体")
    underline: Optional[bool] = Field(False, description="是否下划线")
    background_color: Optional[str] = Field(
        None, pattern="^#[0-9A-Fa-f]{6}$", description="背景颜色(十六进制)"
    )
    opacity: Optional[float] = Field(1.0, ge=0, le=1, description="透明度")
    rotation: Optional[float] = Field(0.0, ge=0, le=360, description="旋转角度")

    @field_validator("color", "background_color", mode="before")
    def validate_color(cls, v):
        """验证颜色格式"""
        if v is not None and not v.startswith("#"):
            raise ValueError("颜色值必须以#开头")
        return v


class Element(BaseModel):
    """
    PPT元素基类

    Attributes:
        type: 元素类型 ("text", "image", "shape", "chart")
        content: 元素内容
        position: 元素位置
        style: 元素样式
        size: 元素大小
    """

    type: Literal["text", "image", "shape", "chart"] = Field(..., description="元素类型")
    content: Any = Field(..., description="元素内容")
    position: Position = Field(..., description="元素位置")
    style: Style = Field(default_factory=Style, description="元素样式")
    size: Optional[Dict[str, float]] = Field(None, description="元素大小")

    class Config:
        """模型配置"""

        extra = "allow"
        json_schema_extra = {  # 将 schema_extra 改为 json_schema_extra
            "example": {
                "type": "text",
                "content": "示例文本",
                "position": {"x": 100, "y": 100, "unit": "px"},
                "style": {"font_size": 24, "color": "#000000"},
            }
        }


class Slide(BaseModel):
    """
    PPT幻灯片

    Attributes:
        title: 幻灯片标题
        elements: 幻灯片元素列表
        background: 背景设置
        layout: 布局类型
        notes: 备注
    """

    title: str = Field(..., min_length=1, max_length=100, description="幻灯片标题")
    elements: List[Element] = Field(default_factory=list, description="幻灯片元素列表")
    background: Optional[Dict[str, Any]] = Field(None, description="背景设置")
    layout: Optional[str] = Field(None, description="布局类型")
    notes: Optional[str] = Field(None, description="幻灯片备注")

    class Config:
        """模型配置"""

        extra = "allow"


class Document(BaseModel):
    """
    PPT文档

    Attributes:
        title: 文档标题
        slides: 幻灯片列表
        theme: 主题设置
        metadata: 元数据
    """

    title: str = Field(..., min_length=1, max_length=200, description="文档标题")
    slides: List[Slide] = Field(default_factory=list, description="幻灯片列表")
    theme: Optional[Dict[str, Any]] = Field(None, description="主题设置")
    metadata: Dict[str, Any] = Field(
        default_factory=lambda: {
            "author": "",
            "created": "",
            "modified": "",
            "version": "1.0",
        },
        description="元数据",
    )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return self.model_dump(exclude_none=True)  # 使用 model_dump 替代 dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Document":
        """从字典创建文档对象"""
        return cls.model_validate(data)  # 使用 model_validate 替代 parse_obj

    class Config:
        """模型配置"""

        extra = "allow"
