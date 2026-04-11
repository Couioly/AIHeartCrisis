from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User
from schemas import UserLogin
from passlib.context import CryptContext

# 密码验证工具
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def user_login(db: AsyncSession, data: UserLogin):
    try:
        # 1. 根据用户名查询
        result = await db.execute(select(User).where(User.username == data.username))
        user = result.scalar_one_or_none()

        # 2. 用户不存在
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": 404, "message": "用户不存在"}
            )

        # 3. 验证密码
        if not pwd_context.verify(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": 401, "message": "密码错误"}
            )

        # 4. 登录成功
        return {
            "code": 200,
            "message": "登录成功",
            "data": {
                "username": user.username
            }
        }
    except HTTPException:
        # 重新抛出 HTTPException，让全局异常处理器处理
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": 500, "message": f"登录失败: {str(e)}"}
        )