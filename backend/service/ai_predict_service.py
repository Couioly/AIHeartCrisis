from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import AIPredictData
from models import create_user_health, create_history
from config import DOUBAO_MODEL, PREDICTION_SYSTEM_PROMPT, get_client

SYSTEM_PROMPT = PREDICTION_SYSTEM_PROMPT


# ===================== 核心预测服务 =====================
async def heart_disease_predict(db: AsyncSession, data: AIPredictData):
    try:
        # 1. 转字典
        input_dict = data.model_dump()
        
        # 2. 存储用户健康数据到user_health表
        user_health_data = AIPredictData(**input_dict)
        user_health = await create_user_health(db, user_health_data)
        
        # 3. 构建用户数据prompt
        user_data_prompt = f"""用户健康数据：
- username: {input_dict['username']}
- age_category: {input_dict['age_category']}
- sex: {input_dict['sex']}
- bmi: {input_dict['bmi']}
- smoking: {input_dict['smoking']}
- alcohol_drinking: {input_dict['alcohol_drinking']}
- stroke: {input_dict['stroke']}
- physical_health: {input_dict['physical_health']}
- mental_health: {input_dict['mental_health']}
- diff_walking: {input_dict['diff_walking']}
- race: {input_dict['race']}
- diabetic: {input_dict['diabetic']}
- physical_activity: {input_dict['physical_activity']}
- gen_health: {input_dict['gen_health']}
- sleep_time: {input_dict['sleep_time']}
- asthma: {input_dict['asthma']}
- kidney_disease: {input_dict['kidney_disease']}
- skin_cancer: {input_dict['skin_cancer']}
"""
        
        # 4. 调用Doubao模型
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
        
        # 5. 解析模型响应
        assistant_message = response.choices[0].message.content
        
        # 6. 提取JSON内容
        import json
        try:
            # 提取JSON部分
            start = assistant_message.find('{')
            end = assistant_message.rfind('}') + 1
            if start != -1 and end != 0:
                prediction_data = json.loads(assistant_message[start:end])
            else:
                # 如果没有JSON格式，使用默认值
                prediction_data = {
                    "risk_percent": "25.00",
                    "risk_level": "中等风险",
                    "analysis": "无法解析模型响应",
                    "suggestions": "请咨询医生获取专业建议"
                }
        except Exception as e:
            # 解析失败时使用默认值
            prediction_data = {
                "risk_percent": "25.00",
                "risk_level": "中等风险",
                "analysis": f"解析模型响应失败: {str(e)}",
                "suggestions": "请咨询医生获取专业建议"
            }
        
        # 7. 构建响应数据
        response_data = {
            "username": input_dict["username"],
            "heart_disease_risk": f"{prediction_data['risk_percent']}%",
            "risk_level": prediction_data['risk_level'],
            "analysis": prediction_data.get('analysis', ''),
            "suggestions": prediction_data.get('suggestions', '')
        }
        
        # 8. 存储AI分析结果到history表
        history_data = {
            "user_health_id": user_health.id,
            "result": json.dumps(response_data)
        }
        await create_history(db, history_data)
        
        # 9. 返回标准格式
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