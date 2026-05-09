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
        
        # 添加体检报告AI预测结果
        medical_report_ai_result = input_dict.get('medical_report_ai_result')
        if medical_report_ai_result:
            user_data_prompt += f"""
            【体检报告AI预测结果】（重要参考，请优先考虑）：
            {str(medical_report_ai_result)}
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
            if analysis_data.get("综合风险分数") is None:
                raise ValueError("缺少综合风险分数")
            if not analysis_data.get("风险等级"):
                raise ValueError("缺少风险等级信息")
            if not analysis_data.get("建议"):
                raise ValueError("缺少建议信息")
            
            # 可选字段：图表数据（如果不存在，设置为默认值）
            if "雷达图数据" not in prediction_data:
                prediction_data["雷达图数据"] = {"labels": [], "values": []}
            if "柱状图数据" not in prediction_data:
                prediction_data["柱状图数据"] = []
            if "健康仪表盘数据" not in prediction_data:
                prediction_data["健康仪表盘数据"] = {}
            if "数据来源" not in prediction_data:
                prediction_data["数据来源"] = ["问卷数据"]
                
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
        
        # 6. 根据用户真实输入过滤AI返回的数据（双重保障）
        # 记录用户真实提供了哪些健康数据
        user_provided_data = {
            "blood_pressure": input_dict.get("blood_pressure"),
            "blood_lipids": input_dict.get("blood_lipids"),
            "blood_sugar": input_dict.get("blood_sugar"),
            "bmi": input_dict.get("bmi"),
            "ecg": input_dict.get("ecg"),
            "heart_rate": input_dict.get("heart_rate"),
            "blood_oxygen": input_dict.get("blood_oxygen")
        }
        
        # 过滤健康仪表盘数据 - 只保留用户真实填写的
        if "健康仪表盘数据" in prediction_data:
            filtered_dashboard = {}
            dashboard_keys = ["heart_rate", "blood_pressure", "blood_oxygen", "blood_sugar", "bmi"]
            for key in dashboard_keys:
                # 检查用户是否提供了对应的数据
                user_key = key
                if key == "heart_rate":
                    user_key = "heart_rate"
                elif key == "blood_pressure":
                    user_key = "blood_pressure"
                elif key == "blood_oxygen":
                    user_key = "blood_oxygen"
                elif key == "blood_sugar":
                    user_key = "blood_sugar"
                elif key == "bmi":
                    user_key = "bmi"
                
                if user_provided_data.get(user_key) not in [None, "None", ""]:
                    if key in prediction_data["健康仪表盘数据"]:
                        filtered_dashboard[key] = prediction_data["健康仪表盘数据"][key]
            prediction_data["健康仪表盘数据"] = filtered_dashboard
        
        # 过滤雷达图数据
        if "雷达图数据" in prediction_data:
            radar_labels = prediction_data["雷达图数据"]["labels"]
            radar_values = prediction_data["雷达图数据"]["values"]
            filtered_radar_labels = []
            filtered_radar_values = []
            
            # 可从问卷推断的风险因素（总是保留）
            inference_factors = ["睡眠", "工作压力", "饮食习惯", "运动情况"]
            
            for i, label in enumerate(radar_labels):
                # 检查是否是可推断的因素，或者用户真实提供的健康指标
                is_inference_factor = any(factor in label for factor in inference_factors)
                is_user_provided = False
                
                # 检查是否是健康指标且用户提供了数据
                health_indicator_map = {
                    "血压": "blood_pressure",
                    "血糖": "blood_sugar",
                    "血脂": "blood_lipids",
                    "心率": "heart_rate",
                    "血氧": "blood_oxygen",
                    "BMI": "bmi"
                }
                
                for indicator, user_key in health_indicator_map.items():
                    if indicator in label and user_provided_data.get(user_key) not in [None, "None", ""]:
                        is_user_provided = True
                        break
                
                if is_inference_factor or is_user_provided:
                    filtered_radar_labels.append(label)
                    filtered_radar_values.append(radar_values[i])
            
            prediction_data["雷达图数据"] = {
                "labels": filtered_radar_labels,
                "values": filtered_radar_values
            }
        
        # 过滤柱状图数据
        if "柱状图数据" in prediction_data:
            filtered_bar_data = []
            
            for item in prediction_data["柱状图数据"]:
                name = item.get("name", "")
                # 检查是否是可推断的因素，或者用户真实提供的健康指标
                is_inference_factor = any(factor in name for factor in ["睡眠", "工作压力", "饮食习惯", "运动情况"])
                is_user_provided = False
                
                health_indicator_map = {
                    "血压": "blood_pressure",
                    "血糖": "blood_sugar",
                    "血脂": "blood_lipids",
                    "心率": "heart_rate",
                    "血氧": "blood_oxygen",
                    "BMI": "bmi"
                }
                
                for indicator, user_key in health_indicator_map.items():
                    if indicator in name and user_provided_data.get(user_key) not in [None, "None", ""]:
                        is_user_provided = True
                        break
                
                if is_inference_factor or is_user_provided:
                    filtered_bar_data.append(item)
            
            prediction_data["柱状图数据"] = filtered_bar_data

        # 7. 构建响应数据
        response_data = {
            "username": input_dict["username"],
            "prediction": prediction_data
        }

        # 8. 存储AI分析结果到history表
        history_data = {
            "questionnaire_id": input_dict.get("questionnaire_id", 0),
            "username": input_dict["username"],
            "prediction_time": datetime.now(),
            "disease_probabilities": prediction_data.get("AI大模型PKL预测发病概率", []),
            "risk_level": prediction_data.get("AI大模型分析", {}).get("风险等级", "未知"),
            "high_probability_diseases": prediction_data.get("AI大模型分析", {}).get("高概率疾病", []),
            "diagnosis_basis": prediction_data.get("AI大模型分析", {}).get("病情依据", ""),
            "recommendations": prediction_data.get("AI大模型分析", {}).get("建议", ""),
            "full_prediction_result": prediction_data
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