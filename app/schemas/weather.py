from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import date

class WeatherSchema(Schema):
    """天气记录创建和更新的schema"""
    date = fields.Date(required=True)
    location = fields.Str(allow_none=True, validate=validate.Length(max=100))
    temperature = fields.Float(allow_none=True)
    weather_condition = fields.Str(allow_none=True, validate=validate.Length(max=50))
    humidity = fields.Float(allow_none=True)
    wind_speed = fields.Float(allow_none=True)
    
    @validates('date')
    def validate_date(self, value):
        """验证日期"""
        if value > date.today():
            raise ValidationError('日期不能是未来日期')

class WeatherResponseSchema(Schema):
    """天气记录响应的schema"""
    id = fields.Int(dump_only=True)
    account_id = fields.Str(dump_only=True)
    date = fields.Date()
    location = fields.Str(allow_none=True)
    temperature = fields.Float(allow_none=True)
    weather_condition = fields.Str(allow_none=True)
    humidity = fields.Float(allow_none=True)
    wind_speed = fields.Float(allow_none=True)
    created_at = fields.DateTime(dump_only=True)

class WeatherFilterSchema(Schema):
    """天气记录过滤的schema"""
    start_date = fields.Date(allow_none=True)
    end_date = fields.Date(allow_none=True)
    location = fields.Str(allow_none=True)
    
    @validates('end_date')
    def validate_end_date(self, value, **kwargs):
        """验证结束日期"""
        start_date = kwargs.get('data', {}).get('start_date')
        if start_date and value and value < start_date:
            raise ValidationError('结束日期不能早于开始日期') 