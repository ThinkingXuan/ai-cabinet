# AI Cabinet API Server

基于Flask的RESTful API服务器，采用MVC架构实现的用户认证系统。

## 功能特点

- 基于MVC架构
- 支持SQLite和MySQL数据库
- 使用SQLAlchemy ORM
- JWT认证（使用全局唯一账户ID作为身份标识）
- 用户注册和登录功能
- 用户资料管理（性别、出生日期）
- 用户身材信息管理（头像、身高、体重、身材类型等）
- 全局唯一账户ID
- 参数验证
- 模块化设计
- 标准化JSON响应格式
- 衣物图片上传功能（支持多图片上传）
- 阿里云OSS对象存储集成

## 项目结构

```
.
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── user.py
│   │   ├── user_body_info.py
│   │   ├── clothes.py
│   │   ├── tag.py
│   │   ├── clothes_tag.py
│   │   ├── outfit.py
│   │   ├── recommendation.py
│   │   ├── weather_log.py
│   │   ├── clothes_ai_info.py
│   │   └── shared_wardrobe.py
│   ├── controllers/
│   │   ├── auth.py
│   │   ├── home.py
│   │   ├── clothes_controller.py
│   │   └── user_body_controller.py
│   ├── services/
│   │   ├── user_service.py
│   │   ├── user_body_service.py
│   │   └── clothes_service.py
│   ├── schemas/
│   │   ├── user.py
│   │   └── user_body.py
│   └── utils/
│       ├── __init__.py
│       ├── response.py
│       └── oss_helper.py
├── migrations/
│   └── ai-cabinet.sql
├── tests/
│   └── test_upload_clothes.py
├── config.py
├── main.py
├── env.example
└── requirements.txt
```

## 安装和运行

1. 克隆项目并安装依赖：

```bash
git clone <repository-url>
cd ai-cabinet
pip install -r requirements.txt
pip install alibabacloud-oss-v2  # 安装阿里云OSS SDK
```

2. 设置环境变量（可选）：

```bash
export FLASK_ENV=development  # 或 production
export DATABASE_URL=mysql+pymysql://user:password@localhost/db_name  # 使用MySQL时
export OSS_ACCESS_KEY_ID=your_access_key_id  # 阿里云AccessKey ID
export OSS_ACCESS_KEY_SECRET=your_access_key_secret  # 阿里云AccessKey Secret
export OSS_REGION=cn-hangzhou  # 阿里云OSS区域
export OSS_BUCKET_NAME=ai-cabinet  # 阿里云OSS Bucket名称
```

3. 运行应用：

```bash
python main.py
```

## 标准化响应格式

所有API接口返回标准化的JSON格式：

### 成功响应

```json
{
  "success": true,
  "result": {...}  // 返回的数据
}
```

### 错误响应

```json
{
  "success": false,
  "message": "错误信息"
}
```

## API文档

### 主页

- **URL**: `/ai-cabinet`
- **方法**: GET
- **成功响应** (200):
  ```json
  {
    "success": true,
    "result": {
      "name": "AI Cabinet API",
      "version": "1.0.0",
      "description": "基于Flask的RESTful API服务器",
      "documentation": "查看 README.md 获取API文档",
      "endpoints": {
        "register": "/ai-cabinet/api/auth/register",
        "login": "/ai-cabinet/api/auth/login",
        "clothes": {
          "list": "/ai-cabinet/api/clothes/",
          "detail": "/ai-cabinet/api/clothes/{clothes_id}",
          "upload": "/ai-cabinet/api/clothes/upload"
        },
        "user_body": {
          "info": "/ai-cabinet/api/user/body",
          "avatar": "/ai-cabinet/api/user/body/avatar",
          "avatar_upload": "/ai-cabinet/api/user/body/avatar/upload"
        }
      }
    }
  }
  ```

### 用户注册

- **URL**: `/ai-cabinet/api/auth/register`
- **方法**: POST
- **请求体**:
  ```json
  {
    "username": "用户名",
    "email": "邮箱",  // 可选字段
    "password": "密码",
    "gender": "male",  // 可选字段，可选值: male, female, other
    "birth_date": "1990-01-01"  // 可选字段，格式: YYYY-MM-DD
  }
  ```
