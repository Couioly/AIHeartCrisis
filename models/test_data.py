from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DECIMAL, Enum, String
from models.base import Base
from enum import StrEnum

class YesNo(StrEnum):
    Yes = "Yes"
    No = "No"

class SexEnum(StrEnum):
    Male = "Male"
    Female = "Female"

# 定义用户健康表模型类
class TestData(Base):
    __tablename__ = "test_data"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    heart_disease: Mapped[YesNo] = mapped_column(Enum(YesNo), default=YesNo.No, comment="心脏病")
    bmi: Mapped[float | None] = mapped_column(DECIMAL(5, 2), comment="BMI")
    smoking: Mapped[YesNo] = mapped_column(Enum(YesNo), default=YesNo.No, comment="吸烟")
    alcohol_drinking: Mapped[YesNo] = mapped_column(Enum(YesNo), default=YesNo.No, comment="饮酒")
    stroke: Mapped[YesNo] = mapped_column(Enum(YesNo), default=YesNo.No, comment="中风")
    physical_health: Mapped[int | None] = mapped_column(comment="身体不适天数")
    mental_health: Mapped[int | None] = mapped_column(comment="心理不适天数")
    diff_walking: Mapped[YesNo] = mapped_column(Enum(YesNo), default=YesNo.No, comment="行走困难")
    sex: Mapped[SexEnum] = mapped_column(Enum(SexEnum), comment="性别")
    age_category: Mapped[str] = mapped_column(String(20), comment="年龄组")
    race: Mapped[str] = mapped_column(String(64), comment="种族")
    diabetic: Mapped[str] = mapped_column(String(64), comment="糖尿病")
    physical_activity: Mapped[YesNo] = mapped_column(Enum(YesNo), default=YesNo.No, comment="运动")
    gen_health: Mapped[str] = mapped_column(String(64), comment="健康自评")
    sleep_time: Mapped[int | None] = mapped_column(comment="睡眠时间")
    asthma: Mapped[YesNo] = mapped_column(Enum(YesNo), default=YesNo.No, comment="哮喘")
    kidney_disease: Mapped[YesNo] = mapped_column(Enum(YesNo), default=YesNo.No, comment="肾病")
    skin_cancer: Mapped[YesNo] = mapped_column(Enum(YesNo), default=YesNo.No, comment="皮肤癌")
