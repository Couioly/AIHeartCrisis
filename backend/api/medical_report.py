from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import get_db, MedicalReport
from schemas import MedicalReportSaveRequest
from service import extract_report_data, save_medical_report
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["体检报告"])


@router.post("/medical-report/upload", summary="上传体检报告并提取数据")
async def upload_medical_report(
    file: UploadFile = File(..., description="体检报告文件（支持PDF、JPG、PNG）")
):
    """
    上传体检报告文件（PDF或图片），自动提取数据并返回JSON格式结果
    
    - **file**: 体检报告文件，支持PDF、JPG、PNG格式
    """
    try:
        if not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": 400, "message": "请上传文件"}
            )
        
        logger.info(f"收到文件上传请求: {file.filename}, 类型: {file.content_type}")
        
        return await extract_report_data(file)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"处理上传文件时出错: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 500, "message": f"处理文件失败: {str(e)}"}
        )


@router.post("/medical-report/save", summary="保存体检报告数据")
async def save_medical_report_endpoint(
    request: MedicalReportSaveRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    保存修改后的体检报告数据到数据库
    
    - **username**: 用户名
    - **medical_data**: 体检报告数据字典
    """
    return await save_medical_report(db, request.username, request.medical_data)


@router.get("/medical-report/latest", summary="获取用户最新体检报告")
async def get_latest_medical_report(
    username: str,
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户最新的体检报告
    
    - **username**: 用户名
    """
    try:
        result = await db.execute(
            select(MedicalReport)
            .where(MedicalReport.username == username)
            .order_by(MedicalReport.created_at.desc())
            .limit(1)
        )
        latest_report = result.scalar_one_or_none()
        
        if not latest_report:
            return {
                "code": 404,
                "message": "暂无体检报告",
                "data": None
            }
        
        # 收集所有体检数据字段
        report_data = {}
        for column in MedicalReport.__table__.columns:
            if column.name not in ['id', 'username', 'created_at', 'ai_report_result']:
                value = getattr(latest_report, column.name)
                if value is not None and value != '':
                    report_data[column.name] = value
        
        return {
            "code": 200,
            "message": "获取成功",
            "data": {
                "id": latest_report.id,
                "username": latest_report.username,
                "created_at": latest_report.created_at,
                "report_data": report_data,
                "ai_report_result": latest_report.ai_report_result
            }
        }
    except Exception as e:
        logger.error(f"获取体检报告失败: {str(e)}", exc_info=True)
        return {
            "code": 500,
            "message": f"获取体检报告失败: {str(e)}",
            "data": None
        }
