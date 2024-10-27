"""
文档构建错误异常类
用于处理PPT文档构建过程中的错误
"""
from typing import Dict, Any, Optional
from .base_exception import PPTParserBaseError


class BuildDocumentError(PPTParserBaseError):
    """文档构建错误异常类"""

    def __init__(
        self,
        message: str,
        stage: str = None,
        element_id: str = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        """
        初始化文档构建错误异常

        Args:
            message: 错误信息
            stage: 构建阶段
            element_id: 出错元素的ID
            details: 其他详细信息
        """
        error_details = details or {}
        if stage:
            error_details["stage"] = stage
        if element_id:
            error_details["element_id"] = element_id

        super().__init__(
            message=message, error_code="BUILD_ERROR", details=error_details
        )
        self.stage = stage
        self.element_id = element_id
