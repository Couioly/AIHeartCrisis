from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from schemas.user import UserCreate
from passlib.context import CryptContext
import re

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
USERNAME_PATTERN = re.compile(r'^[\u4e00-\u9fa5a-zA-Z0-9_]{3,16}$')


async def user_register(db: AsyncSession, data: UserCreate):
    try:
        if not data.username:
            raise HTTPException(status_code=400, detail={"code": 400, "message": "用户名不能为空"})
        if len(data.username) < 3 or len(data.username) > 50:
            raise HTTPException(status_code=400, detail={"code": 400, "message": "用户名长度必须在 3-50 位之间"})
        if ' ' in data.username:
            raise HTTPException(status_code=400, detail={"code": 400, "message": "用户名不能包含空格"})
        if not USERNAME_PATTERN.match(data.username):
            raise HTTPException(status_code=400, detail={"code": 400, "message": "用户名仅支持中文、英文、数字、下划线"})

        if not data.password:
            raise HTTPException(status_code=400, detail={"code": 400, "message": "密码不能为空"})
        if len(data.password) < 6 or len(data.password) > 20:
            raise HTTPException(status_code=400, detail={"code": 400, "message": "密码长度必须在 6-20 位之间"})
        if ' ' in data.password:
            raise HTTPException(status_code=400, detail={"code": 400, "message": "密码不能包含空格"})

        result = await db.execute(select(User).where(User.username == data.username))
        user = result.scalar_one_or_none()

        if user:
            raise HTTPException(status_code=400, detail={"code": 400, "message": "用户名已存在"})

        raw_password = data.password[:72]
        hashed_password = pwd_context.hash(raw_password)

        new_user = User(username=data.username, password=hashed_password)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return {
            "code": 200,
            "message": "注册成功",
            "data": {"username": new_user.username}
        }
    except HTTPException:
        # 重新抛出 HTTPException，让全局异常处理器处理
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": 500, "message": f"注册失败: {str(e)}"}
        )