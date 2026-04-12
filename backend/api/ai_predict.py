from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models import get_db
from schemas import AIPredictData
from service import heart_disease_predict

router = APIRouter(tags=["问卷调查"])

@router.post("/ai-predict", summary="AI心脏病风险预测")
async def ai_predict(
    data: AIPredictData,
    db: AsyncSession = Depends(get_db)
):
    return await heart_disease_predict(db, data)