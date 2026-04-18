from pydantic import BaseModel
from typing import Optional, Dict, Any


class MedicalReportSaveRequest(BaseModel):
    username: str
    medical_data: Dict[str, Any]


class MedicalReportUploadResponse(BaseModel):
    code: int
    message: str
    data: Optional[Dict[str, Any]] = None


class MedicalReportSaveResponse(BaseModel):
    code: int
    message: str
    data: Optional[Dict[str, Any]] = None
