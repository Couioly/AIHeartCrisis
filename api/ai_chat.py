from fastapi import APIRouter
from schemas.ai_chat import AIChatRequest
from service.ai_chat_service import ai_chat_service

router = APIRouter(tags=["用户层接口"])


@router.post("/ai-chat", summary="AI健康咨询对话")
async def ai_chat(request: AIChatRequest):
    """
    AI健康咨询对话接口
    
    - **messages**: 对话消息列表，每条消息包含role(user/assistant)和content
    - **user_id**: 可选的用户标识
    
    注意：本接口仅提供健康相关咨询服务，不提供医疗诊断
    """
    return await ai_chat_service(request)
