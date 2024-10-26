# exceptions/error_codes.py
"""错误代码定义"""
from enum import Enum, auto

class ErrorCode(Enum):
    """错误代码枚举"""
    
    # 解析错误
    PARSE_ERROR = auto()                # 一般解析错误
    INVALID_JSON = auto()               # JSON格式无效
    INVALID_FORMAT = auto()             # 格式错误
    
    # 验证错误
    VALIDATION_ERROR = auto()           # 一般验证错误
    INVALID_FIELD = auto()              # 字段值无效
    MISSING_FIELD = auto()              # 缺少必需字段
    
    # 构建错误
    BUILD_ERROR = auto()                # 一般构建错误
    RESOURCE_NOT_FOUND = auto()         # 资源未找到
    INVALID_ELEMENT = auto()            # 元素无效
    
    @classmethod
    def get_message(cls, code: 'ErrorCode') -> str:
        """获取错误代码对应的默认消息"""
        messages = {
            cls.PARSE_ERROR: "解析错误",
            cls.INVALID_JSON: "无效的JSON格式",
            cls.INVALID_FORMAT: "无效的数据格式",
            cls.VALIDATION_ERROR: "数据验证错误",
            cls.INVALID_FIELD: "字段值无效",
            cls.MISSING_FIELD: "缺少必需字段",
            cls.BUILD_ERROR: "文档构建错误",
            cls.RESOURCE_NOT_FOUND: "资源未找到",
            cls.INVALID_ELEMENT: "无效的元素"
        }
        return messages.get(code, "未知错误")