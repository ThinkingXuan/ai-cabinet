import os
from datetime import timedelta

class Config:
    """基础配置类"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

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