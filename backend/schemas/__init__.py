from .user import UserLogin, UserCreate
from .user_health import UserHealthCreate
from .ai_chat import AIChatMessage, AIChatRequest, AIChatResponse
from .ai_predict import AIPredictData
from .news import NewsArticle, NewsResponse

__all__ = [
    'UserLogin',
    'UserCreate',
    'UserHealthCreate',
    'AIChatMessage',
    'AIChatRequest',
    'AIChatResponse',
    'AIPredictData',
    'NewsArticle',
    'NewsResponse',
]
