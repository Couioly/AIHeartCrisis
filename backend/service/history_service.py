from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from models import UserHealth, History, User
from fastapi import HTTPException, status

async def user_history_list(db: AsyncSession, username: str):
    try:
        # 先检查用户是否存在
        user_result = await db.execute(select(User).where(User.username == username))
        user = user_result.scalar_one_or_none()

        # 不存在 → 直接抛错
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": 404, "message": "用户不存在"}
            )

        # 用户存在 → 再查询健康记录
        result = await db.execute(
            select(UserHealth)
            .where(UserHealth.username == username)
            .order_by(UserHealth.id.desc())
        )
        records = result.scalars().all()

        # 如果没有记录
        if not records:
            return {
                "code": 200,
                "message": "暂无历史记录",
                "data": []
            }

        # 返回记录列表
        return {
            "code": 200,
            "message": "查询成功",
            "data": [
                {
                    "id": record.id,
                    "heart_disease": record.heart_disease,
                    "bmi": record.bmi,
                    "smoking": record.smoking,
                    "alcohol_drinking": record.alcohol_drinking,
                    "stroke": record.stroke,
                    "physical_health": record.physical_health,
                    "mental_health": record.mental_health,
                    "diff_walking": record.diff_walking,
                    "sex": record.sex,
                    "age_category": record.age_category,
                    "race": record.race,
                    "diabetic": record.diabetic,
                    "physical_activity": record.physical_activity,
                    "gen_health": record.gen_health,
                    "sleep_time": record.sleep_time,
                    "asthma": record.asthma,
                    "kidney_disease": record.kidney_disease,
                    "skin_cancer": record.skin_cancer,
                    "created_at": record.created_at
                }
                for record in records
            ]
        }
    except HTTPException:
        # 重新抛出 HTTPException，让全局异常处理器处理
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": 500, "message": f"查询历史记录失败: {str(e)}"}
        )

async def query_historical_results(db: AsyncSession, username: str):
    try:
        # 先检查用户是否存在
        user_result = await db.execute(select(User).where(User.username == username))
        user = user_result.scalar_one_or_none()

        # 不存在 → 直接抛错
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": 404, "message": "用户不存在"}
            )

        # 用户存在 → 查询该用户的健康记录
        user_health_result = await db.execute(
            select(UserHealth.id)
            .where(UserHealth.username == username)
        )
        user_health_ids = [id[0] for id in user_health_result.all()]

        # 如果没有健康记录
        if not user_health_ids:
            return {
                "code": 200,
                "message": "暂无历史记录",
                "data": []
            }

        # 查询历史结果表
        history_result = await db.execute(
            select(History)
            .where(History.user_health_id.in_(user_health_ids))
            .order_by(History.created_at.desc())
        )
        history_records = history_result.scalars().all()

        # 如果没有历史结果记录
        if not history_records:
            return {
                "code": 200,
                "message": "暂无历史分析结果",
                "data": []
            }

        # 返回历史结果列表
        return {
            "code": 200,
            "message": "查询成功",
            "data": [
                {
                    "id": record.id,
                    "user_health_id": record.user_health_id,
                    "result": record.result,
                    "created_at": record.created_at,
                    "updated_at": record.updated_at
                }
                for record in history_records
            ]
        }
    except HTTPException:
        # 重新抛出 HTTPException，让全局异常处理器处理
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": 500, "message": f"查询历史分析结果失败: {str(e)}"}
        )

async def get_history_analysis(db: AsyncSession, user_health_id: int):
    try:
        # 查询指定user_health_id的历史分析结果
        history_result = await db.execute(
            select(History)
            .where(History.user_health_id == user_health_id)
        )
        history_record = history_result.scalar_one_or_none()

        # 如果没有找到记录
        if not history_record:
            return {
                "code": 404,
                "message": "未找到该记录的分析结果",
                "data": None
            }

        # 解析result字段（JSON字符串）
        import json
        try:
            result_data = json.loads(history_record.result)
        except json.JSONDecodeError:
            return {
                "code": 500,
                "message": "分析结果解析失败",
                "data": None
            }

        # 返回分析结果
        return {
            "code": 200,
            "message": "查询成功",
            "data": result_data
        }
    except HTTPException:
        # 重新抛出 HTTPException，让全局异常处理器处理
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": 500, "message": f"查询分析结果失败: {str(e)}"}
        )