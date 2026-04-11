from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from models.user_health import UserHealth
from schemas.user_health import UserHealthCreate

async def submit_user_health(db: AsyncSession, data: UserHealthCreate):
    try:
        # 1. 先查用户是否存在
        result = await db.execute(select(User).where(User.username == data.username))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": 404, "message": "用户不存在"}
            )

        # 2. 用户存在 → 构建健康数据并插入
        health_data = UserHealth(**data.model_dump())

        db.add(health_data)
        await db.commit()

        return {
            "code": 200,
            "message": "用户健康数据保存成功"
        }
    except HTTPException:
        # 重新抛出 HTTPException，让全局异常处理器处理
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": 500, "message": f"保存健康数据失败: {str(e)}"}
        )