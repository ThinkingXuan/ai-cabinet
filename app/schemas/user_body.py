from marshmallow import Schema, fields, validate, validates, ValidationError

class UserBodyInfoSchema(Schema):
    """用户身材信息验证schema"""
    avatar_url = fields.Str(required=False, allow_none=True)
    height = fields.Float(required=False, allow_none=True)
    weight = fields.Float(required=False, allow_none=True)
    upper_body_length = fields.Float(required=False, allow_none=True)
    lower_body_length = fields.Float(required=False, allow_none=True)
    body_shape = fields.Str(required=False, allow_none=True)
    
    @validates('height')
    def validate_height(self, value):
        """验证身高"""
        if value is not None:
            if value <= 0 or value > 300:  # 假设人类身高不超过300cm
                raise ValidationError('身高必须大于0且不超过300cm')
    
    @validates('weight')
    def validate_weight(self, value):
        """验证体重"""
        if value is not None:
            if value <= 0 or value > 500:  # 假设人类体重不超过500kg
                raise ValidationError('体重必须大于0且不超过500kg')
    
    @validates('upper_body_length')
    def validate_upper_body_length(self, value):
        """验证上身长度"""
        if value is not None:
            if value <= 0 or value > 150:  # 假设上身长度不超过150cm
                raise ValidationError('上身长度必须大于0且不超过150cm')
    
    @validates('lower_body_length')
    def validate_lower_body_length(self, value):
        """验证下身长度"""
        if value is not None:
            if value <= 0 or value > 150:  # 假设下身长度不超过150cm
                raise ValidationError('下身长度必须大于0且不超过150cm')
    
    @validates('body_shape')
    def validate_body_shape(self, value):
        """验证身材类型"""
        if value is not None:
            valid_shapes = ['梨形', '苹果型', '长方形', '沙漏型', '倒三角形', 'H型']
            if value not in valid_shapes:
                raise ValidationError(f'无效的身材类型，有效值为: {", ".join(valid_shapes)}')

class UserBodyInfoResponseSchema(Schema):
    """用户身材信息响应schema"""
    id = fields.Int(dump_only=True)
    account_id = fields.Str(dump_only=True)
    avatar_url = fields.Str(allow_none=True)
    height = fields.Float(allow_none=True)
    weight = fields.Float(allow_none=True)
    upper_body_length = fields.Float(allow_none=True)
    lower_body_length = fields.Float(allow_none=True)
    body_shape = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True) 