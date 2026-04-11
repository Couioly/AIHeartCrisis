from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from models import get_db
from service import get_test_data_by_id

router = APIRouter(tags=["测试数据获取接口"])

@router.get("/get-test-data", summary="根据ID获取测试数据")
async def get_test_data(
    id: int = Query(..., description="数据ID，范围 1~319795"),
    db: AsyncSession = Depends(get_db)
):
    return await get_test_data_by_id(db, id)