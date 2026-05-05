# HeartCrisis API接口文档

## 概述

本文档基于项目代码整理，严格按照代码实现描述所有API接口。

- **项目名称**: HeartCrisis - AI心脏预警系统
- **框架**: FastAPI
- **数据库**: SQLAlchemy异步
- **文档地址**: http://localhost:8000/docs
- **ReDoc地址**: http://localhost:8000/redoc

---

## 通用响应格式

所有接口的响应格式通常如下：

```json
{
  "code": 200,
  "message": "操作成功",
  "data": {}
}
```

---

## 1. 用户层接口

### 1.1 用户登录

**接口地址**: `POST /api/login`

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |

**请求示例**:

```json
{
  "username": "testuser",
  "password": "123456"
}
```

**响应示例**:

**成功 (200)**:
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "username": "testuser"
  }
}
```

**用户不存在 (404)**:
```json
{
  "code": 404,
  "message": "用户不存在"
}
```

**密码错误 (401)**:
```json
{
  "code": 401,
  "message": "密码错误"
}
```

---

### 1.2 用户注册

**接口地址**: `POST /api/register`

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| username | string | 是 | 用户名（3-50位，支持中文、英文、数字、下划线，不能包含空格） |
| password | string | 是 | 密码（6-20位，不能包含空格） |

**请求示例**:

```json
{
  "username": "newuser",
  "password": "password123"
}
```

**响应示例**:

**成功 (200)**:
```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "username": "newuser"
  }
}
```

**用户名已存在 (400)**:
```json
{
  "code": 400,
  "message": "用户名已存在"
}
```

---

### 1.3 AI健康咨询对话

**接口地址**: `POST /api/ai/ai-chat`

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| messages | array | 是 | 对话消息列表 |
| user_id | string | 否 | 用户标识 |

**消息格式**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| role | string | 是 | 角色（user/assistant） |
| content | string | 是 | 消息内容 |

**请求示例**:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "我最近总是感到胸闷，这是怎么回事？"
    }
  ],
  "user_id": "user123"
}
```

