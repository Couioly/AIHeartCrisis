from pydantic import BaseModel
from models.user_health import YesNo, SexEnum

class UserHealthCreate(BaseModel):
    username: str
    heart_disease: YesNo = YesNo.No
    bmi: float | None = None
    smoking: YesNo = YesNo.No
    alcohol_drinking: YesNo = YesNo.No
    stroke: YesNo = YesNo.No
    physical_health: int | None = None
    mental_health: int | None = None
    diff_walking: YesNo = YesNo.No
    sex: SexEnum
    age_category: str
    race: str
    diabetic: str
    physical_activity: YesNo = YesNo.No
    gen_health: str
    sleep_time: int | None = None
    asthma: YesNo = YesNo.No
    kidney_disease: YesNo = YesNo.No
    skin_cancer: YesNo = YesNo.No

