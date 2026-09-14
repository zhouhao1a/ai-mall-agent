class BizError(Exception):
    """业务异常：表示"用户可以理解的错误"，比如手机号已注册。"""

    def __init__(self, message: str, code: int = 1):
        self.message = message
        self.code = code
        super().__init__(message)