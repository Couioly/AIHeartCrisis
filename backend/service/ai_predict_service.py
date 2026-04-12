from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import AIPredictData
from models import create_history
from config import DOUBAO_MODEL, PREDICTION_SYSTEM_PROMPT, get_client
from datetime import datetime

SYSTEM_PROMPT = PREDICTION_SYSTEM_PROMPT


# ===================== 核心预测服务 =====================
async def heart_disease_predict(db: AsyncSession, data: AIPredictData):
    try:
        # 1. 转字典
        input_dict = data.model_dump()
        
        # 2. 构建用户数据prompt
        user_data_prompt = \
            f"""用户健康数据：
            - age: {input_dict.get('age', 'None')}
            - gender: {input_dict.get('gender', 'None')}
            - occupation: {input_dict.get('occupation', 'None')}
            - education: {input_dict.get('education', 'None')}
            - answers: {input_dict.get('answers', 'None')}
            - blood_pressure: {input_dict.get('blood_pressure', 'None')}
            - blood_lipids: {input_dict.get('blood_lipids', 'None')}
            - blood_sugar: {input_dict.get('blood_sugar', 'None')}
            - bmi: {input_dict.get('bmi', 'None')}
            - ecg: {input_dict.get('ecg', 'None')}
            - heart_rate: {input_dict.get('heart_rate', 'None')}
            - blood_oxygen: {input_dict.get('blood_oxygen', 'None')}
            """
        
        # 3. 调用Doubao模型
        client = get_client()
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_data_prompt}
        ]
        
        response = client.chat.completions.create(
            model=DOUBAO_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=2000,
        )
        
        # 4. 解析模型响应
        assistant_message = response.choices[0].message.content
        
        # 5. 提取JSON内容 - 严格验证
        import json
        try:
            # 验证响应内容
            if not assistant_message or not assistant_message.strip():
                raise ValueError("AI模型返回空响应")
            
            # 提取JSON部分
            start = assistant_message.find('{')
            end = assistant_message.rfind('}') + 1
            if start == -1 or end == 0:
                raise ValueError("模型响应格式错误：未找到有效的JSON数据")
            
            prediction_data = json.loads(assistant_message[start:end])
            
            # 验证必需字段是否存在且格式正确
            if not isinstance(prediction_data.get("AI大模型PKL预测发病概率"), list):
                raise ValueError("预测概率数据格式不正确")
            
            if not isinstance(prediction_data.get("AI大模型分析"), dict):
                raise ValueError("分析数据格式不正确")
            
            # 验证分析数据中的必需字段
            analysis_data = prediction_data.get("AI大模型分析", {})
            if not analysis_data.get("风险等级"):
                raise ValueError("缺少风险等级信息")
            if not analysis_data.get("建议"):
                raise ValueError("缺少建议信息")
                
        except (json.JSONDecodeError, ValueError) as e:
            # 记录错误日志用于调试
            print(f"AI模型响应解析失败: {e}")
            print(f"原始响应内容: {assistant_message}")
            
            # 抛出明确的错误信息，而不是构造假数据
            raise HTTPException(
                status_code=500,
                detail={
                    "code": 500,
                    "message": "AI模型分析失败，请稍后重试",
                    "error": str(e)
                }
            )
        
        # 6. 构建响应数据
        response_data = {
            "username": input_dict["username"],
            "prediction": prediction_data
        }
        
        # 7. 存储AI分析结果到history表
        history_data = {
            "questionnaire_id": input_dict.get("questionnaire_id", 0),
            "username": input_dict["username"],
            "prediction_time": datetime.now(),
            "disease_probabilities": prediction_data.get("AI大模型PKL预测发病概率", []),
            "risk_level": prediction_data.get("AI大模型分析", {}).get("风险等级", "未知"),
            "high_probability_diseases": prediction_data.get("AI大模型分析", {}).get("高概率疾病", []),
            "diagnosis_basis": prediction_data.get("AI大模型分析", {}).get("病情依据", ""),
            "recommendations": prediction_data.get("AI大模型分析", {}).get("建议", "")
        }
        await create_history(db, history_data)
        
        # 8. 返回标准格式
        return {
            "code": 200,
            "message": "预测完成",
            "data": response_data
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": 500, "message": f"预测失败：{str(e)}"}
        )