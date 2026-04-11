from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
        comment="用户名"
    )
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="密码哈希"
    )
