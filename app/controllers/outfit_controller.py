from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app.services.outfit_service import OutfitService
from app.services.outfit_ai_service import OutfitAIService
from app.schemas.outfit import OutfitSchema, OutfitResponseSchema, OutfitFilterSchema, OutfitAIRequestSchema
from app.utils.response import success_response, error_response

# 创建蓝图
outfit_bp = Blueprint('outfit', __name__)

# 实例化Schema
outfit_schema = OutfitSchema()
outfit_response_schema = OutfitResponseSchema()
outfit_filter_schema = OutfitFilterSchema()
outfit_ai_schema = OutfitAIRequestSchema()

@outfit_bp.route('', methods=['POST'])
@jwt_required()
def create_outfit():
    """
    创建穿搭接口
    :return: JSON响应
    """
    # 获取当前用户的account_id
    account_id = get_jwt_identity()
    
    # 验证请求数据
    try:
        data = outfit_schema.load(request.get_json())
    except ValidationError as err:
        return error_response("验证错误", err.messages, 200)
    
    # 创建穿搭
    outfit = OutfitService.create_outfit(
        account_id=account_id,
        name=data['name'],
        clothes_items=data['clothes_items'],
        image_url=data.get('image_url'),
        description=data.get('description'),
        style=data.get('style'),
        season=data.get('season'),
        occasion=data.get('occasion')
    )
    
    # 序列化响应数据
    result = outfit_response_schema.dump(outfit)
    
    return success_response(result)

@outfit_bp.route('/ai', methods=['POST'])
@jwt_required()
def generate_ai_outfit():
    """
    AI穿搭推荐接口
    
    如果请求中未提供季节、天气或温度参数，将自动从天气数据库中获取：
    - 季节：根据当前日期自动计算（3-5月为春季，6-8月为夏季，9-11月为秋季，12-2月为冬季）
    - 天气：从当天的天气记录中获取
    - 温度：从当天的天气记录中获取
    
    :return: JSON响应
    """
    # 获取当前用户的account_id
    account_id = get_jwt_identity()
    
    # 验证请求数据
    try:
        data = outfit_ai_schema.load(request.get_json() or {})
    except ValidationError as err:
        return error_response("验证错误", err.messages, 200)
    
    # 实例化AI服务
    ai_service = OutfitAIService()
    
    # 生成穿搭推荐
    # 注意：如果未提供季节、天气或温度参数，服务将自动从天气数据库获取
    result = ai_service.generate_outfit(
        account_id=account_id,
        occasion=data.get('occasion'),
        season=data.get('season'),
        style_preference=data.get('style_preference'),
        weather=data.get('weather'),
        temperature=data.get('temperature'),
        exclude_clothes_ids=data.get('exclude_clothes_ids')
    )
    
    if not result.get('success', False):
        return error_response(result.get('message', 'AI穿搭推荐失败'), status_code=200)
    
    # 序列化响应数据
    outfit = result.get('outfit')
    outfit_data = outfit_response_schema.dump(outfit)
    
    # 获取衣物详情
    clothes_detail = [cloth.to_dict() for cloth in outfit.get_clothes()]
    
    response_data = {
        'outfit': outfit_data,
        'clothes_detail': clothes_detail
    }
    
    return success_response(response_data)

@outfit_bp.route('', methods=['GET'])
@jwt_required()
def get_outfit_list():
    """
    获取穿搭列表接口
    :return: JSON响应
    """
    # 获取当前用户的account_id
    account_id = get_jwt_identity()
    
    # 验证过滤参数
    filters = {}
    for key in ['style', 'season', 'occasion']:
        if key in request.args:
            filters[key] = request.args.get(key)
    
    try:
        filters = outfit_filter_schema.load(filters)
    except ValidationError as err:
        return error_response("过滤参数错误", err.messages, 200)
    
    # 获取穿搭列表
    outfits = OutfitService.get_outfit_list(
        account_id=account_id,
        style=filters.get('style'),
        season=filters.get('season'),
        occasion=filters.get('occasion')
    )
    
    # 序列化响应数据
    result = [outfit_response_schema.dump(outfit) for outfit in outfits]
    
    return success_response(result)

@outfit_bp.route('/<int:outfit_id>', methods=['GET'])
@jwt_required()
def get_outfit(outfit_id):
    """
    获取穿搭详情接口
    :param outfit_id: 穿搭ID
    :return: JSON响应
    """
    # 获取当前用户的account_id
    account_id = get_jwt_identity()
    
    # 获取穿搭
    outfit = OutfitService.get_outfit_by_id(account_id, outfit_id)
    
    if not outfit:
        return error_response("穿搭不存在", status_code=200)
    
    # 序列化响应数据
    result = outfit_response_schema.dump(outfit)
    
    return success_response(result)

@outfit_bp.route('/<int:outfit_id>', methods=['DELETE'])
@jwt_required()
def delete_outfit(outfit_id):
    """
    删除穿搭接口
    :param outfit_id: 穿搭ID
    :return: JSON响应
    """
    # 获取当前用户的account_id
    account_id = get_jwt_identity()
    
    # 删除穿搭
    success = OutfitService.delete_outfit(account_id, outfit_id)
    
    if not success:
        return error_response("穿搭不存在", status_code=200)
    
    return success_response({"id": outfit_id, "deleted": True}) 