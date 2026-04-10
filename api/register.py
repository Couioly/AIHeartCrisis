from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.db_conn import get_db
from schemas.user import UserCreate
from service.register_service import user_register

router = APIRouter(tags=["系统层接口"])

@router.post("/register", summary="用户注册")
async def register(
    data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await user_register(db, data)