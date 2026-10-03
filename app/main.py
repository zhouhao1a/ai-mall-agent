from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.api.v1 import user as user_api,category as  category_api  # ← 导入你写的路由文件
import uvicorn

from app.core.exception_handers import biz_error_handler
from app.core.exceptions import BizError

app = FastAPI(title="AiMall 电商后端 API")
app.include_router(user_api.router)  # ← 把里面的接口挂到主应用上
app.include_router(category_api.router)
app.add_exception_handler(BizError, biz_error_handler)

TIMER_PAGE = Path(__file__).resolve().parent / "static" / "timer.html"


@app.get("/", include_in_schema=False)
async def timer():
    return FileResponse(TIMER_PAGE)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
