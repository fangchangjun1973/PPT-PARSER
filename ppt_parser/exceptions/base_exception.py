"""
PPT解析器基础异常类定义
"""
from typing import Dict, Any, Optional


class PPTParserBaseError(Exception):
    """所有PPT解析器异常的基类"""

    def __init__(
        self, message: str, error_code: str, details: Optional[Dict[str, Any]] = None
    ):
        """
        初始化基础异常

        Args:
            message: 错误信息
            error_code: 错误代码
            details: 详细错误信息
        """
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        """格式化错误信息输出"""
        error_msg = f"[{self.error_code}] {self.message}"
        if self.details:
            error_msg += f"\n详细信息: {self.details}"
        return error_msg

    def add_detail(self, key: str, value: Any) -> None:
        """添加详细错误信息"""
        self.details[key] = value
