from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models import get_db
from schemas import (
    QuestionnaireListResponse, QuestionnaireDetailResponse
)
from service import get_questionnaires, get_questionnaire_detail

router = APIRouter(tags=["问卷调查"])

@router.get("/questionnaires/user", summary="获取用户的问卷列表", response_model=QuestionnaireListResponse)
async def get_questionnaires_route(
    username: str,
    db: AsyncSession = Depends(get_db)
):
    """获取用户的问卷列表"""
    return await get_questionnaires(db, username)


@router.get("/questionnaires/id", summary="获取问卷详情", response_model=QuestionnaireDetailResponse)
async def get_questionnaire_detail_route(
    questionnaire_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取问卷详情"""
    return await get_questionnaire_detail(db, questionnaire_id)

