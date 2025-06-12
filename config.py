import os
from datetime import timedelta

class Config:
    """基础配置类"""
    SECRET_KEY = os.getenv('SECRET_KEY', '')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 最大上传文件大小（10MB）
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp', 'tiff', 'ico', 'heic', 'heif'}  # 允许上传的图片格式
    
    # 阿里云OSS配置
    OSS_ACCESS_KEY_ID = os.getenv('OSS_ACCESS_KEY_ID', '')
    OSS_ACCESS_KEY_SECRET = os.getenv('OSS_ACCESS_KEY_SECRET', '')
    OSS_REGION = os.getenv('OSS_REGION', 'cn-beijing')
    OSS_BUCKET_NAME = os.getenv('OSS_BUCKET_NAME', 'ai-cabinet2')
    OSS_ENDPOINT = os.getenv('OSS_ENDPOINT', f"https://oss-{OSS_REGION}.aliyuncs.com")
    
    # OSS文件访问配置
    OSS_URL_EXPIRATION = 360000  # 签名URL有效期（秒）
    OSS_PUBLIC_URL_BASE = f"https://{OSS_BUCKET_NAME}.{OSS_ENDPOINT.replace('https://', '')}"  # 公开访问的URL基础
    
    # OpenAI配置
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', '')
    OPENAI_MAX_RETRIES = 3  # 最大重试次数
    
    # AI识别提示词配置
    AI_VISION_SYSTEM_PROMPT = os.getenv('AI_VISION_SYSTEM_PROMPT', 
        "你是一个专业的服装分析AI,擅长识别服装类型、颜色、适合季节和风格。")
    
    ai_version_user_promot = """请分析这张服装图片, 并以JSON格式返回以下信息:
    1. category: 服装类别（上衣、裤子、裙子、外套、鞋子、配饰、首饰、其他），完全遵守，没有就标记其他类别，
    2. color: 主要颜色
    3. season: 适合的季节(spring, summer, autumn, winter中的一个或多个, 用逗号分隔)
    4. style: 风格（如休闲、正式、运动、复古等）
    5. confidence: 识别置信度(0-100的数字)
        
    请只返回JSON格式的结果,不要包含其他解释文字。"""
    AI_VISION_USER_PROMPT = os.getenv('AI_VISION_USER_PROMPT', ai_version_user_promot)
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