- **成功响应** (200):
  ```json
  {
    "success": true,
    "result": {
      "id": 1,
      "account_id": "550e8400-e29b-41d4-a716-446655440000",  // 全局唯一的账户ID
      "username": "用户名",
      "email": "邮箱",  // 如果未提供则为null
      "gender": "male",  // 如果未提供则为null
      "birth_date": "1990-01-01",  // 如果未提供则为null
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  }
  ```
- **错误响应** (200):
  ```json
  {
    "success": false,
    "message": "用户名已存在"
  }
  ```

### 用户登录

- **URL**: `/ai-cabinet/api/auth/login`
- **方法**: POST
- **请求体**:
  ```json
  {
    "username": "用户名",
    "password": "密码"
  }
  ```
- **成功响应** (200):
  ```json
  {
    "success": true,
    "result": {
      "access_token": "JWT令牌（使用account_id作为身份标识）",
      "user": {
        "id": 1,
        "account_id": "550e8400-e29b-41d4-a716-446655440000",
        "username": "用户名",
        "email": "邮箱",  // 如果未提供则为null
        "gender": "male",  // 如果未提供则为null
        "birth_date": "1990-01-01",  // 如果未提供则为null
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
      }
    }
  }
  ```
- **错误响应** (200):
  ```json
  {
    "success": false,
    "message": "用户名或密码错误"
  }
  ```

### 更新用户资料

- **URL**: `/ai-cabinet/api/auth/profile`
- **方法**: POST
- **认证**: 需要JWT令牌（在请求头中添加 `Authorization: Bearer <token>`）
- **请求体**:
  ```json
  {
    "gender": "female",  // 可选字段，可选值: male, female, other
    "birth_date": "1992-05-15"  // 可选字段格式: YYYY-MM-DD
  }
  ```
- **成功响应** (200):
  ```json
  {
    "success": true,
    "result": {
      "id": 1,
      "account_id": "550e8400-e29b-41d4-a716-446655440000",
      "username": "用户名",
      "email": "邮箱",
      "gender": "female",
      "birth_date": "1992-05-15",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  }
  ```
- **错误响应** (200):
  ```json
  {
    "success": false,
    "message": "验证错误",
    "errors": {
      "gender": ["无效的性别值，可接受的值为: male, female, other"]
    }
  }
  ```

### 获取衣物列表

- **URL**: `/ai-cabinet/api/clothes/`
- **方法**: GET
- **认证**: 需要JWT令牌（在请求头中添加 `Authorization: Bearer <token>`）
- **查询参数**:
  - `category` - 可选，按分类筛选
  - `status` - 可选，按状态筛选
  - `season` - 可选，按季节筛选
- **成功响应** (200):
  ```json
  {
    "success": true,
    "result": {
      "total": 2,
      "items": [
        {
          "id": 1,
          "account_id": "user123",
          "name": "红色上衣",
          "category": "上衣",
          "color": "红色",
          "season": ["spring", "autumn"],
          "style": "休闲",
          "status": "available",
          "image_url": "https://ai-cabinet.oss-cn-hangzhou.aliyuncs.com/clothes/user123/20230601/abc123.jpg",
          "created_at": "2023-06-01T12:34:56"
        },
        {
          "id": 2,
          "account_id": "user123",
          "name": "蓝色裤子",
          "category": "裤子",
          "color": "蓝色",
          "season": ["spring", "summer", "autumn"],
          "style": "休闲",
          "status": "available",
          "image_url": "https://ai-cabinet.oss-cn-hangzhou.aliyuncs.com/clothes/user123/20230601/def456.jpg",
          "created_at": "2023-06-01T12:35:00"
        }
      ]
    }
  }
  ```

### 获取衣物详情

- **URL**: `/ai-cabinet/api/clothes/{clothes_id}`
- **方法**: GET
- **认证**: 需要JWT令牌（在请求头中添加 `Authorization: Bearer <token>`）
- **成功响应** (200):
  ```json
  {
    "success": true,
    "result": {
      "id": 1,
      "account_id": "user123",
      "name": "红色上衣",
      "category": "上衣",
      "color": "红色",
      "season": ["spring", "autumn"],
      "style": "休闲",
      "status": "available",
      "image_url": "https://ai-cabinet.oss-cn-hangzhou.aliyuncs.com/clothes/user123/20230601/abc123.jpg",
      "created_at": "2023-06-01T12:34:56"
    }
  }
  ```
