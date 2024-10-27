"""
核心模块日志配置
提供统一的日志记录机制
"""
import logging
from typing import Optional


class CoreLogger:
    """核心日志记录器"""

    _instance: Optional[logging.Logger] = None

    @classmethod
    def get_logger(cls) -> logging.Logger:
        """获取日志记录器单例"""
        if cls._instance is None:
            # 创建日志记录器
            logger = logging.getLogger("ppt_parser")
            logger.setLevel(logging.INFO)

            # 创建控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            # 设置日志格式
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            console_handler.setFormatter(formatter)

            logger.addHandler(console_handler)
            cls._instance = logger

        return cls._instance
