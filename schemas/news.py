from pydantic import BaseModel
from typing import List, Dict


class NewsArticle(BaseModel):
    url: str
    title: str
    content: str
    image_url: str
    publish_time: str = ""


class NewsResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: List[NewsArticle]
