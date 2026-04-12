from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from .base import Base


class History(Base):
    """分析结果表"""
    __tablename__ = "history"
    
    id = Column(Integer, primary_key=True, index=True, comment="分析结果ID")
    questionnaire_id = Column(Integer, ForeignKey("questionnaires.id"), comment="关联问卷ID")
    username = Column(String(50), index=True, nullable=False, comment="用户名")
    prediction_time = Column(DateTime, nullable=False, comment="预测时间")
    
    # AI分析结果（JSON格式）
    disease_probabilities = Column(JSON, nullable=False, comment="疾病概率")
    risk_level = Column(String(50), comment="风险等级")
    high_probability_diseases = Column(JSON, comment="高概率疾病")
    diagnosis_basis = Column(String(500), comment="病情依据")
    recommendations = Column(String(500), comment="建议")


async def create_history(db, data):
    # 检查data是否为字典，如果是则直接传递给History构造函数
    if isinstance(data, dict):
        db_history = History(**data)
    else:
        # 否则假设是Pydantic模型，调用model_dump()
        db_history = History(**data.model_dump())
    db.add(db_history)
    await db.commit()
    await db.refresh(db_history)
    return db_history
