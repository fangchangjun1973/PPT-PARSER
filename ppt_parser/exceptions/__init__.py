"""
PPT解析器异常处理模块
定义了所有自定义异常类
"""

from .base_exception import PPTParserBaseError
from .parse_error import ParseError
from .validation_error import ValidationError
from .build_document_error import BuildDocumentError
from .plugin_error import PluginError  # 添加这一行

__all__ = [
    'PPTParserBaseError',
    'ParseError',
    'ValidationError',
    'BuildDocumentError',
    'PluginError'  # 添加这一行
]
