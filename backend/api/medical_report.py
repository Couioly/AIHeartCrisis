from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from models import get_db
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