**响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "response": "您好，胸闷是一个需要重视的症状...",
    "model": "doubao-pro",
    "user_id": "user123"
  }
}
```

---

## 2. 问卷调查接口

### 2.1 提交问卷

**接口地址**: `POST /api/user/questionnaires/submit`

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| username | string | 是 | 用户名 |
| submission_time | datetime | 是 | 提交时间 |
| basic_info | object | 是 | 基本信息 |
| answers | array | 是 | 问卷回答列表 |
| health_data | object | 否 | 健康数据 |
| wearable_data | object | 否 | 手环数据 |

**基本信息 (basic_info)**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| age | string | 是 | 年龄范围 |
| gender | string | 是 | 性别 |
| occupation | string | 是 | 职业类别 |
| education | string | 是 | 最高学历 |

**问卷回答 (answers)**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| question_id | int | 是 | 问题编号 |
| answer | any | 是 | 答案 |

**健康数据 (health_data)**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| blood_pressure | string | 否 | 血压 |
| blood_lipids | string | 否 | 血脂 |
| blood_sugar | float | 否 | 血糖 |
| bmi | float | 否 | BMI指数 |
| ecg | string | 否 | 心电图结果 |

**手环数据 (wearable_data)**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| heart_rate | int | 否 | 心率 |
| blood_oxygen | int | 否 | 血氧 |

**请求示例**:

```json
{
  "username": "testuser",
  "submission_time": "2024-01-01T12:00:00",
  "basic_info": {
    "age": "25-35",
    "gender": "男",
    "occupation": "程序员",
    "education": "本科"
  },
  "answers": [
    {
      "question_id": 1,
      "answer": "是"
    },
    {
      "question_id": 2,
      "answer": "否"
    }
  ],
  "health_data": {
    "blood_pressure": "120/80",
    "blood_sugar": 5.6,
    "bmi": 22.5
  },
  "wearable_data": {
    "heart_rate": 75,
    "blood_oxygen": 98
  }
}
```

**响应示例**:

```json
{
  "success": true,
  "message": "问卷提交成功",
  "data": {
    "questionnaire_id": 1,
    "submission_time": "2024-01-01T12:00:00",
    "risk_level": "低风险"
  },
  "errors": null
}
```

---

### 2.2 获取用户的问卷列表

**接口地址**: `GET /api/questionnaires/user`

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| username | string | 是 | 用户名 |

**请求示例**:

```
GET /api/questionnaires/user?username=testuser
```

**响应示例**:

```json
{
  "success": true,
  "message": "获取问卷列表成功",
  "data": [
    {
      "id": 1,
      "username": "testuser",
      "submission_time": "2024-01-01T12:00:00",
      "risk_level": "低风险"
    }
  ]
}
```

---

### 2.3 获取问卷详情

**接口地址**: `GET /api/questionnaires/id`

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| questionnaire_id | int | 是 | 问卷ID |

**请求示例**:

```
GET /api/questionnaires/id?questionnaire_id=1
```

**响应示例**:

```json
{
  "success": true,
  "message": "获取问卷详情成功",
  "data": {
    "id": 1,
    "username": "testuser",
    "submission_time": "2024-01-01T12:00:00",
    "created_at": "2024-01-01T12:00:00",
    "risk_level": "低风险",
    "basic_info": {
      "age": "25-35",
      "gender": "男",
      "occupation": "程序员",
      "education": "本科"
    },
    "answers": [
      {
        "question_id": 1,
        "answer": "是",
        "is_core": false
      }
    ],
    "health_data": {
      "blood_pressure": "120/80",
      "blood_lipids": null,
      "blood_sugar": 5.6,
      "bmi": 22.5,
      "ecg": null
    },
    "wearable_data": {
      "heart_rate": 75,
      "blood_oxygen": 98
    }
  }
}
```

---

### 2.4 AI心脏病风险预测

**接口地址**: `POST /api/ai-predict`

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| username | string | 是 | 用户名 |
| questionnaire_id | int | 否 | 关联的问卷ID |
| age | string | 否 | 年龄范围 |
| gender | string | 否 | 性别 |
| occupation | string | 否 | 职业类别 |
| education | string | 否 | 最高学历 |
| answers | array | 否 | 问卷回答列表 |
| blood_pressure | string | 否 | 血压 |
| blood_lipids | string | 否 | 血脂 |
| blood_sugar | float | 否 | 血糖 |
| bmi | float | 否 | BMI指数 |
| ecg | string | 否 | 心电图结果 |
| heart_rate | int | 否 | 心率 |
| blood_oxygen | int | 否 | 血氧 |
| medical_report_ai_result | object | 否 | 体检报告的AI预测结果 |

**请求示例**:

```json
{
  "username": "testuser",
  "questionnaire_id": 1,
  "age": "25-35",
  "gender": "男",
  "answers": [
    {
      "question_id": 1,
      "answer": "是"
    }
  ]
}
```

**响应示例**:

```json
{
  "code": 200,
  "message": "预测完成",
  "data": {
    "username": "testuser",
    "prediction": {
      "AI大模型PKL预测发病概率": [
        {
          "disease": "冠心病",
          "probability": 0.15
        }
      ],
      "AI大模型分析": {
        "综合风险分数": 25,
        "风险等级": "低风险",
        "高概率疾病": ["冠心病"],
        "病情依据": "根据您的生活习惯...",
        "建议": "建议您保持健康饮食..."
      },
      "雷达图数据": {
        "labels": [],
        "values": []
      },
      "柱状图数据": [],
      "健康仪表盘数据": {},
      "数据来源": ["问卷数据"]
    }
  }
}
```

---

### 2.5 查询指定健康记录的分析结果

**接口地址**: `GET /api/user/history`

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| questionnaire_id | int | 是 | 问卷ID |

**请求示例**:

```
GET /api/user/history?questionnaire_id=1
```

**响应示例**:

**成功 (200)**:
```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "disease_probabilities": [
      {
        "disease": "冠心病",
        "probability": 0.15
      }
    ],
    "AI大模型分析": {
      "风险等级": "低风险",
      "高概率疾病": ["冠心病"],
      "病情依据": "根据您的生活习惯...",
      "建议": "建议您保持健康饮食..."
    },
    "full_prediction_result": {
      "AI大模型PKL预测发病概率": [],
      "AI大模型分析": {},
      "雷达图数据": {},
      "柱状图数据": [],
      "健康仪表盘数据": {},
      "数据来源": []
    }
  }
}
```

**未找到 (404)**:
```json
{
  "code": 404,
  "message": "未找到该记录的分析结果",
  "data": null
}
```

---

## 3. 体检报告接口

### 3.1 上传体检报告并提取数据

**接口地址**: `POST /api/medical-report/upload`

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| file | file | 是 | 体检报告文件（支持PDF、JPG、PNG） |

**请求说明**: 使用form-data格式上传文件

**响应示例**:

```json
{
  "code": 200,
  "message": "提取成功",
  "data": {
    "age": 35,
    "sex": "男",
    "height": 175,
    "weight": 70,
    "BMI": 22.9,
    "heartRate": 72
  }
}
```

---

### 3.2 保存体检报告数据

**接口地址**: `POST /api/medical-report/save`

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| username | string | 是 | 用户名 |
| medical_data | object | 是 | 体检报告数据字典 |

**请求示例**:

```json
{
  "username": "testuser",
  "medical_data": {
    "age": 35,
    "sex": "男",
    "height": 175,
    "weight": 70,
    "BMI": 22.9
  }
}
```

**响应示例**:

```json
{
  "code": 200,
  "message": "保存成功",
  "data": {
    "id": 1,
    "ai_report_result": {
      "diseases": []
    }
  }
}
```

---

## 4. 系统层接口

### 4.1 获取健康新闻资讯

**接口地址**: `GET /api/news`

**请求参数**: 无

**请求示例**:

```
GET /api/news
```

**响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "url": "https://www.medlive.cn/...",
      "title": "最新心脏病研究进展",
      "content": "近日，国际著名医学期刊发表了...",
      "image_url": "https://www.medlive.cn/...",
      "publish_time": "2024-01-01"
    }
  ]
}
```

