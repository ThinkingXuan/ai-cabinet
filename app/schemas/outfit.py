from marshmallow import Schema, fields, validate, validates, ValidationError

class OutfitSchema(Schema):
    """穿搭创建和更新的schema"""
    name = fields.Str(required=True, validate=validate.Length(max=100))
    clothes_items = fields.List(fields.Int(), required=True)
    image_url = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    style = fields.Str(allow_none=True, validate=validate.Length(max=50))
    season = fields.Str(allow_none=True, validate=validate.Length(max=50))
    occasion = fields.Str(allow_none=True, validate=validate.Length(max=50))
    
    @validates('clothes_items')
    def validate_clothes_items(self, clothes_items):
        """验证衣物ID列表"""
        if not clothes_items or len(clothes_items) == 0:
            raise ValidationError('穿搭必须包含至少一件衣物')
        
class OutfitResponseSchema(Schema):
    """穿搭响应的schema"""
    id = fields.Int(dump_only=True)
    account_id = fields.Str(dump_only=True)
    name = fields.Str()
    clothes_items = fields.Method('get_clothes_items')
    image_url = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    style = fields.Str(allow_none=True)
    season = fields.Str(allow_none=True)
    occasion = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    
    def get_clothes_items(self, obj):
        """获取衣物ID列表"""
        return obj.get_clothes_items()

class OutfitFilterSchema(Schema):
    """穿搭过滤的schema"""
    style = fields.Str(allow_none=True)
    season = fields.Str(allow_none=True)
    occasion = fields.Str(allow_none=True)

class OutfitAIRequestSchema(Schema):
    """AI穿搭请求的schema"""
    occasion = fields.Str(allow_none=True, validate=validate.Length(max=50))
    season = fields.Str(allow_none=True, validate=validate.Length(max=50))
    style_preference = fields.Str(allow_none=True, validate=validate.Length(max=50))
    weather = fields.Str(allow_none=True, validate=validate.Length(max=50))
    temperature = fields.Float(allow_none=True)
    exclude_clothes_ids = fields.List(fields.Int(), allow_none=True) 