- **错误响应** (200):
  ```json
  {
    "success": false,
    "message": "衣物不存在"
  }
  ```

### 更新衣物信息

- **URL**: `/ai-cabinet/api/clothes/{clothes_id}`
- **方法**: PUT
- **认证**: 需要JWT令牌（在请求头中添加 `Authorization: Bearer <token>`）
- **请求体**:
  ```json
  {
    "name": "新名称",  // 可选字段
    "category": "新分类",  // 可选字段
    "color": "新颜色",  // 可选字段
    "season": "spring,summer",  // 可选字段，用逗号分隔的季节列表
    "style": "新风格"  // 可选字段
  }
  ```
- **成功响应** (200):
  ```json
  {
    "success": true,
    "result": {
      "id": 1,
      "account_id": "user123",
      "name": "新名称",
      "category": "新分类",
      "color": "新颜色",
      "season": ["spring", "summer"],
      "style": "新风格",
      "status": "available",
      "image_url": "https://ai-cabinet.oss-cn-hangzhou.aliyuncs.com/clothes/user123/20230601/abc123.jpg",
      "created_at": "2023-06-01T12:34:56"
    }
  }
  ```
- **错误响应** (200):
  ```json
  {
    "success": false,
    "message": "更新衣物失败: 错误信息"
  }
  ```

### 重新AI识别衣物

- **URL**: `/ai-cabinet/api/clothes/{clothes_id}/reanalyze`
- **方法**: POST
- **认证**: 需要JWT令牌（在请求头中添加 `Authorization: Bearer <token>`）
- **请求体**: 无需请求体
- **成功响应** (200):
  ```json
  {
    "success": true,
    "result": {
      "message": "AI识别成功",
      "ai_result": {
        "category": "上衣",
        "color": "蓝色",
        "season": "spring,summer",
        "style": "休闲",
        "confidence": 95
      },
      "clothes_id": 1,
      "image_url": "https://ai-cabinet.oss-cn-hangzhou.aliyuncs.com/clothes/user123/20230601/abc123.jpg"
    }
  }
  ```
- **错误响应** (200):
  ```json
  {
    "success": false,
    "message": "AI识别失败: 错误信息"
  }
  ```

### 删除衣物

- **URL**: `/ai-cabinet/api/clothes/{clothes_id}`
- **方法**: DELETE
- **认证**: 需要JWT令牌（在请求头中添加 `Authorization: Bearer <token>`）
- **请求体**: 无需请求体
- **说明**: 此接口只从数据库中删除衣物记录，不会删除OSS中的图片文件
  ```json
  {
    "success": true,
    "result": {
      "message": "衣物删除成功",
      "clothes_id": 1
    }
  }
  ```
- **错误响应** (200):
  ```json
  {
    "success": false,
    "message": "删除衣物失败: 错误信息"
  }
  ```

### 获取用户身材信息

- **URL**: `/ai-cabinet/api/user/body`
- **方法**: GET
- **认证**: 需要JWT令牌（在请求头中添加 `Authorization: Bearer <token>`）
- **成功响应** (200):
  ```json
  {
    "success": true,
    "result": {
      "id": 1,
      "account_id": "550e8400-e29b-41d4-a716-446655440000",
      "avatar_url": "https://ai-cabinet.oss-cn-hangzhou.aliyuncs.com/avatars/user123/avatar.jpg",
      "height": 175.5,
      "weight": 65.0,
      "upper_body_length": 70.0,
      "lower_body_length": 100.0,
      "body_shape": "梨形",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  }
  ```
- **错误响应** (200):
  ```json
  {
    "success": false,
    "message": "未找到用户身材信息"
  }
  ```

### 创建或更新用户身材信息

