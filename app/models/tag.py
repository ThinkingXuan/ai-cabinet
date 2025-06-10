from datetime import datetime
from app import db
from sqlalchemy import UniqueConstraint

class Tag(db.Model):
    """标签模型"""
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='标签ID')
    account_id = db.Column(db.String(64), nullable=False, index=True, comment='所属账号ID')
    name = db.Column(db.String(50), nullable=False, comment='标签名称')
    category = db.Column(db.String(50), nullable=True, comment='标签分类')
    color = db.Column(db.String(30), nullable=True, comment='标签颜色')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    __table_args__ = (
        UniqueConstraint('account_id', 'name', name='uix_tag_account_name'),
    )

    def __init__(self, account_id, name):
        self.account_id = account_id
        self.name = name
    
    def get_clothes(self):
        """
        获取使用此标签的所有衣物
        :return: 衣物列表
        """
        from app.models.clothes_tag import ClothesTag
        from app.models.clothes import Clothes
        
        # 获取所有关联记录
        clothes_tags = ClothesTag.query.filter_by(account_id=self.account_id, tag_id=self.id).all()
        
        # 获取衣物ID列表
        clothes_ids = [ct.clothes_id for ct in clothes_tags]
        
        # 查询衣物
        if clothes_ids:
            return Clothes.query.filter(
                Clothes.account_id == self.account_id,
                Clothes.id.in_(clothes_ids)
            ).all()
        return []
    
    @classmethod
    def get_by_id(cls, tag_id):
        """
        通过ID获取标签
        :param tag_id: 标签ID
        :return: 标签对象或None
        """
        return cls.query.get(tag_id)
    
    @classmethod
    def get_by_name(cls, account_id, name):
        """
        通过名称获取标签
        :param account_id: 账号ID
        :param name: 标签名称
        :return: 标签对象或None
        """
        return cls.query.filter_by(account_id=account_id, name=name).first()
    
    @classmethod
    def get_or_create(cls, account_id, name):
        """
        获取或创建标签
        :param account_id: 账号ID
        :param name: 标签名称
        :return: 标签对象
        """
        tag = cls.get_by_name(account_id, name)
        if not tag:
            tag = cls(account_id=account_id, name=name)
            db.session.add(tag)
            db.session.commit()
        return tag
    
    @classmethod
    def get_all_by_account(cls, account_id):
        """
        获取账号的所有标签
        :param account_id: 账号ID
        :return: 标签列表
        """
        return cls.query.filter_by(account_id=account_id).all()
    
    def to_dict(self):
        """
        将标签对象转换为字典
        :return: 标签信息字典
        """
        return {
            'id': self.id,
            'account_id': self.account_id,
            'name': self.name,
            'created_at': self.created_at.isoformat()
        } 