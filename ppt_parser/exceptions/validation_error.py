"""
验证错误异常类
用于处理数据验证过程中的错误
"""
from typing import List, Dict, Any, Optional
from .base_exception import PPTParserBaseError


class ValidationError(PPTParserBaseError):
    """验证错误异常类"""

    def __init__(
        self,
        message: str,
        field: str = None,
        validation_errors: List[Dict[str, Any]] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        """
        初始化验证错误异常

        Args:
            message: 错误信息
            field: 验证失败的字段
            validation_errors: 验证错误列表
            details: 其他详细信息
        """
        error_details = details or {}
        if field:
            error_details["field"] = field
        if validation_errors:
            error_details["validation_errors"] = validation_errors

        super().__init__(
            message=message, error_code="VALIDATION_ERROR", details=error_details
        )
        self.field = field
        self.validation_errors = validation_errors or []

    def add_validation_error(self, field: str, error: str, value: Any = None) -> None:
        """
        添加验证错误

        Args:
            field: 字段名
            error: 错误描述
            value: 导致错误的值
        """
        validation_error = {"field": field, "error": error}
        if value is not None:
            validation_error["value"] = value

        self.validation_errors.append(validation_error)
        self.details["validation_errors"] = self.validation_errors