- **URL**: `/ai-cabinet/api/user/body`
- **方法**: POST 或 PUT
- **认证**: 需要JWT令牌（在请求头中添加 `Authorization: Bearer <token>`）
- **请求体**:
  ```json
  {
    "avatar_url": "https://ai-cabinet.oss-cn-hangzhou.aliyuncs.com/avatars/user123/avatar.jpg",  // 可选字段
    "height": 175.5,  // 可选字段，单位cm
    "weight": 65.0,  // 可选字段，单位kg
    "upper_body_length": 70.0,  // 可选字段，单位cm
    "lower_body_length": 100.0,  // 可选字段，单位cm
    "body_shape": "梨形"  // 可选字段，可选值: 梨形、苹果型、长方形、沙漏型、倒三角形
  }
  ```
- **成功响应** (200):
  ```json
  {
    "success": true,
    "result": {
      "id": 1,
      "account_id": "550e8400-e29b-41d4-a716-446655440000",
      "avatar_url": "https://ai-cabinet.oss-cn-hangzhou.aliyuncs.com/avatars/user123/avatar.jpg",
      "height": 175.5,
      "weight": 65.0,
      "upper_body_length": 70.0,
      "lower_body_length": 100.0,
      "body_shape": "梨形",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  }
  ```
- **错误响应** (200):
  ```json
  {
    "success": false,
    "message": "验证错误",
    "errors": {
      "height": ["身高必须大于0且不超过300cm"]
    }
  }
  ```

### 上传用户头像文件

- **URL**: `/ai-cabinet/api/user/body/avatar/upload`
- **方法**: POST
- **认证**: 需要JWT令牌（在请求头中添加 `Authorization: Bearer <token>`）
- **请求参数**:
  - `avatar` - 头像文件（表单字段名）
- **成功响应** (200):
  ```json
  {
    "success": true,
    "result": {
      "id": 1,
      "account_id": "550e8400-e29b-41d4-a716-446655440000",
      "avatar_url": "https://ai-cabinet.oss-cn-hangzhou.aliyuncs.com/avatar/user123/20240601/abc123.jpg",
      "height": 175.5,
      "weight": 65.0,
      "upper_body_length": 70.0,
      "lower_body_length": 100.0,
      "body_shape": "梨形",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  }
  ```
- **错误响应** (200):
  ```json
  {
    "success": false,
    "message": "没有上传头像文件"
  }
  ```

### 删除用户身材信息

- **URL**: `/ai-cabinet/api/user/body`
- **方法**: DELETE
- **认证**: 需要JWT令牌（在请求头中添加 `Authorization: Bearer <token>`）
- **请求体**: 无需请求体
- **成功响应** (200):
  ```json
  {
    "success": true,
    "result": {
      "message": "用户身材信息已删除"
    }
  }
  ```
- **错误响应** (200):
  ```json
  {
    "success": false,
    "message": "未找到用户身材信息"
  }
  ```

### 创建穿搭

- **URL**: `/ai-cabinet/api/outfit`
- **方法**: POST
- **认证**: 需要JWT令牌（在请求头中添加 `Authorization: Bearer <token>`）
- **请求体**:
  ```json
  {
    "name": "休闲穿搭",
    "clothes_items": [1, 2, 3],  // 衣物ID列表
    "image_url": "https://ai-cabinet.oss-cn-hangzhou.aliyuncs.com/outfits/user123/outfit1.jpg",  // 可选
    "description": "适合周末逛街的休闲穿搭",  // 可选
    "style": "休闲",  // 可选
    "season": "春秋",  // 可选
    "occasion": "日常"  // 可选
  }
  ```
- **成功响应** (200):
  ```json
  {
    "success": true,
    "result": {
      "id": 1,
      "account_id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "休闲穿搭",
      "clothes_items": [1, 2, 3],
      "image_url": "https://ai-cabinet.oss-cn-hangzhou.aliyuncs.com/outfits/user123/outfit1.jpg",
      "description": "适合周末逛街的休闲穿搭",
      "style": "休闲",
      "season": "春秋",
      "occasion": "日常",
      "created_at": "2024-01-01T00:00:00"
    }
  }
  ```
- **错误响应** (200):
  ```json
  {
    "success": false,
    "message": "验证错误",
    "errors": {
      "clothes_items": ["穿搭必须包含至少一件衣物"]
    }
  }
  ```

### 获取穿搭列表

