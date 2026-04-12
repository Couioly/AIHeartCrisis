from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


# 基本信息模型
class BasicInfo(BaseModel):
    age: str = Field(..., description="年龄范围")
    gender: str = Field(..., description="性别")
    occupation: str = Field(..., description="职业类别")
    education: str = Field(..., description="最高学历")


# 问卷回答模型
class AnswerItem(BaseModel):
    question_id: int = Field(..., description="问题编号")
    answer: Any = Field(..., description="答案，根据问题类型不同，格式也不同")


# 健康数据模型
class HealthData(BaseModel):
    blood_pressure: Optional[str] = Field(None, description="血压")
    blood_lipids: Optional[str] = Field(None, description="血脂")
    blood_sugar: Optional[float] = Field(None, description="血糖")
    bmi: Optional[float] = Field(None, description="BMI指数")
    ecg: Optional[str] = Field(None, description="心电图结果")


# 手环数据模型
class WearableData(BaseModel):
    heart_rate: Optional[int] = Field(None, description="心率")
    blood_oxygen: Optional[int] = Field(None, description="血氧")


# 问卷提交请求模型
class QuestionnaireSubmit(BaseModel):
    username: str = Field(..., description="用户名")
    submission_time: datetime = Field(..., description="提交时间")
    basic_info: BasicInfo = Field(..., description="基本信息")
    answers: List[AnswerItem] = Field(..., description="问卷回答")
    health_data: Optional[HealthData] = Field(None, description="健康数据")
    wearable_data: Optional[WearableData] = Field(None, description="手环数据")


# 问卷提交响应模型
class QuestionnaireResponse(BaseModel):
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="消息")
    data: Optional[Dict[str, Any]] = Field(None, description="返回数据")
    errors: Optional[List[str]] = Field(None, description="错误信息")


# 问卷列表响应模型
class QuestionnaireItem(BaseModel):
    id: int = Field(..., description="问卷ID")
    username: str = Field(..., description="用户名")
    submission_time: datetime = Field(..., description="提交时间")
    risk_level: str = Field(None, description="风险等级")


class QuestionnaireListResponse(BaseModel):
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="消息")
    data: Optional[List[QuestionnaireItem]] = Field(None, description="问卷列表")


# 问卷详情响应模型
class QuestionnaireDetailResponse(BaseModel):
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="消息")
    data: Optional[Dict[str, Any]] = Field(None, description="问卷详情")
