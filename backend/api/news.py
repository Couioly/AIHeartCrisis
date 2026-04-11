from fastapi import APIRouter
from service import news_service

router = APIRouter(tags=["用户层接口"])


@router.get("/news", summary="获取健康新闻资讯")
async def get_news():
    """
    获取健康新闻资讯接口
    
    从医脉通心血管内科页面获取最新的健康新闻资讯，
    包含新闻链接、标题、摘要、图片链接和发布时间。
    """
    return await news_service()
