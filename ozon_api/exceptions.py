class OzonAPIError(Exception):
    """Ozon API错误基类"""
    
    def __init__(self, message: str, response=None):
        super().__init__(message)
        self.message = message
        self.response = response
        self.status_code = response.status_code if response else None
    
    def __str__(self):
        if self.status_code:
            return f"Ozon API Error ({self.status_code}): {self.message}"
        return f"Ozon API Error: {self.message}"


class AuthenticationError(OzonAPIError):
    """认证错误"""
    pass


class RateLimitError(OzonAPIError):
    """请求频率限制错误"""
    pass


class InvalidRequestError(OzonAPIError):
    """无效请求错误"""
    pass


class ServerError(OzonAPIError):
    """服务器错误"""
    pass
