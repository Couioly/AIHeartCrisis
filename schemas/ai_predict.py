from pydantic import BaseModel
from models.test_data import YesNo, SexEnum


class AIPredictData(BaseModel):
    # 来源：用户数据 + 测试数据
    username: str = "admin"  # 测试数据自动变成 admin

    # 模型需要的全部字段（完全统一）
    heart_disease: YesNo
    bmi: float | None
    smoking: YesNo
    alcohol_drinking: YesNo
    stroke: YesNo
    physical_health: int | None
    mental_health: int | None
    diff_walking: YesNo
    sex: SexEnum
    age_category: str
    race: str
    diabetic: str
    physical_activity: YesNo
    gen_health: str
    sleep_time: int | None
    asthma: YesNo
    kidney_disease: YesNo
    skin_cancer: YesNo