---

### 4.2 图片代理接口

**接口地址**: `GET /api/proxy/image`

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| url | string | 是 | 原始图片URL |

**请求示例**:

```
GET /api/proxy/image?url=https://example.com/image.jpg
```

**响应**: 返回图片二进制数据

---

## 5. 测试数据获取接口

### 5.1 根据ID获取测试数据

**接口地址**: `GET /api/db/get-test-data`

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | int | 是 | 数据ID（范围1~319795） |

**请求示例**:

```
GET /api/db/get-test-data?id=1
```

**响应示例**:

```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "id": 1,
    "heart_disease": "No",
    "bmi": 22.5,
    "smoking": "No",
    "alcohol_drinking": "No",
    "stroke": "No",
    "physical_health": 0,
    "mental_health": 0,
    "diff_walking": "No",
    "sex": "Male",
    "age_category": "25-35",
    "race": "White",
    "diabetic": "No",
    "physical_activity": "Yes",
    "gen_health": "Excellent",
    "sleep_time": 7,
    "asthma": "No",
    "kidney_disease": "No",
    "skin_cancer": "No"
  }
}
```

---

## 附录：枚举类型说明

### YesNo 枚举

| 值 | 说明 |
|----|------|
| Yes | 是 |
| No | 否 |

### SexEnum 枚举

| 值 | 说明 |
|----|------|
| Male | 男性 |
| Female | 女性 |

---

## 附录：接口路由总览

| 前缀 | 接口模块 |
|------|----------|
| /api | 登录、注册、AI预测、新闻、图片代理、问卷、体检报告 |
| /api/user | 提交问卷、历史记录 |
| /api/ai | AI健康咨询 |
| /api/db | 测试数据获取 |
