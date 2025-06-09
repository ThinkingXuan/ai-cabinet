# AI Cabinet API Server

基于Flask的RESTful API服务器，采用MVC架构实现的用户认证系统。

## 功能特点

- 基于MVC架构
- 支持SQLite和MySQL数据库
- 使用SQLAlchemy ORM
- JWT认证
- 用户注册和登录功能
- 参数验证
- 模块化设计
- 标准化JSON响应格式

## 项目结构

```
.
├── app/
│   ├── __init__.py
│   ├── models/
│   │   └── user.py
│   ├── controllers/
│   │   ├── auth.py
│   │   └── home.py
│   ├── services/
│   │   └── user_service.py
│   ├── schemas/
│   │   └── user.py
│   └── utils/
│       ├── __init__.py
│       └── response.py
├── migrations/
│   └── create_users_table.sql
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
```

2. 设置环境变量（可选）：

```bash
export FLASK_ENV=development  # 或 production
export DATABASE_URL=mysql+pymysql://user:password@localhost/db_name  # 使用MySQL时
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
        "login": "/ai-cabinet/api/auth/login"
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
    "email": "邮箱",
    "password": "密码"
  }
  ```
- **成功响应** (200):
  ```json
  {
    "success": true,
    "result": {
      "id": 1,
      "username": "用户名",
      "email": "邮箱",
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
      "access_token": "JWT令牌",
      "user": {
        "id": 1,
        "username": "用户名",
        "email": "邮箱",
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

## 配置说明

项目支持两种数据库配置：

1. SQLite（开发环境默认）：
   - 无需额外配置
   - 数据存储在 `dev.db` 文件中

2. MySQL：
   - 需要设置环境变量 `DATABASE_URL`
   - 格式：`mysql+pymysql://user:password@localhost/db_name`

## 部署说明

项目提供了两个部署脚本：

1. `deploy_aws_minimal.sh` - 使用systemd管理服务的最小化部署方案
2. `deploy_no_systemd.sh` - 不使用systemd的极简部署方案（资源占用更少）

## 开发说明

1. 项目使用 Flask-SQLAlchemy 作为 ORM 工具
2. 使用 Flask-JWT-Extended 处理用户认证
3. 使用 Marshmallow 进行数据验证和序列化
4. 所有配置项都在 `config.py` 中集中管理
5. 使用统一的响应格式工具函数 `success_response` 和 `error_response`