import os
import json
import shutil
import uuid
import logging
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import MedicalReport, User
from .get_report_data_ai import extract_medical_info
from .multi_disease_predict_service import predict_diseases

logger = logging.getLogger(__name__)

FIELD_NAME_MAP = {
    "姓名": "subject_identifier",
    "性别": "sex",
    "年龄": "age",
    "检测日期": "time",
    "身高": "height",
    "体重": "weight",
    "BMI": "BMI",
    "体重指数": "BMI",
    "静息血压": "trestbps",
    "收缩压": "sysBP",
    "舒张压": "diaBP",
    "心率": "heartRate",
    "最大心率": "thalach",
    "胆固醇": "chol",
    "总胆固醇": "totChol",
    "空腹血糖": "fbs",
    "血糖": "glucose",
    "是否贫血": "anemia",
    "肌酐": "creatinin",
    "血小板": "platelets",
    "血清肌酐": "serum_creatinine",
    "钠": "sodium",
    "射血分数": "ejection",
    "量子指标": "Quantum",
    "是否吸烟": "smoke",
    "当前是否吸烟": "currentSmok",
    "每天吸烟数量": "cigsPerDay",
    "是否饮酒": "alco",
    "饮酒量": "Alcohol",
    "是否服用降压药": "BPMeds",
    "是否有糖尿病": "diabetes",
    "是否有高血压": "high_blood_pressure",
    "是否活跃": "active",
    "是否锻炼": "Exercise",
    "是否有家族病史": "Family_History",
    "是否无疾病": "No_Diseases",
    "压力水平": "stress",
    "睡眠质量": "Sleep",
    "糖摄入量": "sugar",
    "饮食质量": "diet",
    "是否肥胖": "obesity",
    "胸痛类型": "cp",
    "静息心电图结果": "restecg",
    "运动诱发心绞痛": "exang",
    "ST段压低": "oldpeak",
    "运动ST段斜率": "slope",
    "主要血管数量": "ca",
    "地中海贫血": "thal",
    "受试者": "subject",
    "第一导联段": "segment1",
    "第二导联段": "segment2",
    "第三导联段": "segment3",
    "第四导联段": "segment4",
    "数量": "Num",
    "是否有心脏病": "HeartDisease",
    "风险评分": "Risk",
    "是否死亡事件": "DEATH_EVENT"
}

def convert_field_names(data: dict) -> dict:
    """将中文字段名转换为英文字段名"""
    converted = {}
    for key, value in data.items():
        # 如果是中文字段名，转换为英文
        if key in FIELD_NAME_MAP:
            converted[FIELD_NAME_MAP[key]] = value
        elif key in FIELD_NAME_MAP.values():
            # 已经是英文字段名，直接使用
            converted[key] = value
        else:
            # 保留其他字段
            converted[key] = value
    
    # 确保一些特殊字段正确设置
    if "sex" in converted:
        converted["male"] = 1 if converted["sex"] == "男" else 0
    
    return converted


async def extract_report_data(file: UploadFile):
    file_location = None
    try:
        upload_dir = os.path.join(os.path.dirname(__file__), '..', 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        file_ext = os.path.splitext(file.filename)[1].lower() if file.filename else ''
        allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": 400, "message": f"不支持的文件格式，请上传 {', '.join(allowed_extensions)} 格式的文件"}
            )
        
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_location = os.path.join(upload_dir, unique_filename)
        
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"文件已保存: {file_location}")
        
        json_result = extract_medical_info(file_location)
        
        try:
            result_data = json.loads(json_result)
            
            if "error" in result_data:
                if file_location and os.path.exists(file_location):
                    os.remove(file_location)
                return {
                    "code": 400,
                    "message": result_data["error"],
                    "data": None
                }
            
            if file_location and os.path.exists(file_location):
                os.remove(file_location)
            
            return {
                "code": 200,
                "message": "提取成功",
                "data": result_data
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析失败: {str(e)}")
            if file_location and os.path.exists(file_location):
                os.remove(file_location)
            return {
                "code": 400,
                "message": "解析数据失败",
                "data": None
            }
            
    except HTTPException:
        if file_location and os.path.exists(file_location):
            try:
                os.remove(file_location)
            except:
                pass
        raise
    except Exception as e:
        logger.error(f"处理文件时发生错误: {str(e)}", exc_info=True)
        if file_location and os.path.exists(file_location):
            try:
                os.remove(file_location)
            except:
                pass
        return {
            "code": 500,
            "message": f"处理文件失败: {str(e)}",
            "data": None
        }


async def save_medical_report(db: AsyncSession, username: str, medical_data: dict):
    try:
        user_result = await db.execute(select(User).where(User.username == username))
        user = user_result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": 404, "message": "用户不存在"}
            )
        
        # 转换字段名
        converted_data = convert_field_names(medical_data)
        
        medical_report = MedicalReport(
            username=username,
            **converted_data
        )
        
        db.add(medical_report)
        await db.commit()
        await db.refresh(medical_report)
        
        try:
            ai_report_result = predict_diseases(medical_data)
            if ai_report_result:
                medical_report.ai_report_result = ai_report_result
                await db.commit()
                await db.refresh(medical_report)
                logger.info(f"AI疾病预测完成，已更新到记录 {medical_report.id}")
        except Exception as predict_error:
            logger.error(f"AI疾病预测失败: {str(predict_error)}", exc_info=True)
        
        return {
            "code": 200,
            "message": "保存成功",
            "data": {"id": medical_report.id, "ai_report_result": medical_report.ai_report_result}
        }
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"保存失败: {str(e)}"}
        )