- **URL**: `/ai-cabinet/api/outfit`
- **方法**: GET
- **认证**: 需要JWT令牌（在请求头中添加 `Authorization: Bearer <token>`）
- **查询参数**:
  - `style` - 可选，按风格筛选
  - `season` - 可选，按季节筛选
  - `occasion` - 可选，按场合筛选
- **成功响应** (200):
  ```json
  {
    "success": true,
    "result": [
      {
        "id": 1,
        "account_id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "休闲穿搭",
        "clothes_items": [1, 2, 3],
        "image_url": "https://ai-cabinet.oss-cn-hangzhou.aliyuncs.com/outfits/user123/outfit1.jpg",
        "description": "适合周末逛街的休闲穿搭",
        "style": "休闲",
        "season": "春秋",
        "occasion": "日常",
        "created_at": "2024-01-01T00:00:00"
      },
      {
        "id": 2,
        "account_id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "正式场合穿搭",
        "clothes_items": [4, 5, 6],
        "image_url": "https://ai-cabinet.oss-cn-hangzhou.aliyuncs.com/outfits/user123/outfit2.jpg",
        "description": "适合工作场合的正式穿搭",
        "style": "正式",
        "season": "四季",
        "occasion": "工作",
        "created_at": "2024-01-02T00:00:00"
      }
    ]
  }
  ```

### 获取穿搭详情

- **URL**: `/ai-cabinet/api/outfit/{outfit_id}`
- **方法**: GET
- **认证**: 需要JWT令牌（在请求头中添加 `Authorization: Bearer <token>`）
- **成功响应** (200):
  ```json
  {
    "success": true,
    "result": {
      "id": 1,
      "account_id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "休闲穿搭",
      "clothes_items": [1, 2, 3],
      "image_url": "https://ai-cabinet.oss-cn-hangzhou.aliyuncs.com/outfits/user123/outfit1.jpg",
      "description": "适合周末逛街的休闲穿搭",
      "style": "休闲",
      "season": "春秋",
      "occasion": "日常",
      "created_at": "2024-01-01T00:00:00"
    }
  }
  ```
- **错误响应** (200):
  ```json
  {
    "success": false,
    "message": "穿搭不存在"
  }
  ```

### 删除穿搭

- **URL**: `/ai-cabinet/api/outfit/{outfit_id}`
- **方法**: DELETE
- **认证**: 需要JWT令牌（在请求头中添加 `Authorization: Bearer <token>`）
- **请求体**: 无需请求体
- **成功响应** (200):
  ```json
  {
    "success": true,
    "result": {
      "id": 1,
      "deleted": true
    }
  }
  ```
- **错误响应** (200):
  ```json
  {
    "success": false,
    "message": "穿搭不存在"
  }
  ```

### AI穿搭推荐

- **URL**: `/ai-cabinet/api/outfit/ai`
- **方法**: POST
- **认证**: 需要JWT令牌（在请求头中添加 `Authorization: Bearer <token>`）
- **请求体**:
  ```json
  {
    "occasion": "工作",          // 可选，场合
    "season": "夏季",            // 可选，季节
    "style_preference": "休闲",  // 可选，风格偏好
    "weather": "晴天",           // 可选，天气
    "temperature": 25,           // 可选，温度
    "exclude_clothes_ids": [1, 2, 3]  // 可选，排除的衣物ID
  }
  ```
