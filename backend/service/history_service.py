from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import History, User
from fastapi import HTTPException, status

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

        # 查询历史结果表
        history_result = await db.execute(
            select(History)
            .where(History.username == username)
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
                    "questionnaire_id": record.questionnaire_id,
                    "username": record.username,
                    "prediction_time": record.prediction_time,
                    "risk_level": record.risk_level,
                    "high_probability_diseases": record.high_probability_diseases,
                    "diagnosis_basis": record.diagnosis_basis,
                    "recommendations": record.recommendations,
                    "created_at": record.created_at
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

async def get_history_analysis(db: AsyncSession, questionnaire_id: int):
    try:
        # 查询指定questionnaire_id的历史分析结果
        history_result = await db.execute(
            select(History)
            .where(History.questionnaire_id == questionnaire_id)
        )
        history_record = history_result.scalar_one_or_none()

        # 如果没有找到记录
        if not history_record:
            return {
                "code": 404,
                "message": "未找到该记录的分析结果",
                "data": None
            }

        # 构建分析结果
        result_data = {
            "disease_probabilities": history_record.disease_probabilities,
            "AI大模型分析": {
                "风险等级": history_record.risk_level,
                "高概率疾病": history_record.high_probability_diseases,
                "病情依据": history_record.diagnosis_basis,
                "建议": history_record.recommendations
            }
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