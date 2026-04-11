from fastapi import HTTPException
from schemas.ai_chat import AIChatRequest
from config.ai_config import DOUBAO_MODEL, CHAT_SYSTEM_PROMPT, get_client

SYSTEM_PROMPT = CHAT_SYSTEM_PROMPT


async def ai_chat_service(request: AIChatRequest):
    try:
        client = get_client()
        
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        for msg in request.messages:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        response = client.chat.completions.create(
            model=DOUBAO_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=2000,
        )
        
        assistant_message = response.choices[0].message.content
        
        return {
            "code": 200,
            "message": "success",
            "data": {
                "response": assistant_message,
                "model": DOUBAO_MODEL,
                "user_id": request.user_id
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": 500, "message": f"AI服务异常：{str(e)}"}
        )
