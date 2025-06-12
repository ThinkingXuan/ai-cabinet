from flask import Blueprint
from app.utils.response import success_response

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def ai_cabinet():
    """
    AI Cabinet 主页
    :return: JSON响应
    """
    return success_response({
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
                "upload": "/ai-cabinet/api/clothes/upload",
                "update": "/ai-cabinet/api/clothes/{clothes_id}",
                "reanalyze": "/ai-cabinet/api/clothes/{clothes_id}/reanalyze"
            }
        }
    }) 