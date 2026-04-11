from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.db_conn import get_db
from schemas.ai_predict import AIPredictData
from service.ai_predict_service import heart_disease_predict

router = APIRouter(tags=["用户层接口"])

@router.post("/ai-predict", summary="AI心脏病风险预测")
async def ai_predict(
    data: AIPredictData,
    db: AsyncSession = Depends(get_db)
):
    return await heart_disease_predict(db, data)