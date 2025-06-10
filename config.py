import os
from datetime import timedelta

class Config:
    """基础配置类"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 最大上传文件大小（10MB）
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}  # 允许上传的图片格式
    
    # 阿里云OSS配置
    OSS_ACCESS_KEY_ID = os.getenv('OSS_ACCESS_KEY_ID', '')
    OSS_ACCESS_KEY_SECRET = os.getenv('OSS_ACCESS_KEY_SECRET', '')
    OSS_REGION = os.getenv('OSS_REGION', 'cn-beijing')
    OSS_BUCKET_NAME = os.getenv('OSS_BUCKET_NAME', 'ai-cabinet2')
    OSS_ENDPOINT = os.getenv('OSS_ENDPOINT', f"https://oss-{OSS_REGION}.aliyuncs.com")
    
    # OSS文件访问配置
    OSS_URL_EXPIRATION = 3600  # 签名URL有效期（秒）
    OSS_PUBLIC_URL_BASE = f"https://{OSS_BUCKET_NAME}.{OSS_ENDPOINT.replace('https://', '')}"  # 公开访问的URL基础

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    # SQLite配置
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    
class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    # MySQL配置
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
        'mysql+pymysql://user:password@localhost/db_name')

# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 