from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime

class UserRegisterSchema(Schema):
    """用户注册数据验证schema"""
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Str(required=False, allow_none=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    gender = fields.Str(required=False, allow_none=True)
    birth_date = fields.Date(required=False, allow_none=True)
    
    @validates('email')
    def validate_email(self, value):
        """验证邮箱格式，允许为空或null"""
        if value is None or value == '':
            return
        
        # 简单的邮箱格式验证
        if '@' not in value or '.' not in value:
            raise ValidationError('无效的邮箱格式')
    
    @validates('gender')
    def validate_gender(self, value):
        """验证性别字段"""
        if value is None or value == '':
            return
        
        valid_genders = ['male', 'female', 'other']
        if value.lower() not in valid_genders:
            raise ValidationError('无效的性别值，可接受的值为: male, female, other')

class UserProfileUpdateSchema(Schema):
    """用户资料更新schema"""
    gender = fields.Str(required=False, allow_none=True)
    birth_date = fields.Date(required=False, allow_none=True)
    
    @validates('gender')
    def validate_gender(self, value):
        """验证性别字段"""
        if value is None or value == '':
            return
        
        valid_genders = ['male', 'female', 'other']
        if value.lower() not in valid_genders:
            raise ValidationError('无效的性别值，可接受的值为: male, female, other')
    
    @validates('birth_date')
    def validate_birth_date(self, value):
        """验证出生日期"""
        if value is None:
            return
        
        # 检查出生日期是否在未来
        if value > datetime.now().date():
            raise ValidationError('出生日期不能在未来')
        
        # 检查出生日期是否太早（例如超过120年）
        min_year = datetime.now().year - 120
        if value.year < min_year:
            raise ValidationError('出生日期无效')

class UserLoginSchema(Schema):
    """用户登录数据验证schema"""
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class UserSchema(Schema):
    """用户信息序列化schema"""
    id = fields.Int(dump_only=True)
    account_id = fields.Str(dump_only=True)
    username = fields.Str()
    email = fields.Str(allow_none=True)
    gender = fields.Str(allow_none=True)
    birthdate = fields.Date(allow_none=True)
    created_at = fields.DateTime(dump_only=True) 