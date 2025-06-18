from datetime import datetime
import bcrypt
import uuid
from app import db
from app.models.user_body_info import UserBodyInfo

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='系统主键')
    account_id = db.Column(db.String(64), unique=True, nullable=False, comment='全局唯一账号ID（逻辑主键）')
    username = db.Column(db.String(50), nullable=False, comment='用户名')
    email = db.Column(db.String(100), unique=True, nullable=True, comment='邮箱')
    password_hash = db.Column(db.String(255), nullable=False, comment='加密后的密码')
    gender = db.Column(db.Enum('male', 'female', 'other'), nullable=True, comment='性别')
    birthdate = db.Column(db.Date, nullable=True, comment='出生日期')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')

    def __init__(self, username, password, email=None, gender=None, birthdate=None):
        self.account_id = str(uuid.uuid4())  # 生成全局唯一的account_id
        self.username = username
        # 如果email是空字符串，则设置为None
        self.email = None if email == '' else email
        self.gender = gender
        self.birthdate = birthdate
        self.set_password(password)
    
    def set_password(self, password):
        """
        设置密码
        :param password: 明文密码
        """
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        """
        验证密码
        :param password: 明文密码
        :return: 布尔值，表示密码是否正确
        """
        return bcrypt.checkpw(password.encode('utf-8'), 
                            self.password_hash.encode('utf-8'))
    
    def update_profile(self, gender=None, birthdate=None):
        """
        更新用户资料
        :param gender: 性别
        :param birthdate: 出生日期
        """
        if gender is not None:
            self.gender = gender
        if birthdate is not None:
            self.birthdate = birthdate
        db.session.commit()
    
    def get_clothes(self):
        """
        获取用户的所有衣物
        :return: 衣物列表
        """
        from app.models.clothes import Clothes
        return Clothes.query.filter_by(account_id=self.account_id).all()
    
    def get_outfits(self):
        """
        获取用户的所有穿搭
        :return: 穿搭列表
        """
        from app.models.outfit import Outfit
        return Outfit.query.filter_by(account_id=self.account_id).all()
    
    def get_tags(self):
        """
        获取用户的所有标签
        :return: 标签列表
        """
        from app.models.tag import Tag
        return Tag.query.filter_by(account_id=self.account_id).all()
    
    @classmethod
    def get_by_username(cls, username):
        """
        通过用户名获取用户
        :param username: 用户名
        :return: 用户对象或None
        """
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def get_by_account_id(cls, account_id):
        """
        通过account_id获取用户
        :param account_id: 全局唯一账号ID
        :return: 用户对象或None
        """
        return cls.query.filter_by(account_id=account_id).first()
    
    @classmethod
    def get_by_email(cls, email):
        """
        通过邮箱获取用户
        :param email: 邮箱
        :return: 用户对象或None
        """
        if not email:
            return None
        return cls.query.filter_by(email=email).first()
    
    def get_body_info(self):
        """
        获取用户的身材信息
        :return: 用户身材信息对象或None
        """
        return UserBodyInfo.get_by_account_id(self.account_id)
            
    def to_dict(self):
        """
        将用户对象转换为字典
        :return: 用户信息字典
        """
        birthdate_str = None
        if self.birthdate:
            birthdate_str = self.birthdate.isoformat()
            
        return {
            'id': self.id,
            'account_id': self.account_id,
            'username': self.username,
            'email': self.email,
            'gender': self.gender,
            'birthdate': birthdate_str,
            'created_at': self.created_at.isoformat()
        } 