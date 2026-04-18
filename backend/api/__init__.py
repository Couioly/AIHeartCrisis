from fastapi import APIRouter
from .submit import router as submit_router
from .login import router as login_router
from .register import router as register_router
from .history import router as history_router
from .ai_predict import router as ai_predict_router
from .ai_chat import router as ai_chat_router
from .news import router as news_router
from .proxy import router as proxy_router
from .get_test_data import router as get_test_data_router
from .questionnaire import router as questionnaire_router
from .medical_report import router as medical_report_router

api_router = APIRouter()

api_router.include_router(submit_router, prefix="/api/user")
api_router.include_router(login_router, prefix="/api")
api_router.include_router(register_router, prefix="/api")
api_router.include_router(history_router, prefix="/api/user")
api_router.include_router(ai_predict_router, prefix="/api")
api_router.include_router(ai_chat_router, prefix="/api/ai")
api_router.include_router(news_router, prefix="/api")
api_router.include_router(proxy_router, prefix="/api")
api_router.include_router(get_test_data_router, prefix="/api/db")
api_router.include_router(questionnaire_router, prefix="/api")
api_router.include_router(medical_report_router, prefix="/api")

__all__ = ['api_router']
