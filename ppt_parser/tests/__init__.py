"""
PPT Parser 测试模块
提供测试配置和通用测试辅助工具
"""

import pytest
import json
from typing import Dict, Any
from pathlib import Path

# 测试数据目录
TEST_DATA_DIR = Path(__file__).parent / "test_data"

def load_test_json(filename: str) -> Dict[str, Any]:
    """
    加载JSON测试数据文件
    
    Args:
        filename: 测试数据文件名
        
    Returns:
        Dict[str, Any]: 加载的测试数据
        
    Raises:
        FileNotFoundError: 文件不存在
        json.JSONDecodeError: JSON格式错误
    """
    file_path = TEST_DATA_DIR / filename
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 测试数据示例
SAMPLE_DOCUMENT = {
    "title": "测试文档",
    "metadata": {
        "author": "Test Author",
        "version": "1.0.0"
    },
    "slides": [
        {
            "title": "测试页面",
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

# 测试用例标记
pytest.mark.asyncio  # 用于异步测试
pytest.mark.integration  # 用于集成测试
pytest.mark.unit  # 用于单元测试

# 通用测试异常
class TestError(Exception):
    """测试相关的异常基类"""
    pass

class TestDataError(TestError):
    """测试数据相关的异常"""
    pass

# 测试辅助函数
def assert_document_structure(data: Dict[str, Any]) -> None:
    """
    验证文档结构的正确性
    
    Args:
        data: 要验证的文档数据
        
    Raises:
        TestDataError: 文档结构无效
    """
    required_fields = ["title", "slides"]
    for field in required_fields:
        if field not in data:
            raise TestDataError(f"缺少必需字段: {field}")
    
    if not isinstance(data["slides"], list):
        raise TestDataError("slides必须是列表类型")
        
    for slide in data["slides"]:
        assert_slide_structure(slide)

def assert_slide_structure(slide: Dict[str, Any]) -> None:
    """
    验证幻灯片结构的正确性
    
    Args:
        slide: 要验证的幻灯片数据
        
    Raises:
        TestDataError: 幻灯片结构无效
    """
    required_fields = ["title", "elements"]
    for field in required_fields:
        if field not in slide:
            raise TestDataError(f"幻灯片缺少必需字段: {field}")
            
    if not isinstance(slide["elements"], list):
        raise TestDataError("elements必须是列表类型")
        
    for element in slide["elements"]:
        assert_element_structure(element)

def assert_element_structure(element: Dict[str, Any]) -> None:
    """
    验证元素结构的正确性
    
    Args:
        element: 要验证的元素数据
        
    Raises:
        TestDataError: 元素结构无效
    """
    required_fields = ["type", "content", "position"]
    for field in required_fields:
        if field not in element:
            raise TestDataError(f"元素缺少必需字段: {field}")
            
    if not isinstance(element["position"], dict):
        raise TestDataError("position必须是字典类型")
        
    if "style" in element and not isinstance(element["style"], dict):
        raise TestDataError("style必须是字典类型")

# 测试装饰器
def requires_test_data(filename: str):
    """
    要求测试数据文件的装饰器
    
    Args:
        filename: 测试数据文件名
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                test_data = load_test_json(filename)
                return func(*args, test_data=test_data, **kwargs)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                raise TestDataError(f"加载测试数据失败: {str(e)}")
        return wrapper
    return decorator