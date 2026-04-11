from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# 通用基类
class Base(DeclarativeBase):
    __abstract__ = True  # 不会单独创建表，只当父类

    # 创建时间：插入时自动赋值，不修改
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(),
        server_default=func.now(),
        comment="创建时间"
    )

    # 更新时间：插入/更新时自动刷新
    updated_at: Mapped[str] = mapped_column(
        TIMESTAMP(),
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间"
    )

