from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.db_conn import get_db
from schemas.user import UserLogin
from service.login_service import user_login

router = APIRouter(tags=["系统层接口"])

@router.post("/login", summary="用户登录")
async def login(
    data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    return await user_login(db, data)