
# HeartCrisisAPI - AI 心脏预警接口

## 项目简介

HeartCrisisAPI 是一个基于人工智能的心脏健康预警系统后端接口，旨在为用户提供心脏健康风险评估和相关健康管理服务。

## 功能特性

- **用户管理**：支持用户注册、登录等基本功能
- **健康数据管理**：用户可以提交和管理个人健康数据
- **AI 心脏预测**：利用人工智能技术进行心脏健康风险预测
- **AI 健康咨询**：提供智能健康咨询对话服务
- **历史记录**：记录用户的健康数据和预测历史
- **健康资讯**：提供相关健康新闻和资讯
- **数据测试**：提供测试数据获取接口

## 技术栈

- **Web 框架**：FastAPI
- **数据库**：MySQL
- **ORM**：SQLAlchemy (异步)
- **数据库驱动**：aiomysql
- **配置管理**：python-dotenv

## 项目结构

```
HeartCrisisAPI/
├── api/              # API 路由层
├── config/           # 配置文件
├── models/           # 数据模型
├── schemas/          # Pydantic 数据模式
├── service/          # 业务逻辑层
└── main.py           # 项目入口
```

## 如何启动

### 1. 环境要求
- Python 3.7+
- MySQL 5.7+ 或 8.0+

### 2. 安装项目依赖

在项目根目录下执行以下命令安装依赖：

```bash
pip install fastapi uvicorn sqlalchemy aiomysql python-dotenv openai pydantic
```

或创建 `requirements.txt` 文件，包含以下内容：
```
fastapi
uvicorn
sqlalchemy
aiomysql
python-dotenv
openai
pydantic
```

然后执行：
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

在项目根目录下创建 `.env` 文件，配置以下字段：

```env
# ===================== 数据库配置 =====================
DB_HOST=localhost        # 数据库主机地址
DB_PORT=3306             # 数据库端口
DB_USER=root             # 数据库用户名
DB_PASSWORD=your_password # 数据库密码
DB_NAME=health_db       # 数据库名称

# ===================== AI 模型配置 =====================
DOUBAO_API_KEY=your_doubao_api_key      # 豆包 API Key
DOUBAO_BASE_URL=https://ark.cn-beijing.volces.com/api/v3  # 豆包 API 地址
DOUBAO_MODEL=ep-20241202xxxxxx-xxxxx   # 豆包模型 ID
```

### 4. 创建数据库

在 MySQL 中创建数据库：

```sql
CREATE DATABASE health_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. 启动项目

在项目根目录下执行：

```bash
python main.py
```

或使用 uvicorn 启动：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. 访问接口

项目启动成功后，可以通过以下地址访问：

- **API 文档（Swagger UI）**：http://localhost:8000/docs
- **API 文档（ReDoc）**：http://localhost:8000/redoc
- **根路径**：http://localhost:8000/

通过 Swagger UI 可以直接在浏览器中测试所有 API 接口。

