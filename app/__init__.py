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
    
    # 注册JWT错误处理器
    register_jwt_handlers(jwt)
    
    # 添加根路由
    from .controllers.home import home_bp
    app.register_blueprint(home_bp, url_prefix='/ai-cabinet')
    
    # 注册蓝图
    from .controllers.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/ai-cabinet/api/auth')
    
    # 注册衣物蓝图
    from .controllers.clothes_controller import clothes_bp
    app.register_blueprint(clothes_bp, url_prefix='/ai-cabinet/api/clothes')
    
    # 注册用户身材信息蓝图
    from .controllers.user_body_controller import user_body_bp
    app.register_blueprint(user_body_bp, url_prefix='/ai-cabinet/api/user/body')
    
    # 注册全局错误处理
    register_error_handlers(app)
    
    return app

def register_jwt_handlers(jwt):
    """
    注册JWT错误处理器
    :param jwt: JWT管理器实例
    """
    from .utils.response import error_response
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """处理令牌过期的情况"""
        return error_response("令牌已过期，请重新登录", status_code=200)
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        """处理无效令牌的情况"""
        return error_response("无效的令牌", status_code=200)
    
    @jwt.unauthorized_loader
    def missing_token_callback(error_string):
        """处理缺少令牌的情况"""
        return error_response("缺少令牌", status_code=200)
    
    # 令牌黑名单检查回调
    # 注意：此回调必须返回布尔值，而不是响应对象
    # 返回True表示令牌在黑名单中（被禁用），返回False表示令牌不在黑名单中（可用）
    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_header, jwt_payload):
        """
        检查令牌是否在黑名单中
        目前我们没有实现令牌黑名单功能，所以始终返回False
        如果需要实现令牌黑名单，可以在此处添加检查逻辑
        """
        return False  # 返回False表示令牌不在黑名单中
    
    @jwt.needs_fresh_token_loader
    def needs_fresh_token_callback(jwt_header, jwt_payload):
        """处理需要新令牌的情况"""
        return error_response("需要新的令牌", status_code=200)
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        """处理令牌被撤销的情况"""
        return error_response("令牌已被撤销", status_code=200)

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