from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models import get_db
from schemas import UserCreate
from service import user_register

router = APIRouter(tags=["用户层接口"])

@router.post("/register", summary="用户注册")
async def register(
    data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await user_register(db, data)