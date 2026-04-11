from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import TestData

async def get_test_data_by_id(db: AsyncSession, data_id: int):
    try:
        # ===================== ID 范围校验（1 ~ 319795） =====================
        if data_id < 1 or data_id > 319795:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": 400,
                    "message": "ID 超出合法范围，允许的范围：1 ~ 319795"
                }
            )

        # 根据 ID 查询测试数据
        result = await db.execute(
            select(TestData).where(TestData.id == data_id)
        )
        data = result.scalar_one_or_none()

        # 数据不存在
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": 404, "message": "测试数据不存在"}
            )

        # 返回数据
        return {
            "code": 200,
            "message": "查询成功",
            "data": {
                "id": data.id,
                "heart_disease": data.heart_disease,
                "bmi": data.bmi,
                "smoking": data.smoking,
                "alcohol_drinking": data.alcohol_drinking,
                "stroke": data.stroke,
                "physical_health": data.physical_health,
                "mental_health": data.mental_health,
                "diff_walking": data.diff_walking,
                "sex": data.sex,
                "age_category": data.age_category,
                "race": data.race,
                "diabetic": data.diabetic,
                "physical_activity": data.physical_activity,
                "gen_health": data.gen_health,
                "sleep_time": data.sleep_time,
                "asthma": data.asthma,
                "kidney_disease": data.kidney_disease,
                "skin_cancer": data.skin_cancer
            }
        }
    except HTTPException:
        # 重新抛出 HTTPException，让全局异常处理器处理
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": 500, "message": f"查询测试数据失败: {str(e)}"}
        )