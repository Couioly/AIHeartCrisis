from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models import get_db
from service import user_history_list
from service import query_historical_results
from service import get_history_analysis

router = APIRouter(tags=["用户层接口"])

@router.get("/history-list", summary="获取当前用户历史健康记录")
async def user_history(
    username: str,
    db: AsyncSession = Depends(get_db)
):
    return await user_history_list(db, username)


@router.get("/query-historical-results", summary="查询用户历史分析结果")
async def get_historical_results(
    username: str,
    db: AsyncSession = Depends(get_db)
):
    return await query_historical_results(db, username)


@router.get("/history-analysis", summary="查询指定健康记录的分析结果")
async def get_history_analysis_result(
    user_health_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await get_history_analysis(db, user_health_id)