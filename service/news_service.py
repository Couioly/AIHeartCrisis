import asyncio
import aiohttp
from fastapi import HTTPException
from bs4 import BeautifulSoup
import fake_useragent
from schemas.news import NewsResponse, NewsArticle

async def get_heart_news():
    """从医脉通心血管内科页面获取新闻数据"""
    url = "https://www.medlive.cn/new/dep/heart/cms/1"
    headers = {
        "User-Agent": fake_useragent.UserAgent().random,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as resp:
                if resp.status == 200:
                    html_content = await resp.text()
                    soup = BeautifulSoup(html_content, 'html.parser')

                    # 查找新闻列表容器
                    news_container = soup.find('div', class_='info-list-box')
                    news_data = []

                    if news_container:
                        # 查找ul元素
                        ul_elem = news_container.find('ul')
                        if ul_elem:
                            # 查找所有li元素
                            li_items = ul_elem.find_all('li', class_='info-item')

                            for item in li_items:
                                # 提取标题和链接（找到info-title类的a标签）
                                title_elem = item.find('a', class_='info-title')
                                if title_elem:
                                    title = title_elem.get_text(strip=True)
                                    link = title_elem.get('href', '')
                                    if link and not link.startswith('http'):
                                        if link.startswith('/'):
                                            link = f"https://www.medlive.cn{link}"
                                        else:
                                            link = f"https://www.medlive.cn/{link}"
                                else:
                                    title = ''
                                    link = ''

                                # 提取摘要
                                summary_elem = item.find('p', class_='overflow-two')
                                summary = summary_elem.get_text(strip=True) if summary_elem else ''

                                # 提取发布时间
                                time_elem = item.find('span', class_='info-time')
                                publish_time = time_elem.get_text(strip=True) if time_elem else ''

                                # 提取图片链接
                                img_elem = item.find('img')
                                image_url = img_elem.get('src', '') if img_elem else ''
                                # 只在图片链接不是完整URL时添加前缀
                                if image_url and not image_url.startswith('http'):
                                    if image_url.startswith('/'):
                                        # 检查是否已经包含域名
                                        if not image_url.startswith('//'):
                                            image_url = f"https://www.medlive.cn{image_url}"
                                    else:
                                        image_url = f"https://www.medlive.cn/{image_url}"

                                if title and link:
                                    # 创建NewsArticle对象
                                    article = NewsArticle(
                                        url=link,
                                        title=title,
                                        content=summary,
                                        image_url=image_url,
                                        publish_time=publish_time
                                    )
                                    news_data.append(article)

                    # 使用NewsResponse模型返回数据
                    return NewsResponse(
                        code=200,
                        message="success",
                        data=news_data
                    )
                else:
                    return NewsResponse(
                        code=resp.status,
                        message=f"HTTP status {resp.status}",
                        data=[]
                    )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": 500, "message": f"新闻获取失败：{str(e)}"}
        )

async def news_service():
    """新闻服务"""
    try:
        result = await get_heart_news()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": 500, "message": f"新闻服务异常：{str(e)}"}
        )