import time
import random
from functools import wraps
from typing import Callable, Optional, Any, Dict

from .exceptions import RateLimitError, ServerError


def retry_on_failure(
    max_retries: int = 3, 
    backoff_factor: float = 1.0,
    exceptions: tuple = (RateLimitError, ServerError)
) -> Callable:
    """
    重试装饰器，用于处理临时错误
    
    Args:
        max_retries: 最大重试次数
        backoff_factor: 退避因子，每次重试的等待时间会增加
        exceptions: 需要重试的异常类型
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt >= max_retries:
                        raise
                    
                    # 计算退避时间: backoff_factor * (2 ** (attempt - 1)) + 随机延迟
                    wait_time = backoff_factor * (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(wait_time)
        
        return wrapper
    return decorator


def parse_iso_datetime(datetime_str: str) -> Optional[Dict]:
    """解析ISO格式的日期时间字符串"""
    if not datetime_str:
        return None
    
    try:
        # 尝试解析ISO格式
        from datetime import datetime
        dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        return {
            'year': dt.year,
            'month': dt.month,
            'day': dt.day,
            'hour': dt.hour,
            'minute': dt.minute,
            'second': dt.second,
            'timestamp': dt.timestamp()
        }
    except (ValueError, TypeError):
        return None