- **成功响应** (200):
  ```json
  {
    "success": true,
    "result": {
      "outfit": {
        "id": 1,
        "account_id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "清爽夏日工作装扮",
        "description": "这套穿搭组合了浅色系的上衣和深色长裤，既符合工作环境的正式感，又能应对夏季炎热天气...",
        "style": "商务休闲",
        "season": "夏季",
        "occasion": "工作",
        "clothes_items": [11, 22, 33],
        "image_url": null,
        "created_at": "2023-06-01T08:30:00Z"
      },
      "clothes_detail": [
        {
          "id": 11,
          "account_id": "550e8400-e29b-41d4-a716-446655440000",
          "name": "白色棉麻衬衫",
          "category": "上衣",
          "color": "白色",
          "season": ["spring", "summer"],
          "style": "休闲",
          "status": "available",
          "image_url": "https://example.com/clothes/11.jpg",
          "created_at": "2023-05-20T10:15:00Z"
        },
        {
          "id": 22,
          "account_id": "550e8400-e29b-41d4-a716-446655440000",
          "name": "深蓝色西裤",
          "category": "裤子",
          "color": "深蓝色",
          "season": ["spring", "summer", "autumn", "winter"],
          "style": "正式",
          "status": "available",
          "image_url": "https://example.com/clothes/22.jpg",
          "created_at": "2023-05-18T09:30:00Z"
        },
        {
          "id": 33,
          "account_id": "550e8400-e29b-41d4-a716-446655440000",
          "name": "棕色皮鞋",
          "category": "鞋子",
          "color": "棕色",
          "season": ["spring", "autumn", "winter"],
          "style": "正式",
          "status": "available",
          "image_url": "https://example.com/clothes/33.jpg",
          "created_at": "2023-05-15T14:20:00Z"
        }
      ]
    }
  }
  ```
- **错误响应** (200):
  ```json
  {
    "success": false,
    "message": "没有可用的衣物进行搭配"
  }
  ```

### 上传衣物图片

- **URL**: `/ai-cabinet/api/clothes/upload`
- **方法**: POST
- **认证**: 需要JWT令牌（在请求头中添加 `Authorization: Bearer <token>`）
- **请求参数**:
  - `files[]` - 文件列表，可以包含多个文件
- **成功响应** (200):
  ```json
  {
    "success": true,
    "result": {
      "total": 2,
      "success_count": 2,
      "failed_count": 0,
      "items": [
        {
          "filename": "shirt.jpg",
          "success": true,
          "clothes_id": 1,
          "image_url": "https://ai-cabinet.oss-cn-hangzhou.aliyuncs.com/clothes/user123/20230601/abc123.jpg"
        },
        {
          "filename": "pants.jpg",
          "success": true,
          "clothes_id": 2,
          "image_url": "https://ai-cabinet.oss-cn-hangzhou.aliyuncs.com/clothes/user123/20230601/def456.jpg"
        }
      ]
    }
  }
  ```
- **错误响应** (200):
  ```json
  {
    "success": false,
    "message": "没有上传文件"
  }
  ```

## 安全说明

系统使用JWT（JSON Web Token）进行认证，具有以下特点：

1. 使用全局唯一的`account_id`（UUID格式）作为JWT身份标识，而不是数据库ID
2. 密码使用bcrypt算法加密存储，不保存明文密码
3. 所有敏感操作（如更新用户资料、上传图片）都需要JWT认证
4. JWT令牌有效期为1小时（可在配置文件中调整）

## 配置说明

项目使用统一的配置文件`config.py`，包含以下配置项：

### 基础配置

```python
# 基础配置
SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
```

### 数据库配置

项目支持两种数据库配置：

1. SQLite（开发环境默认）：
   - 无需额外配置
   - 数据存储在 `dev.db` 文件中

2. MySQL：
   - 需要设置环境变量 `DATABASE_URL`
   - 格式：`mysql+pymysql://user:password@localhost/db_name`

### 文件上传配置

```python
# 文件上传配置
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 最大上传文件大小（10MB）
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}  # 允许上传的图片格式
```

### 阿里云OSS配置

```python
# 阿里云OSS配置
OSS_ACCESS_KEY_ID = os.getenv('OSS_ACCESS_KEY_ID', 'your_access_key_id')
OSS_ACCESS_KEY_SECRET = os.getenv('OSS_ACCESS_KEY_SECRET', 'your_access_key_secret')
OSS_REGION = os.getenv('OSS_REGION', 'cn-hangzhou')
OSS_BUCKET_NAME = os.getenv('OSS_BUCKET_NAME', 'ai-cabinet')
OSS_ENDPOINT = os.getenv('OSS_ENDPOINT', f"https://oss-{OSS_REGION}.aliyuncs.com")

# OSS文件访问配置
OSS_URL_EXPIRATION = 3600  # 签名URL有效期（秒）
OSS_PUBLIC_URL_BASE = f"https://{OSS_BUCKET_NAME}.{OSS_ENDPOINT.replace('https://', '')}"
```