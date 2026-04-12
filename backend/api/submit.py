from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models import get_db
from schemas import QuestionnaireSubmit, QuestionnaireResponse
from service import submit_questionnaire

router = APIRouter(tags=["问卷调查"])

@router.post("/questionnaires/submit", summary="提交问卷")
async def submit_questionnaire_endpoint(
    data: QuestionnaireSubmit,
    db: AsyncSession = Depends(get_db)
):
    """提交问卷"""
    return await submit_questionnaire(db, data)