from sqlalchemy import Column, Integer, String, DateTime, JSON, Float
from .base import Base


class Questionnaire(Base):
    """问卷表（单表存储）"""
    __tablename__ = "questionnaires"
    
    id = Column(Integer, primary_key=True, index=True, comment="问卷ID")
    username = Column(String(50), index=True, nullable=False, comment="用户名")
    submission_time = Column(DateTime, nullable=False, comment="提交时间")
    
    # 基本信息
    age = Column(String(20), comment="年龄范围")
    gender = Column(String(10), comment="性别")
    occupation = Column(String(50), comment="职业类别")
    education = Column(String(20), comment="最高学历")
    
    # 问卷回答（JSON格式）
    answers = Column(JSON, nullable=False, comment="问卷回答")
    
    # 健康数据
    blood_pressure = Column(String(20), comment="血压")
    blood_lipids = Column(String(50), comment="血脂")
    blood_sugar = Column(Float, comment="血糖")
    bmi = Column(Float, comment="体重指数")
    ecg = Column(String(50), comment="心电图")
    
    # 手环数据
    heart_rate = Column(Integer, comment="心率")
    blood_oxygen = Column(Integer, comment="血氧")
    
    # AI分析结果
    risk_level = Column(String(50), comment="风险等级")
