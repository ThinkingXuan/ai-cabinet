from datetime import datetime
from app import db
from sqlalchemy import UniqueConstraint

class ClothesTag(db.Model):
    """衣物标签关联模型"""
    __tablename__ = 'clothes_tags'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='关联ID')
    account_id = db.Column(db.String(64), nullable=False, index=True, comment='所属账号ID')
    clothes_id = db.Column(db.Integer, nullable=False, comment='衣物ID')
    tag_id = db.Column(db.Integer, nullable=False, comment='标签ID')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    # 添加索引
    __table_args__ = (
        db.Index('idx_clothes_tag_unique', 'account_id', 'clothes_id', 'tag_id', unique=True),
        UniqueConstraint('clothes_id', 'tag_id', name='uix_clothes_tag'),
    )

    def __init__(self, account_id, clothes_id, tag_id):
        self.account_id = account_id
        self.clothes_id = clothes_id
        self.tag_id = tag_id
    
    def get_clothes(self):
        """
        获取关联的衣物
        :return: 衣物对象或None
        """
        from app.models.clothes import Clothes
        return Clothes.get_by_id(self.account_id, self.clothes_id)
    
    def get_tag(self):
        """
        获取关联的标签
        :return: 标签对象或None
        """
        from app.models.tag import Tag
        return Tag.get_by_id(self.tag_id)
    
    @classmethod
    def get_by_clothes(cls, account_id, clothes_id):
        """
        获取衣物的所有标签关联
        :param account_id: 账号ID
        :param clothes_id: 衣物ID
        :return: 关联记录列表
        """
        return cls.query.filter_by(account_id=account_id, clothes_id=clothes_id).all()
    
    @classmethod
    def get_by_tag(cls, account_id, tag_id):
        """
        获取标签关联的所有衣物
        :param account_id: 账号ID
        :param tag_id: 标签ID
        :return: 关联记录列表
        """
        return cls.query.filter_by(account_id=account_id, tag_id=tag_id).all()
    
    @classmethod
    def delete_by_clothes(cls, account_id, clothes_id):
        """
        删除衣物的所有标签关联
        :param account_id: 账号ID
        :param clothes_id: 衣物ID
        """
        cls.query.filter_by(account_id=account_id, clothes_id=clothes_id).delete()
        db.session.commit()
    
    @classmethod
    def delete_by_tag(cls, account_id, tag_id):
        """
        删除标签的所有衣物关联
        :param account_id: 账号ID
        :param tag_id: 标签ID
        """
        cls.query.filter_by(account_id=account_id, tag_id=tag_id).delete()
        db.session.commit() 