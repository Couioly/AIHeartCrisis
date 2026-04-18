
# HeartCrisis - AI 心脏预警系统

## 项目简介

HeartCrisis 是一个基于人工智能的心脏健康预警系统，包含前端和后端两部分，旨在为用户提供心脏健康风险评估和相关健康管理服务。

## 功能特性

### 前端功能
- **用户认证**：登录、注册功能
- **主页**：系统介绍、健康资讯展示
- **问卷调查**：健康数据录入，提交后自动进行AI分析
- **体检报告**：上传PDF/图片体检报告，AI自动提取数据，支持用户修改后保存
- **结果详情**：基于用户数据的心脏健康风险预测，包含雷达图、仪表盘等可视化
- **历史记录**：查看健康数据历史和AI分析结果
- **AI交互**：智能健康咨询对话服务

### 后端功能
- **用户管理**：支持用户注册、登录等基本功能
- **健康数据管理**：用户可以提交和管理个人健康数据
- **AI 心脏预测**：利用人工智能技术进行心脏健康风险预测
- **多疾病预测**：基于体检报告数据的多种疾病风险预测
- **体检报告处理**：支持PDF/图片上传，AI自动提取数据，支持修改和保存
- **AI 健康咨询**：提供智能健康咨询对话服务
- **历史记录**：记录用户的健康数据和预测历史
- **健康资讯**：提供相关健康新闻和资讯
- **数据测试**：提供测试数据获取接口

## 技术栈

### 前端
- **HTML5**：页面结构
- **CSS3**：样式设计
- **JavaScript**：交互逻辑
- **Font Awesome**：图标库
- **Google Fonts**：字体

### 后端
- **Web 框架**：FastAPI
- **数据库**：MySQL
- **ORM**：SQLAlchemy (异步)
- **数据库驱动**：aiomysql
- **配置管理**：python-dotenv

## 项目结构

```
HeartCrisis/
├── backend/           # 后端代码
│   ├── api/           # API 路由层
│   ├── config/        # 配置文件
│   ├── models/        # 数据模型
│   ├── schemas/       # Pydantic 数据模式
│   ├── service/       # 业务逻辑层
│   ├── main.py        # 项目入口
│   └── requirements.txt
├── frontend/          # 前端代码
│   ├── css/           # CSS 样式文件
│   │   ├── variables.css  # 主题变量
│   │   ├── components.css # 通用组件
│   │   ├── nav.css        # 导航栏样式
│   │   ├── pages.css      # 页面样式
│   │   └── chat.css       # 聊天样式
│   ├── js/            # JavaScript 文件
│   │   └── main.js        # 主脚本
│   ├── index.html     # 主应用页面
│   ├── login.html     # 登录页面
│   └── logo.png       # 品牌 logo
└── README.md
```

## 如何启动

### 1. 环境要求
- Python 3.7+
- MySQL 5.7+ 或 8.0+
- 现代浏览器（Chrome、Firefox、Edge等）

### 2. 安装项目依赖

进入 backend 目录，然后执行以下命令安装依赖：

```bash
cd backend
pip install -r requirements.txt
```

### 3. 配置环境变量

在 `backend` 目录下创建 `.env` 文件，配置以下字段：

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
DOUBAO_MODEL=doubao-xxxxxx-xxxxx   # 豆包模型 ID

# ===================== LongCat API 配置 =====================
LONGCAT_API_KEY=your_longcat_api_key      # LongCat API Key（体检报告提取用）
LONGCAT_BASE_URL=https://api.longcat.chat/openai  # LongCat API 地址
```

### 4. 创建数据库

在 MySQL 中创建数据库：

```sql
CREATE DATABASE health_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. 启动后端服务

确保在 `backend` 目录下执行：

```bash
cd backend
python main.py
```

或使用 uvicorn 启动：

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. 访问前端页面

后端服务启动成功后，可以通过以下地址访问前端页面：

- **登录页面**：http://localhost:8000/frontend/login.html
- **主应用页面**：http://localhost:8000/frontend/index.html

