from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Text
from models.base import Base

# 定义历史记录表模型类
class History(Base):
    __tablename__ = "history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="历史记录ID")
    user_health_id: Mapped[int] = mapped_column(ForeignKey("user_health.id"), comment="关联用户健康记录ID")
    result: Mapped[str] = mapped_column(Text, comment="AI分析结果")


async def create_history(db, data):
    # 检查data是否为字典，如果是则直接传递给History构造函数
    if isinstance(data, dict):
        db_history = History(**data)
    else:
        # 否则假设是Pydantic模型，调用model_dump()
        db_history = History(**data.model_dump())
    db.add(db_history)
    await db.commit()
    await db.refresh(db_history)
    return db_history
