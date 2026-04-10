from pydantic import BaseModel
from typing import Optional


class AIChatMessage(BaseModel):
    role: str
    content: str


class AIChatRequest(BaseModel):
    messages: list[AIChatMessage]
    user_id: Optional[str] = None


class AIChatResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: dict
