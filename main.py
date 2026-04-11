from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from api import api_router # 导入聚合后的总路由
import traceback

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI心脏预警接口")

# CORS 预检请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境请指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 挂载所有 API 路由
app.include_router(api_router)

# 全局异常处理器
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # 打印异常堆栈信息到控制台，便于调试
    print(f"[ERROR] {exc}")
    traceback.print_exc()
    
    # 检查是否已经是 HTTPException
    if isinstance(exc, HTTPException):
        # 如果是 HTTPException，直接返回其内容
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail
        )
    else:
        # 其他未捕获的异常，返回 500 错误
        return JSONResponse(
            status_code=500,
            content={"code": 500, "message": f"服务器内部错误: {str(exc)}"}
        )

# 启动应用时建表
async def create_tables():
    try:
        from models.db_conn import async_engine
        from models.base import Base
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

            # 此处自动创建数据表会报错，采用手动创建
            # from models.user import User
            # from models.user_health import UserHealth
            # from models.history import History
            # await conn.run_sync(Base.metadata.tables["history"].create)
            # await conn.run_sync(Base.metadata.tables["user"].create)
            # await conn.run_sync(Base.metadata.tables["user_health"].create)

    except Exception as e:
        print(f"[ERROR] 创建表失败: {str(e)}")
        traceback.print_exc()

@app.on_event("startup")
async def startup_event():
    await create_tables()

@app.get("/")
async def root():
    return FileResponse("config/index.html")


print("\033[1;31mdosc-site\thttp://localhost:8000/docs\033[0m")
