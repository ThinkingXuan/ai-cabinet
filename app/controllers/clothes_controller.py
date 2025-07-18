"""
衣物控制器
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app.services.clothes_service import ClothesService
from config import Config
from app.utils.response import success_response, error_response

# 从配置中导入上传文件大小限制
MAX_CONTENT_LENGTH = Config.MAX_CONTENT_LENGTH

# 创建蓝图
clothes_bp = Blueprint('clothes', __name__, url_prefix='/api/clothes')

# 创建服务实例
clothes_service = ClothesService()

@clothes_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_clothes_images():
    """
    上传衣物图片
    """
    # 获取当前用户的account_id
    account_id = get_jwt_identity()
    
    # 检查是否有文件上传
    if 'files[]' not in request.files:
        return error_response('没有上传文件', status_code=200)
    
    # 获取上传的文件列表
    files = request.files.getlist('files[]')
    
    # 检查文件大小总和
    total_size = sum(len(file.read()) for file in files)
    
    # 重置文件指针
    for file in files:
        file.seek(0)
    
    # 检查文件大小是否超过限制
    if total_size > MAX_CONTENT_LENGTH:
        return error_response(f'上传文件总大小不能超过{MAX_CONTENT_LENGTH / 1024 / 1024}MB', status_code=400)
    
    # 上传文件
    result = clothes_service.upload_clothes_images(account_id, files)
    
    if result['success']:
        return success_response(result['items'], 200)
    else:
        return error_response(result['message'], status_code=200)

@clothes_bp.route('/', methods=['GET'])
@jwt_required()
def get_clothes_list():
    """
    获取衣物列表
    """
    # 获取当前用户的account_id
    account_id = get_jwt_identity()
    
    # 获取查询参数
    category = request.args.get('category')
    status = request.args.get('status')
    season = request.args.get('season')
    
    # 查询衣物列表
    clothes_list = clothes_service.get_clothes_list(account_id, category, status, season)
    
    # 转换为字典列表
    items = [clothes.to_dict() for clothes in clothes_list]
    
    return success_response({
        'total': len(items),
        'items': items
    }, 200)

@clothes_bp.route('/<int:clothes_id>', methods=['GET'])
@jwt_required()
def get_clothes_by_id(clothes_id):
    """
    通过ID获取衣物
    """
    # 获取当前用户的account_id
    account_id = get_jwt_identity()
    
    # 查询衣物
    clothes = clothes_service.get_clothes_by_id(account_id, clothes_id)
    
    if clothes:
        return success_response(clothes.to_dict(), 200)
    else:
        return error_response('衣物不存在', status_code=200)

@clothes_bp.route('/<int:clothes_id>', methods=['PUT'])
@jwt_required()
def update_clothes(clothes_id):
    """
    更新衣物信息
    """
    # 获取当前用户的account_id
    account_id = get_jwt_identity()
    
    # 获取请求数据
    data = request.get_json()
    
    if not data:
        return error_response('请求数据不能为空', status_code=200)
    
    # 提取更新字段
    name = data.get('name')
    category = data.get('category')
    color = data.get('color')
    season = data.get('season')
    style = data.get('style')
    
    # 更新衣物
    result = clothes_service.update_clothes(
        account_id=account_id,
        clothes_id=clothes_id,
        name=name,
        category=category,
        color=color,
        season=season,
        style=style
    )
    
    if result['success']:
        return success_response(result['data'], 200)
    else:
        return error_response(result['message'], status_code=200)

@clothes_bp.route('/<int:clothes_id>/reanalyze', methods=['POST'])
@jwt_required()
def reanalyze_clothes(clothes_id):
    """
    重新AI识别衣物
    """
    # 获取当前用户的account_id
    account_id = get_jwt_identity()
    
    # 调用服务重新识别衣物
    result = clothes_service.reanalyze_clothes(account_id, clothes_id)
    
    if result['success']:
        return success_response(result['result'], 200)
    else:
        return error_response(result['message'], status_code=200)

@clothes_bp.route('/<int:clothes_id>', methods=['DELETE'])
@jwt_required()
def delete_clothes(clothes_id):
    """
    删除衣物
    """
    # 获取当前用户的account_id
    account_id = get_jwt_identity()
    
    # 调用服务删除衣物
    result = clothes_service.delete_clothes(account_id, clothes_id)
    
    if result['success']:
        return success_response(result['result'], 200)
    else:
        return error_response(result['message'], status_code=200) 