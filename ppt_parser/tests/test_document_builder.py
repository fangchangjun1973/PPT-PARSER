"""
文档构建器测试模块
测试文档对象的构建功能
"""

import pytest
from typing import List, Dict, Any, Optional, Literal
from ppt_parser.core import DocumentBuilder
from ppt_parser.models.document import Document, Slide, Element
from ppt_parser.exceptions import BuildDocumentError

@pytest.fixture
def document_builder():
    """创建文档构建器实例"""
    return DocumentBuilder()

@pytest.fixture
def valid_doc_data():
    """有效的文档数据"""
    return {
        "title": "测试文档",
        "metadata": {
            "author": "测试作者",
            "version": "1.0"
        },
        "slides": [
            {
                "title": "第一页",
                "elements": [
                    {
                        "type": "text",
                        "content": "Hello World",
                        "position": {"x": 100, "y": 100},
                        "style": {
                            "font_size": 24,
                            "color": "#000000"
                        }
                    }
                ],
                "background": {"color": "#FFFFFF"}
            }
        ]
    }

@pytest.mark.asyncio
async def test_build_document_success(document_builder, valid_doc_data):
    """测试成功构建文档"""
    document = await document_builder.build_document(valid_doc_data)
    
    # 验证文档基本信息
    assert isinstance(document, Document)
    assert document.title == valid_doc_data["title"]
    assert document.metadata == valid_doc_data["metadata"]
    
    # 验证幻灯片
    assert len(document.slides) == 1
    slide = document.slides[0]
    assert isinstance(slide, Slide)
    assert slide.title == valid_doc_data["slides"][0]["title"]
    
    # 验证元素
    assert len(slide.elements) == 1
    element = slide.elements[0]
    assert isinstance(element, Element)
    assert element.type == valid_doc_data["slides"][0]["elements"][0]["type"]
    assert element.content == valid_doc_data["slides"][0]["elements"][0]["content"]

@pytest.mark.asyncio
async def test_build_document_missing_title(document_builder, valid_doc_data):
    """测试缺少文档标题"""
    del valid_doc_data["title"]
    with pytest.raises(BuildDocumentError) as exc_info:
        await document_builder.build_document(valid_doc_data)
    assert "缺少必需字段" in str(exc_info.value)

@pytest.mark.asyncio
async def test_build_document_invalid_element(document_builder, valid_doc_data):
    """测试无效的元素数据"""
    valid_doc_data["slides"][0]["elements"][0]["position"] = "invalid"
    with pytest.raises(BuildDocumentError) as exc_info:
        await document_builder.build_document(valid_doc_data)
    assert "元素构建失败" in str(exc_info.value)

@pytest.mark.asyncio
async def test_build_document_with_empty_slides(document_builder, valid_doc_data):
    """测试空幻灯片列表"""
    valid_doc_data["slides"] = []
    document = await document_builder.build_document(valid_doc_data)
    assert isinstance(document, Document)
    assert len(document.slides) == 0

@pytest.mark.asyncio
async def test_build_document_with_multiple_slides(document_builder, valid_doc_data):
    """测试多个幻灯片"""
    valid_doc_data["slides"].append(valid_doc_data["slides"][0].copy())
    document = await document_builder.build_document(valid_doc_data)
    assert len(document.slides) == 2