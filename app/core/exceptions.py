"""
业务异常 BizError：表示用户可以理解的错误，比如手机号已注册。
用法：在 service 里 raise BizError("该手机号已注册", code=2001)。
由 app/core/exception_handlers.py 捕获，翻译成 HTTP 200 + 统一响应。
"""

class BizError(Exception):
    """业务异常：表示"用户可以理解的错误"，比如手机号已注册。"""
    def __init__(self, message: str, code: int = 1):
        self.message = message
        self.code = code
        super().__init__(message)
