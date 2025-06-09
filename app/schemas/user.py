from marshmallow import Schema, fields, validate

class UserRegisterSchema(Schema):
    """用户注册数据验证schema"""
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))

class UserLoginSchema(Schema):
    """用户登录数据验证schema"""
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class UserSchema(Schema):
    """用户信息序列化schema"""
    id = fields.Int(dump_only=True)
    username = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True) 