from datetime import datetime
import json
from app import db

class Outfit(db.Model):
    """穿搭模型"""
    __tablename__ = 'outfits'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='穿搭ID')
    account_id = db.Column(db.String(64), nullable=False, index=True, comment='所属账号ID')
    name = db.Column(db.String(100), nullable=True, comment='穿搭名称')
    description = db.Column(db.Text, nullable=True, comment='穿搭描述')
    style = db.Column(db.String(50), nullable=True, comment='风格')
    season = db.Column(db.String(50), nullable=True, comment='适合季节')
    occasion = db.Column(db.String(50), nullable=True, comment='适合场合')
    clothes_items = db.Column(db.Text, nullable=True, comment='包含的衣物ID列表，JSON格式')
    image_url = db.Column(db.String(255), nullable=True, comment='穿搭图片URL')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')

    def __init__(self, account_id, name=None, clothes_items=None, image_url=None, description=None, style=None, season=None, occasion=None):
        self.account_id = account_id
        self.name = name
        self.set_clothes_items(clothes_items or [])
        self.image_url = image_url
        self.description = description
        self.style = style
        self.season = season
        self.occasion = occasion
    
    def get_clothes_items(self):
        """
        获取穿搭包含的衣物ID列表
        :return: 衣物ID列表
        """
        if not self.clothes_items:
            return []
        return json.loads(self.clothes_items)
    
    def set_clothes_items(self, clothes_ids):
        """
        设置穿搭包含的衣物ID列表
        :param clothes_ids: 衣物ID列表
        """
        self.clothes_items = json.dumps(clothes_ids)
    
    def add_clothes(self, clothes_id):
        """
        添加衣物到穿搭
        :param clothes_id: 衣物ID
        """
        clothes_ids = self.get_clothes_items()
        if clothes_id not in clothes_ids:
            clothes_ids.append(clothes_id)
            self.set_clothes_items(clothes_ids)
            db.session.commit()
    
    def remove_clothes(self, clothes_id):
        """
        从穿搭中移除衣物
        :param clothes_id: 衣物ID
        """
        clothes_ids = self.get_clothes_items()
        if clothes_id in clothes_ids:
            clothes_ids.remove(clothes_id)
            self.set_clothes_items(clothes_ids)
            db.session.commit()
    
    def get_clothes(self):
        """
        获取穿搭包含的衣物对象列表
        :return: 衣物对象列表
        """
        from app.models.clothes import Clothes
        clothes_ids = self.get_clothes_items()
        if not clothes_ids:
            return []
        return Clothes.query.filter(Clothes.id.in_(clothes_ids)).all()
    
    @classmethod
    def get_by_id(cls, account_id, outfit_id):
        """
        通过ID获取穿搭
        :param account_id: 账号ID
        :param outfit_id: 穿搭ID
        :return: 穿搭对象或None
        """
        return cls.query.filter_by(account_id=account_id, id=outfit_id).first()
    
    @classmethod
    def get_all_by_account(cls, account_id):
        """
        获取账号的所有穿搭
        :param account_id: 账号ID
        :return: 穿搭列表
        """
        return cls.query.filter_by(account_id=account_id).all()
    
    def to_dict(self):
        """
        将穿搭对象转换为字典
        :return: 穿搭信息字典
        """
        return {
            'id': self.id,
            'account_id': self.account_id,
            'name': self.name,
            'description': self.description,
            'style': self.style,
            'season': self.season,
            'occasion': self.occasion,
            'clothes_items': self.get_clothes_items(),
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat()
        } 