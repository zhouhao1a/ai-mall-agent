from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import BizError


async def biz_error_handler(request: Request, exc: BizError) -> JSONResponse:
    """把业务异常统一翻译成 {code, message, data} 格式的响应。"""
    return JSONResponse(
        status_code=200,
        content={"code": exc.code, "message": exc.message, "data": None},
    )