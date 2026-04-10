from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config.db_config import ASYNC_DATABASE_URL
import logging
import os
from datetime import datetime  # 用于获取当前日期

# 按日期生成日志文件
os.makedirs("logs", exist_ok=True)

# 获取当前日期 格式：xxxx-xx-xx
current_date = datetime.now().strftime("%Y-%m-%d")
log_filename = f"logs/{current_date}_sql.log"

# 配置 SQLAlchemy 日志
sql_logger = logging.getLogger('sqlalchemy.engine')
sql_logger.setLevel(logging.INFO)
sql_logger.propagate = False  # 禁止输出到控制台

# 文件处理器（按日期命名）
file_handler = logging.FileHandler(log_filename, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
sql_logger.addHandler(file_handler)

# 创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    # echo=True, # 打印SQL日志
    echo=False,
    pool_size=10,
    max_overflow=20
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()