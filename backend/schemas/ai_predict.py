from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class AIPredictData(BaseModel):
    # 来源：用户数据 + 测试数据
    username: str = "admin"  # 测试数据自动变成 admin
    questionnaire_id: int | None = None  # 关联的问卷ID

    # 问卷调查的字段格式
    age: str | None = None
    gender: str | None = None
    occupation: str | None = None
    education: str | None = None
    answers: List[Dict[str, Any]] | None = None
    blood_pressure: str | None = None
    blood_lipids: str | None = None
    blood_sugar: float | None = None
    bmi: float | None = None
    ecg: str | None = None
    heart_rate: int | None = None
    blood_oxygen: int | None = None