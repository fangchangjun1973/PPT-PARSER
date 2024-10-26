
"""
解析错误异常类
用于处理JSON解析等数据解析过程中的错误
"""
from typing import Optional, Any, Dict
from .base_exception import PPTParserBaseError

class ParseError(PPTParserBaseError):
    """解析错误异常类"""
    
    def __init__(self, message: str, position: int = None, 
                 input_data: str = None, details: Optional[Dict[str, Any]] = None):
        """
        初始化解析错误异常
        
        Args:
            message: 错误信息
            position: 错误发生的位置
            input_data: 导致错误的输入数据
            details: 其他详细信息
        """
        error_details = details or {}
        if position is not None:
            error_details['position'] = position
        if input_data is not None:
            error_details['input_data'] = input_data
            
        super().__init__(
            message=message,
            error_code='PARSE_ERROR',
            details=error_details
        )
        self.position = position
        self.input_data = input_data