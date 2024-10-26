"""
验证器测试模块
测试数据验证功能
"""

import pytest
from typing import List, Dict, Any, Optional, Literal
from ppt_parser.core import Validator
from ppt_parser.exceptions import ValidationError

@pytest.fixture
def validator():
    """创建验证器实例"""
    return Validator()

@pytest.fixture
def valid_data():
    """有效的测试数据"""
    return {
        "title": "测试文档",
        "slides": [
            {
                "title": "测试页面",
                "elements": [
                    {
                        "type": "text",
                        "content": "测试内容",
                        "position": {"x": 0, "y": 0},
                        "style": {"font_size": 12}
                    }
                ]
            }
        ]
    }

@pytest.mark.asyncio
async def test_validate_valid_data(validator, valid_data):
    """测试验证有效数据"""
    assert await validator.validate(valid_data) is True

@pytest.mark.asyncio
async def test_validate_missing_title(validator, valid_data):
    """测试缺少标题"""
    del valid_data["title"]
    with pytest.raises(ValidationError) as exc_info:
        await validator.validate(valid_data)
    assert "缺少必需字段: title" in str(exc_info.value)

@pytest.mark.asyncio
async def test_validate_invalid_slides_type(validator, valid_data):
    """测试无效的slides类型"""
    valid_data["slides"] = "not a list"
    with pytest.raises(ValidationError) as exc_info:
        await validator.validate(valid_data)
    assert "slides必须是列表类型" in str(exc_info.value)

@pytest.mark.asyncio
async def test_validate_invalid_element_position(validator, valid_data):
    """测试无效的元素位置信息"""
    valid_data["slides"][0]["elements"][0]["position"] = "invalid"
    with pytest.raises(ValidationError) as exc_info:
        await validator.validate(valid_data)
    assert "position必须是字典类型" in str(exc_info.value)

@pytest.mark.asyncio
async def test_validate_missing_element_required_fields(validator, valid_data):
    """测试元素缺少必需字段"""
    del valid_data["slides"][0]["elements"][0]["type"]
    with pytest.raises(ValidationError) as exc_info:
        await validator.validate(valid_data)
    assert "元素缺少必需字段" in str(exc_info.value)