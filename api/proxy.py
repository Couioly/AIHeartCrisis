from fastapi import APIRouter, HTTPException, Query
import aiohttp

router = APIRouter(tags=["系统层接口"])


@router.get("/proxy/image", summary="图片代理接口")
async def proxy_image(url: str = Query(..., description="原始图片URL")):
    """
    图片代理接口，用于解决CORS问题
    
    - **url**: 原始图片URL
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                if resp.status == 200:
                    content = await resp.read()
                    content_type = resp.headers.get("Content-Type", "image/jpeg")
                    # 确保返回正确的Content-Type
                    if content_type == "$mime":
                        # 根据文件扩展名猜测Content-Type
                        if url.lower().endswith(".jpg") or url.lower().endswith(".jpeg"):
                            content_type = "image/jpeg"
                        elif url.lower().endswith(".png"):
                            content_type = "image/png"
                        elif url.lower().endswith(".gif"):
                            content_type = "image/gif"
                        else:
                            content_type = "image/jpeg"
                    
                    from fastapi.responses import Response
                    return Response(content=content, media_type=content_type)
                else:
                    raise HTTPException(status_code=resp.status, detail=f"图片获取失败: {resp.status}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"代理请求失败: {str(e)}")
