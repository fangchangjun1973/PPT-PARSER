"""
解析引擎模块
负责协调整个解析过程，包括数据解析、验证和文档构建
"""
from typing import Dict, Any, Optional
import logging
from ..exceptions import ParseError, ValidationError, BuildDocumentError
from .validator import Validator
from .document_builder import DocumentBuilder
from .plugin_manager import PluginManager
from .logger import CoreLogger
from ..models.document import Document

class ParserEngine:
    """解析引擎，负责将输入数据转换为PPT文档对象"""
    
    # 输入数据大小限制（10MB）
    MAX_INPUT_SIZE = 10 * 1024 * 1024

    def __init__(self):
        """初始化解析引擎"""
        self.plugin_manager = PluginManager()
        self.validator = Validator()
        self.document_builder = DocumentBuilder()
        self.logger = CoreLogger.get_logger()

    async def parse(self, input_data: str, format_type: str = "json") -> Document:
        """
        解析输入数据并生成文档对象
        
        Args:
            input_data: 输入的数据字符串
            format_type: 数据格式类型，默认为json
            
        Returns:
            Document: 生成的文档对象
            
        Raises:
            ParseError: 解析过程出错
            ValidationError: 数据验证失败
            BuildDocumentError: 文档构建失败
        """
        try:
            # 检查输入数据大小
            if len(input_data.encode('utf-8')) > self.MAX_INPUT_SIZE:
                raise ParseError("输入数据超过大小限制")
            
            self.logger.info(f"开始解析数据，格式类型: {format_type}")
            
            # 获取适当的解析插件
            plugin = self.plugin_manager.get_plugin(format_type)
            if not plugin:
                self.logger.error(f"不支持的格式类型: {format_type}")
                raise ParseError(f"不支持的格式类型: {format_type}")
            
            # 解析数据
            self.logger.debug("开始数据解析")
            parsed_data = await plugin.parse(input_data)
            
            # 验证数据
            self.logger.debug("开始数据验证")
            if not await self.validator.validate(parsed_data):
                self.logger.error("数据验证失败")
                raise ValidationError("数据验证失败")
            
            # 构建文档
            self.logger.debug("开始构建文档")
            document = await self.document_builder.build_document(parsed_data)
            
            self.logger.info("文档解析完成")
            return document
            
        except (ParseError, ValidationError, BuildDocumentError):
            raise
        except Exception as e:
            self.logger.exception("解析过程出现未预期的错误")
            raise ParseError(f"解析过程出错: {str(e)}")