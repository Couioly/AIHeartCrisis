from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Questionnaire, User
from fastapi import HTTPException, status
from schemas import QuestionnaireItem, QuestionnaireDetailResponse, QuestionnaireListResponse, QuestionnaireSubmit, QuestionnaireResponse, AIPredictData
from .ai_predict_service import heart_disease_predict



async def get_questionnaires(db: AsyncSession, username: str):
    """获取用户的问卷列表"""
    try:
        result = await db.execute(
            select(Questionnaire).where(Questionnaire.username == username)
        )
        questionnaires = result.scalars().all()
        
        if not questionnaires:
            return QuestionnaireListResponse(
                success=True,
                message="暂无问卷记录",
                data=[]
            )
        
        questionnaire_items = [
            QuestionnaireItem(
                id=q.id,
                username=q.username,
                submission_time=q.submission_time,
                risk_level=q.risk_level
            )
            for q in questionnaires
        ]
        
        return QuestionnaireListResponse(
            success=True,
            message="获取问卷列表成功",
            data=questionnaire_items
        )
    except Exception as e:
        return QuestionnaireListResponse(
            success=False,
            message="获取问卷列表失败",
            data=None
        )

async def get_questionnaire_detail(db: AsyncSession, questionnaire_id: int):
    """获取问卷详情"""
    try:
        # 获取问卷信息
        result = await db.execute(
            select(Questionnaire).where(Questionnaire.id == questionnaire_id)
        )
        questionnaire = result.scalars().first()
        
        if not questionnaire:
            return QuestionnaireDetailResponse(
                success=False,
                message="问卷不存在",
                data=None
            )
        
        # 构建返回数据
        detail_data = {
            "id": questionnaire.id,
            "username": questionnaire.username,
            "submission_time": questionnaire.submission_time,
            "created_at": questionnaire.created_at,
            "risk_level": questionnaire.risk_level,
            "basic_info": {
                "age": questionnaire.age,
                "gender": questionnaire.gender,
                "occupation": questionnaire.occupation,
                "education": questionnaire.education
            },
            "answers": questionnaire.answers,
            "health_data": {
                "blood_pressure": questionnaire.blood_pressure,
                "blood_lipids": questionnaire.blood_lipids,
                "blood_sugar": questionnaire.blood_sugar,
                "bmi": questionnaire.bmi,
                "ecg": questionnaire.ecg
            },
            "wearable_data": {
                "heart_rate": questionnaire.heart_rate,
                "blood_oxygen": questionnaire.blood_oxygen
            }
        }
        
        return QuestionnaireDetailResponse(
            success=True,
            message="获取问卷详情成功",
            data=detail_data
        )
    except Exception as e:
        return QuestionnaireDetailResponse(
            success=False,
            message="获取问卷详情失败",
            data=None
        )


async def submit_questionnaire(db: AsyncSession, data: QuestionnaireSubmit):
    """提交问卷"""
    try:
        # 构建问卷数据
        questionnaire_data = {
            "username": data.username,
            "submission_time": data.submission_time,
            "age": data.basic_info.age,
            "gender": data.basic_info.gender,
            "occupation": data.basic_info.occupation,
            "education": data.basic_info.education,
            "answers": [
                {
                    "question_id": item.question_id,
                    "answer": item.answer,
                    "is_core": item.question_id in [6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27]
                }
                for item in data.answers
            ]
        }
        
        # 添加健康数据
        if data.health_data:
            questionnaire_data.update({
                "blood_pressure": data.health_data.blood_pressure,
                "blood_lipids": data.health_data.blood_lipids,
                "blood_sugar": data.health_data.blood_sugar,
                "bmi": data.health_data.bmi,
                "ecg": data.health_data.ecg
            })
        
        # 添加手环数据
        if data.wearable_data:
            questionnaire_data.update({
                "heart_rate": data.wearable_data.heart_rate,
                "blood_oxygen": data.wearable_data.blood_oxygen
            })
        
        # 创建问卷记录
        questionnaire = Questionnaire(**questionnaire_data)
        db.add(questionnaire)
        await db.commit()
        await db.refresh(questionnaire)
        
        # 调用AI大模型接口进行分析
        try:
            # 构建AI预测数据
            ai_predict_data = AIPredictData(
                username=data.username,
                questionnaire_id=questionnaire.id,
                age=data.basic_info.age,
                gender=data.basic_info.gender,
                occupation=data.basic_info.occupation,
                education=data.basic_info.education,
                answers=questionnaire.answers,
                blood_pressure=data.health_data.blood_pressure if data.health_data else None,
                blood_lipids=data.health_data.blood_lipids if data.health_data else None,
                blood_sugar=data.health_data.blood_sugar if data.health_data else None,
                bmi=data.health_data.bmi if data.health_data else None,
                ecg=data.health_data.ecg if data.health_data else None,
                heart_rate=data.wearable_data.heart_rate if data.wearable_data else None,
                blood_oxygen=data.wearable_data.blood_oxygen if data.wearable_data else None
            )
            
            # 调用AI预测服务
            ai_response = await heart_disease_predict(db, ai_predict_data)
            
            # 提取风险等级
            if ai_response and "data" in ai_response and "prediction" in ai_response["data"]:
                prediction = ai_response["data"]["prediction"]
                if "AI大模型分析" in prediction and "风险等级" in prediction["AI大模型分析"]:
                    risk_level = prediction["AI大模型分析"]["风险等级"]
                    # 更新问卷记录的风险等级
                    questionnaire.risk_level = risk_level
                    await db.commit()
                    await db.refresh(questionnaire)
        except Exception as ai_error:
            # AI分析失败不影响问卷提交
            print(f"AI分析失败: {ai_error}")
        
        return QuestionnaireResponse(
            success=True,
            message="问卷提交成功",
            data={
                "questionnaire_id": questionnaire.id,
                "submission_time": data.submission_time,
                "risk_level": questionnaire.risk_level
            }
        )
    except Exception as e:
        await db.rollback()
        return QuestionnaireResponse(
            success=False,
            message="问卷提交失败",
            errors=[str(e)]
        )
