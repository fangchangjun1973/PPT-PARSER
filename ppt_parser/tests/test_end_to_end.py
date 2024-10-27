"""
端到端集成测试
测试完整的文档解析和生成流程
"""

import pytest
from typing import List, Dict, Any, Optional, Literal
from ppt_parser.core import ParserEngine
from ppt_parser.plugins import JSONPlugin
from ppt_parser.models.document import Document, Slide, Element


@pytest.fixture
async def setup_engine():
    """设置解析引擎"""
    engine = ParserEngine()
    plugin = JSONPlugin()
    engine.plugin_manager.register_plugin(plugin)
    return engine


@pytest.mark.asyncio
async def test_end_to_end_flow(setup_engine):
    """测试完整的解析流程"""
    # 准备测试数据
    input_json = """
    {
        "title": "端到端测试",
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
                        "content": "标题文本",
                        "position": {"x": 100, "y": 50},
                        "style": {"font_size": 32}
                    },
                    {
                        "type": "image",
                        "content": "test.png",
                        "position": {"x": 200, "y": 150},
                        "style": {"size": {"width": 300, "height": 200}}
                    }
                ]
            },
            {
                "title": "第二页",
                "elements": [
                    {
                        "type": "chart",
                        "content": {
                            "type": "bar",
                            "data": [1, 2, 3, 4, 5]
                        },
                        "position": {"x": 150, "y": 100},
                        "style": {"width": 400, "height": 300}
                    }
                ]
            }
        ]
    }
    """

    # 执行解析
    document = await setup_engine.parse(input_json, "json")

    # 验证文档结构
    assert isinstance(document, Document)
    assert document.title == "端到端测试"
    assert document.metadata["author"] == "测试作者"
    assert len(document.slides) == 2

    # 验证第一页
    slide1 = document.slides[0]
    assert isinstance(slide1, Slide)
    assert slide1.title == "第一页"
    assert len(slide1.elements) == 2
    assert slide1.elements[0].type == "text"
    assert slide1.elements[1].type == "image"

    # 验证第二页
    slide2 = document.slides[1]
    assert isinstance(slide2, Slide)
    assert slide2.title == "第二页"
    assert len(slide2.elements) == 1
    assert slide2.elements[0].type == "chart"

    # 验证元素属性
    text_element = slide1.elements[0]
    assert text_element.content == "标题文本"
    assert text_element.position
