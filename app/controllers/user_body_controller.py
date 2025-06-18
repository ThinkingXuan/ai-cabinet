from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from werkzeug.utils import secure_filename

from app.services.user_body_service import UserBodyService
from app.services.user_service import UserService
from app.schemas.user_body import UserBodyInfoSchema, UserBodyInfoResponseSchema
from app.utils.response import success_response, error_response
from config import Config

# 从配置中导入上传文件大小限制
MAX_CONTENT_LENGTH = Config.MAX_CONTENT_LENGTH

# 创建蓝图
user_body_bp = Blueprint('user_body', __name__)

# 实例化Schema
user_body_schema = UserBodyInfoSchema()
user_body_response_schema = UserBodyInfoResponseSchema()

@user_body_bp.route('', methods=['GET'])
@jwt_required()
def get_user_body_info():
    """
    获取当前用户的身材信息
    :return: JSON响应
    """
    # 获取当前用户的account_id
    account_id = get_jwt_identity()
    
    # 获取用户身材信息
    body_info = UserBodyService.get_user_body_info(account_id)
    
    if not body_info:
        return error_response("未找到用户身材信息", status_code=200)
    
    # 序列化响应数据
    result = user_body_response_schema.dump(body_info)
    
    return success_response(result)

@user_body_bp.route('', methods=['POST', 'PUT'])
@jwt_required()
def create_or_update_body_info():
    """
    创建或更新用户身材信息
    :return: JSON响应
    """
    # 获取当前用户的account_id
    account_id = get_jwt_identity()
    
    # 验证请求数据
    try:
        data = user_body_schema.load(request.get_json())
    except ValidationError as err:
        return error_response("验证错误", err.messages, 200)
    
    # 创建或更新用户身材信息
    body_info = UserBodyService.create_or_update_body_info(
        account_id=account_id,
        avatar_url=data.get('avatar_url'),
        height=data.get('height'),
        weight=data.get('weight'),
        upper_body_length=data.get('upper_body_length'),
        lower_body_length=data.get('lower_body_length'),
        body_shape=data.get('body_shape')
    )
    
    # 序列化响应数据
    result = user_body_response_schema.dump(body_info)
    
    return success_response(result)

@user_body_bp.route('/avatar', methods=['PUT'])
@jwt_required()
def update_avatar():
    """
    更新用户头像URL
    :return: JSON响应
    """
    # 获取当前用户的account_id
    account_id = get_jwt_identity()
    
    # 获取请求数据
    data = request.get_json()
    
    if not data or 'avatar_url' not in data:
        return error_response("缺少头像URL", status_code=200)
    
    # 更新用户头像
    body_info = UserBodyService.update_avatar(
        account_id=account_id,
        avatar_url=data['avatar_url']
    )
    
    # 序列化响应数据
    result = user_body_response_schema.dump(body_info)
    
    return success_response(result)

@user_body_bp.route('/avatar/upload', methods=['POST'])
@jwt_required()
def upload_avatar():
    """
    上传用户头像文件
    :return: JSON响应
    """
    # 获取当前用户的account_id
    account_id = get_jwt_identity()
    
    # 检查是否有文件上传
    if 'avatar' not in request.files:
        return error_response("没有上传头像文件", status_code=200)
    
    # 获取上传的文件
    avatar_file = request.files['avatar']
    
    # 检查文件名是否为空
    if avatar_file.filename == '':
        return error_response("未选择文件", status_code=200)
    
    # 检查文件大小
    avatar_file.seek(0, 2)  # 移动到文件末尾
    file_size = avatar_file.tell()  # 获取文件大小
    avatar_file.seek(0)  # 重置文件指针
    
    if file_size > MAX_CONTENT_LENGTH:
        return error_response(f"文件大小不能超过{MAX_CONTENT_LENGTH / 1024 / 1024}MB", status_code=200)
    
    # 上传头像
    body_info = UserBodyService.upload_avatar(account_id, avatar_file)
    
    if not body_info:
        return error_response("头像上传失败", status_code=200)
    
    # 序列化响应数据
    result = user_body_response_schema.dump(body_info)
    
    return success_response(result)

@user_body_bp.route('', methods=['DELETE'])
@jwt_required()
def delete_body_info():
    """
    删除用户身材信息
    :return: JSON响应
    """
    # 获取当前用户的account_id
    account_id = get_jwt_identity()
    
    # 删除用户身材信息
    success = UserBodyService.delete_body_info(account_id)
    
    if not success:
        return error_response("未找到用户身材信息", status_code=200)
    
    return success_response({"message": "用户身材信息已删除"}) 