from pydantic import BaseModel

# ------------------------------
# 登录：只用于 登录接口
# ------------------------------
class UserLogin(BaseModel):
    username: str
    password: str

# ------------------------------
# 注册：只用于 注册接口
# ------------------------------
class UserCreate(BaseModel):
    username: str
    password: str