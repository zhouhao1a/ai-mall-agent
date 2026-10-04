"""
全局异常处理器：把 BizError 翻译成统一响应。
好处：service 抛异常后接口层完全不用 try/except，框架自动调用这里。
业务错误返回 HTTP 200（避免污染 500 告警），靠 body 里的 code 区分成败。
"""

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import BizError


async def biz_error_handler(request: Request, exc: BizError) -> JSONResponse:
    """把业务异常统一翻译成 {code, message, data} 格式的响应。"""
    return JSONResponse(
        status_code=200,
        content={"code": exc.code, "message": exc.message, "data": None},
    )
