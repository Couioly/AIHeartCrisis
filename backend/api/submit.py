from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.db_conn import get_db
from schemas.user_health import UserHealthCreate
from service.submit_service import submit_user_health

router = APIRouter(tags=["用户层接口"])

@router.post("/submit", summary="插入用户健康数据（还未接入AI）")
async def submit(
    data: UserHealthCreate,
    db: AsyncSession = Depends(get_db)
):
    return await submit_user_health(db, data)