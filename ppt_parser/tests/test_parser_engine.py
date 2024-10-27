"""
解析引擎测试模块
测试 ParserEngine 的功能和异常处理
"""

import pytest
from typing import Dict, Any
from typing import List, Dict, Any, Optional, Literal
from ppt_parser.core import ParserEngine
from ppt_parser.plugins import JSONPlugin
from ppt_parser.exceptions import ParseError, ValidationError, BuildDocumentError


@pytest.fixture
async def parser_engine():
    """创建解析引擎实例"""
    engine = ParserEngine()
    plugin = JSONPlugin()
    engine.plugin_manager.register_plugin(plugin)
    return engine


@pytest.fixture
def valid_json_data():
    """有效的JSON测试数据"""
    return """
    {
        "title": "测试演示",
        "slides": [
            {
                "title": "第一页",
                "elements": [
                    {
                        "type": "text",
                        "content": "Hello World",
                        "position": {"x": 100, "y": 100},
                        "style": {"font_size": 24}
                    }
                ]
            }
        ]
    }
    """


@pytest.mark.asyncio
async def test_parse_valid_json(parser_engine, valid_json_data):
    """测试解析有效的JSON数据"""
    document = await parser_engine.parse(valid_json_data, "json")
    assert document.title == "测试演示"
    assert len(document.slides) == 1
    assert document.slides[0].title == "第一页"
    assert len(document.slides[0].elements) == 1


@pytest.mark.asyncio
async def test_parse_invalid_json(parser_engine):
    """测试解析无效的JSON数据"""
    with pytest.raises(ParseError):
        await parser_engine.parse("{invalid json", "json")


@pytest.mark.asyncio
async def test_parse_missing_required_fields(parser_engine):
    """测试缺少必需字段的情况"""
    invalid_data = '{"title": "测试"}'  # 缺少slides字段
    with pytest.raises(ValidationError):
        await parser_engine.parse(invalid_data, "json")


@pytest.mark.asyncio
async def test_parse_unsupported_format(parser_engine):
    """测试不支持的格式类型"""
    with pytest.raises(ParseError) as exc_info:
        await parser_engine.parse("{}", "unsupported")
    assert "不支持的格式类型" in str(exc_info.value)


@pytest.mark.asyncio
async def test_parse_large_input(parser_engine):
    """测试超大输入数据"""
    large_data = '{"title": "test", "slides": []}'.ljust(
        parser_engine.MAX_INPUT_SIZE + 1
    )
    with pytest.raises(ParseError) as exc_info:
        await parser_engine.parse(large_data, "json")
    assert "超过大小限制" in str(exc_info.value)
