from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError

from app.services.user_service import UserService
from app.schemas.user import UserRegisterSchema, UserLoginSchema, UserSchema
from app.utils.response import success_response, error_response

auth_bp = Blueprint('auth', __name__)
user_schema = UserSchema()
register_schema = UserRegisterSchema()
login_schema = UserLoginSchema()

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    用户注册接口
    :return: JSON响应
    """
    try:
        data = register_schema.load(request.get_json())
    except ValidationError as err:
        return error_response("验证错误", err.messages, 200)

    # 检查用户名是否已存在
    if UserService.get_user_by_username(data['username']):
        return error_response("用户名已存在", status_code=200)

    # 检查邮箱是否已存在
    if UserService.get_user_by_email(data['email']):
        return error_response("邮箱已被注册", status_code=200)

    # 创建新用户
    user = UserService.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )

    return success_response(user_schema.dump(user), 200)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    用户登录接口
    :return: JSON响应
    """
    try:
        data = login_schema.load(request.get_json())
    except ValidationError as err:
        return error_response("验证错误", err.messages, 200)

    user = UserService.authenticate_user(
        username=data['username'],
        password=data['password']
    )

    if not user:
        return error_response("用户名或密码错误", status_code=200)

    # 创建访问令牌
    access_token = create_access_token(identity=user.id)

    return success_response({
        "access_token": access_token,
        "user": user_schema.dump(user)
    }, 200) 