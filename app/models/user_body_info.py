from datetime import datetime
from app import db

class UserBodyInfo(db.Model):
    """用户身材信息模型"""
    __tablename__ = 'user_body_info'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='身材信息ID')
    account_id = db.Column(db.String(64), unique=True, nullable=False, comment='关联的账号ID')
    avatar_url = db.Column(db.String(255), nullable=True, comment='用户头像URL')
    height = db.Column(db.Float(precision=2), nullable=True, comment='身高(cm)')
    weight = db.Column(db.Float(precision=2), nullable=True, comment='体重(kg)')
    upper_body_length = db.Column(db.Float(precision=2), nullable=True, comment='上身长度(cm)')
    lower_body_length = db.Column(db.Float(precision=2), nullable=True, comment='下身长度(cm)')
    body_shape = db.Column(db.String(50), nullable=True, comment='身材类型，如梨形、苹果型等')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    def __init__(self, account_id, avatar_url=None, height=None, weight=None, 
                 upper_body_length=None, lower_body_length=None, body_shape=None):
        """
        初始化用户身材信息
        :param account_id: 关联的账号ID
        :param avatar_url: 用户头像URL
        :param height: 身高(cm)
        :param weight: 体重(kg)
        :param upper_body_length: 上身长度(cm)
        :param lower_body_length: 下身长度(cm)
        :param body_shape: 身材类型
        """
        self.account_id = account_id
        self.avatar_url = avatar_url
        self.height = height
        self.weight = weight
        self.upper_body_length = upper_body_length
        self.lower_body_length = lower_body_length
        self.body_shape = body_shape
    
    def update(self, avatar_url=None, height=None, weight=None, 
               upper_body_length=None, lower_body_length=None, body_shape=None):
        """
        更新用户身材信息
        :param avatar_url: 用户头像URL
        :param height: 身高(cm)
        :param weight: 体重(kg)
        :param upper_body_length: 上身长度(cm)
        :param lower_body_length: 下身长度(cm)
        :param body_shape: 身材类型
        """
        if avatar_url is not None:
            self.avatar_url = avatar_url
        if height is not None:
            self.height = height
        if weight is not None:
            self.weight = weight
        if upper_body_length is not None:
            self.upper_body_length = upper_body_length
        if lower_body_length is not None:
            self.lower_body_length = lower_body_length
        if body_shape is not None:
            self.body_shape = body_shape
        
        db.session.commit()
    
    @classmethod
    def get_by_account_id(cls, account_id):
        """
        通过account_id获取用户身材信息
        :param account_id: 账号ID
        :return: 用户身材信息对象或None
        """
        return cls.query.filter_by(account_id=account_id).first()
    
    @classmethod
    def create_or_update(cls, account_id, **kwargs):
        """
        创建或更新用户身材信息
        :param account_id: 账号ID
        :param kwargs: 其他参数
        :return: 用户身材信息对象
        """
        body_info = cls.get_by_account_id(account_id)
        
        if body_info:
            body_info.update(**kwargs)
        else:
            body_info = cls(account_id=account_id, **kwargs)
            db.session.add(body_info)
            db.session.commit()
        
        return body_info
    
    def to_dict(self):
        """
        将用户身材信息对象转换为字典
        :return: 用户身材信息字典
        """
        return {
            'id': self.id,
            'account_id': self.account_id,
            'avatar_url': self.avatar_url,
            'height': self.height,
            'weight': self.weight,
            'upper_body_length': self.upper_body_length,
            'lower_body_length': self.lower_body_length,
            'body_shape': self.body_shape,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 