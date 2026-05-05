from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models import get_db
from service import get_history_analysis, query_historical_results

router = APIRouter(tags=["问卷调查"])


@router.get("/history", summary="查询指定健康记录的分析结果")
async def get_history_analysis_result(
    questionnaire_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await get_history_analysis(db, questionnaire_id)


@router.get("/history/list", summary="查询用户的历史分析结果列表")
async def get_history_list(
    username: str,
    db: AsyncSession = Depends(get_db)
):
    return await query_historical_results(db, username)
