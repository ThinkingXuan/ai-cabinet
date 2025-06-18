from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app.services.weather_service import WeatherService
from app.schemas.weather import WeatherSchema, WeatherResponseSchema, WeatherFilterSchema
from app.utils.response import success_response, error_response

# 创建蓝图
weather_bp = Blueprint('weather', __name__)

# 实例化Schema
weather_schema = WeatherSchema()
weather_response_schema = WeatherResponseSchema()
weather_filter_schema = WeatherFilterSchema()

@weather_bp.route('', methods=['POST'])
@jwt_required()
def create_weather():
    """
    创建/更新天气记录接口
    :return: JSON响应
    """
    # 获取当前用户的account_id
    account_id = get_jwt_identity()
    
    # 验证请求数据
    try:
        data = weather_schema.load(request.get_json())
    except ValidationError as err:
        return error_response("验证错误", err.messages, 200)
    
    # 创建天气记录
    weather = WeatherService.create_weather(
        account_id=account_id,
        date=data['date'],
        location=data.get('location'),
        temperature=data.get('temperature'),
        weather_condition=data.get('weather_condition'),
        humidity=data.get('humidity'),
        wind_speed=data.get('wind_speed')
    )
    
    # 序列化响应数据
    result = weather_response_schema.dump(weather)
    
    return success_response(result)

@weather_bp.route('', methods=['GET'])
@jwt_required()
def get_weather_list():
    """
    获取天气记录列表接口
    :return: JSON响应
    """
    # 获取当前用户的account_id
    account_id = get_jwt_identity()
    
    # 验证过滤参数
    filters = {}
    for key in ['start_date', 'end_date', 'location']:
        if key in request.args:
            filters[key] = request.args.get(key)
    
    try:
        filters = weather_filter_schema.load(filters)
    except ValidationError as err:
        return error_response("过滤参数错误", err.messages, 200)
    
    # 获取天气记录列表
    if 'start_date' in filters and 'end_date' in filters:
        weathers = WeatherService.get_weather_by_date_range(
            account_id=account_id,
            start_date=filters['start_date'],
            end_date=filters['end_date']
        )
    elif 'location' in filters:
        weathers = WeatherService.get_weather_by_location(
            account_id=account_id,
            location=filters['location']
        )
    else:
        # 如果没有过滤条件，返回错误
        return error_response("请提供过滤条件", status_code=200)
    
    # 序列化响应数据
    result = [weather_response_schema.dump(weather) for weather in weathers]
    
    return success_response(result)

@weather_bp.route('/<string:date>', methods=['GET'])
@jwt_required()
def get_weather(date):
    """
    获取指定日期的天气记录接口
    :param date: 日期，格式为YYYY-MM-DD
    :return: JSON响应
    """
    # 获取当前用户的account_id
    account_id = get_jwt_identity()
    
    # 解析日期
    try:
        from datetime import datetime
        parsed_date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return error_response("日期格式错误，应为YYYY-MM-DD", status_code=200)
    
    # 获取天气记录
    weather = WeatherService.get_weather_by_date(account_id, parsed_date)
    
    if not weather:
        return error_response("天气记录不存在", status_code=200)
    
    # 序列化响应数据
    result = weather_response_schema.dump(weather)
    
    return success_response(result)

@weather_bp.route('/<int:weather_id>', methods=['PUT'])
@jwt_required()
def update_weather(weather_id):
    """
    更新天气记录接口
    :param weather_id: 天气记录ID
    :return: JSON响应
    """
    # 获取当前用户的account_id
    account_id = get_jwt_identity()
    
    # 验证请求数据
    try:
        data = weather_schema.load(request.get_json())
    except ValidationError as err:
        return error_response("验证错误", err.messages, 200)
    
    # 更新天气记录
    weather = WeatherService.update_weather(
        account_id=account_id,
        weather_id=weather_id,
        date=data.get('date'),
        location=data.get('location'),
        temperature=data.get('temperature'),
        weather_condition=data.get('weather_condition'),
        humidity=data.get('humidity'),
        wind_speed=data.get('wind_speed')
    )
    
    if not weather:
        return error_response("天气记录不存在", status_code=200)
    
    # 序列化响应数据
    result = weather_response_schema.dump(weather)
    
    return success_response(result)

@weather_bp.route('/<int:weather_id>', methods=['DELETE'])
@jwt_required()
def delete_weather(weather_id):
    """
    删除天气记录接口
    :param weather_id: 天气记录ID
    :return: JSON响应
    """
    # 获取当前用户的account_id
    account_id = get_jwt_identity()
    
    # 删除天气记录
    success = WeatherService.delete_weather(account_id, weather_id)
    
    if not success:
        return error_response("天气记录不存在", status_code=200)
    
    return success_response({"id": weather_id, "deleted": True}) 