### 7. 访问后端接口

- **API 文档（Swagger UI）**：http://localhost:8000/docs
- **API 文档（ReDoc）**：http://localhost:8000/redoc
- **根路径**：http://localhost:8000/

通过 Swagger UI 可以直接在浏览器中测试所有 API 接口。

## API 接口文档

### 用户层接口

| 方法 | 接口                   | 说明 |
|------|----------------------|------|
| POST | `/api/register` | 用户注册 |
| POST | `/api/login`    | 用户登录 |
| POST | `/api/ai/ai-chat`    | AI 健康咨询对话 |

### 问卷调查接口

| 方法 | 接口 | 说明 |
|------|------|------|
| GET | `/api/questionnaires/user` | 获取用户的问卷列表 |
| GET | `/api/questionnaires/id` | 获取问卷详情 |
| POST | `/api/user/questionnaires/submit` | 提交问卷（自动进行AI分析） |
| GET | `/api/user/history` | 查询指定健康记录的分析结果 |
| POST | `/api/ai-predict` | AI 心脏病风险预测 |

### 体检报告接口

| 方法 | 接口 | 说明 |
|------|------|------|
| POST | `/api/medical-report/upload` | 上传体检报告并提取数据（支持PDF、JPG、PNG） |
| POST | `/api/medical-report/save` | 保存体检报告数据（自动进行多疾病预测） |

### 系统层接口

| 方法 | 接口 | 说明 |
|------|------|------|
| GET | `/api/news` | 获取健康新闻资讯 |
| GET | `/api/proxy/image` | 图片代理接口（解决CORS问题） |

### 测试数据获取接口

| 方法 | 接口 | 说明 |
|------|------|------|
| GET | `/api/db/get-test-data` | 根据ID获取测试数据（范围1~319795） |

## 使用说明

### 1. 注册和登录
- 访问登录页面（http://localhost:8000/frontend/login.html）
- 点击"注册"链接，填写注册信息
- 注册成功后，使用用户名和密码登录

### 2. 主要功能使用
- **首页**：查看系统介绍和健康资讯
- **问卷调查**：填写健康相关数据，提交后系统会自动调用豆包AI进行分析，包含雷达图、健康仪表盘等可视化展示
- **体检报告**：
  - 上传PDF/图片格式的体检报告文件
  - 系统自动提取数据并返回JSON格式
  - 用户可以在前端修改提取的数据
  - 确认无误后提交保存，系统自动进行多疾病预测（只在查询结果时显示）
- **历史记录**：查看历史健康数据和评估结果
- **AI交互**：与AI助手聊天，获取健康咨询

### 3. 主题切换
- 点击右上角的主题切换按钮，可以在深色模式和浅色模式之间切换

## 注意事项

1. **数据库配置**：确保MySQL数据库已正确配置，并且.env文件中的数据库连接信息正确
2. **AI模型配置**：
   - 需要配置有效的豆包API密钥才能使用AI相关功能
   - 需要配置有效的LongCat API密钥才能使用体检报告提取功能
3. **模型文件**：确保 `multi_disease_model.pkl` 文件需要放置在 `backend/config/` 目录下
4. **文件上传**：体检报告上传功能支持PDF、JPG、PNG格式
5. **浏览器兼容性**：建议使用Chrome、Firefox、Edge等现代浏览器
6. **网络连接**：系统需要网络连接才能获取健康资讯和使用AI功能
7. **数据安全**：
   - 原始体检报告文件在提取数据后会自动删除，不保留在服务器上
   - 所有API密钥等敏感信息通过环境变量配置，请勿硬编码在代码中

## 项目维护

- **前端代码**：位于 `frontend` 目录，包含HTML、CSS和JavaScript文件
- **后端代码**：位于 `backend` 目录，包含Python代码和配置文件
- **API文档**：可通过Swagger UI查看和测试所有API接口

## 许可证

本项目仅供学习和研究使用。

