
# HeartCrisis - AI 心脏预警系统

## 项目简介

HeartCrisis 是一个基于人工智能的心脏健康预警系统，包含前端和后端两部分，旨在为用户提供心脏健康风险评估和相关健康管理服务。

## 功能特性

### 前端功能
- **用户认证**：登录、注册功能
- **主页**：系统介绍、健康资讯展示
- **问卷调查**：健康数据录入
- **AI风险评估**：基于用户数据的心脏健康风险预测
- **体检报告**：上传和管理体检报告
- **历史记录**：查看健康数据历史
- **AI交互**：智能健康咨询对话服务

### 后端功能
- **用户管理**：支持用户注册、登录等基本功能
- **健康数据管理**：用户可以提交和管理个人健康数据
- **AI 心脏预测**：利用人工智能技术进行心脏健康风险预测
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

## 使用说明

### 1. 注册和登录
- 访问登录页面（http://localhost:8000/frontend/login.html）
- 点击"注册"链接，填写注册信息
- 注册成功后，使用用户名和密码登录

### 2. 主要功能使用
- **首页**：查看系统介绍和健康资讯
- **问卷调查**：填写健康相关数据，提交后系统会保存
- **AI风险评估**：输入健康数据，点击"开始预测"获取风险评估结果
- **体检报告**：上传体检报告文件，查看历史报告
- **历史记录**：查看历史健康数据和评估结果
- **AI交互**：与AI助手聊天，获取健康咨询

### 3. 主题切换
- 点击右上角的主题切换按钮，可以在深色模式和浅色模式之间切换

## 注意事项

1. **数据库配置**：确保MySQL数据库已正确配置，并且.env文件中的数据库连接信息正确
2. **AI模型配置**：需要配置有效的豆包API密钥才能使用AI相关功能
3. **文件上传**：体检报告上传功能支持PDF、JPG、PNG格式
4. **浏览器兼容性**：建议使用Chrome、Firefox、Edge等现代浏览器
5. **网络连接**：系统需要网络连接才能获取健康资讯和使用AI功能

## 项目维护

- **前端代码**：位于 `frontend` 目录，包含HTML、CSS和JavaScript文件
- **后端代码**：位于 `backend` 目录，包含Python代码和配置文件
- **API文档**：可通过Swagger UI查看和测试所有API接口

## 许可证

本项目仅供学习和研究使用。

