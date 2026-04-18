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
        
        medical_report = MedicalReport(
            username=username,
            **medical_data
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
