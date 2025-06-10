from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError
from datetime import datetime

from app.services.user_service import UserService
from app.schemas.user import UserRegisterSchema, UserLoginSchema, UserSchema, UserProfileUpdateSchema
from app.utils.response import success_response, error_response

auth_bp = Blueprint('auth', __name__)
user_schema = UserSchema()
register_schema = UserRegisterSchema()
login_schema = UserLoginSchema()
profile_update_schema = UserProfileUpdateSchema()

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

    # 处理邮箱字段
    email = data.get('email')
    if email == '':  # 如果是空字符串，转换为None
        email = None
    
    # 检查邮箱是否已存在（如果提供了邮箱）
    if email and UserService.get_user_by_email(email):
        return error_response("邮箱已被注册", status_code=200)

    # 处理出生日期字段
    birth_date = data.get('birth_date')
    
    # 创建新用户
    user = UserService.create_user(
        username=data['username'],
        password=data['password'],
        email=email,
        gender=data.get('gender'),
        birthdate=birth_date
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

    # 创建访问令牌，使用account_id作为身份标识
    access_token = create_access_token(identity=user.account_id)

    return success_response({
        "access_token": access_token,
        "user": user_schema.dump(user)
    }, 200)

@auth_bp.route('/profile', methods=['POST'])
@jwt_required()
def update_profile():
    """
    更新用户资料接口
    :return: JSON响应
    """
    try:
        data = profile_update_schema.load(request.get_json())
    except ValidationError as err:
        return error_response("验证错误", err.messages, 200)
    
    # 获取当前用户的account_id
    current_account_id = get_jwt_identity()
    
    # 通过account_id获取用户
    user = UserService.get_user_by_account_id(current_account_id)
    
    if not user:
        return error_response("用户不存在", status_code=200)
    
    # 更新用户资料
    user = UserService.update_user_profile(
        user=user,
        gender=data.get('gender'),
        birthdate=data.get('birth_date')
    )
    
    return success_response(user_schema.dump(user), 200) 