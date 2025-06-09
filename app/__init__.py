from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import config

# 初始化扩展
db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name='default'):
    """
    应用工厂函数
    :param config_name: 配置名称，默认为default
    :return: Flask应用实例
    """
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    jwt.init_app(app)
    
    # 添加根路由
    from .controllers.home import home_bp
    app.register_blueprint(home_bp, url_prefix='/ai-cabinet')
    
    # 注册蓝图
    from .controllers.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/ai-cabinet/api/auth')
    
    # 注册全局错误处理
    register_error_handlers(app)
    
    return app

def register_error_handlers(app):
    """
    注册全局错误处理
    :param app: Flask应用实例
    """
    from .utils.response import error_response
    
    @app.errorhandler(400)
    def bad_request(e):
        return error_response("请求参数错误", status_code=200)
    
    @app.errorhandler(401)
    def unauthorized(e):
        return error_response("未授权访问", status_code=200)
    
    @app.errorhandler(403)
    def forbidden(e):
        return error_response("禁止访问此资源", status_code=200)
    
    @app.errorhandler(404)
    def not_found(e):
        return error_response("资源不存在", status_code=200)
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return error_response("服务器内部错误", status_code=200)
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"未处理的异常: {str(e)}")
        return error_response("服务器处理请求时出错", status_code=200) 