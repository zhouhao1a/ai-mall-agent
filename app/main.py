from fastapi import FastAPI
from app.api.v1 import user as user_api  # ← 导入你写的路由文件
import uvicorn

from app.core.exception_handers import biz_error_handler
from app.core.exceptions import BizError

app = FastAPI(title="AiMall 电商后端 API")
app.include_router(user_api.router)  # ← 把里面的接口挂到主应用上
app.add_exception_handler(BizError, biz_error_handler)
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
