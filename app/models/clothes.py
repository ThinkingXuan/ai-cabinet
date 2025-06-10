from datetime import datetime
import json
from app import db

class Clothes(db.Model):
    """衣物模型"""
    __tablename__ = 'clothes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='衣物ID')
    account_id = db.Column(db.String(64), nullable=False, index=True, comment='所属账号ID')
    name = db.Column(db.String(100), nullable=True, comment='衣物名称')
    category = db.Column(db.String(50), nullable=True, comment='分类，如上衣、裤子')
    color = db.Column(db.String(30), nullable=True, comment='主色调')
    season = db.Column(db.String(50), nullable=True, comment='适合季节，SET类型：spring,summer,autumn,winter')
    style = db.Column(db.String(50), nullable=True, comment='风格')
    status = db.Column(db.Enum('available', 'dirty', 'laundry', 'lost', 'discarded'), 
                     default='available', comment='状态')
    image_url = db.Column(db.String(255), nullable=True, comment='衣物图片URL')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')

    def __init__(self, account_id, name=None, category=None, color=None, 
                 season=None, style=None, status='available', image_url=None):
        self.account_id = account_id
        self.name = name
        self.category = category
        self.color = color
        self.season = season  # MySQL SET类型，存储为逗号分隔的字符串，如 "spring,summer"
        self.style = style
        self.status = status
        self.image_url = image_url

    @property
    def season_list(self):
        """
        获取季节列表
        :return: 季节列表
        """
        if not self.season:
            return []
        return self.season.split(',')
    
    @season_list.setter
    def season_list(self, seasons):
        """
        设置季节列表
        :param seasons: 季节列表，可选值：spring, summer, autumn, winter
        """
        valid_seasons = ['spring', 'summer', 'autumn', 'winter']
        if not seasons:
            self.season = None
        else:
            # 过滤无效的季节值
            valid_input = [s for s in seasons if s in valid_seasons]
            if valid_input:
                self.season = ','.join(valid_input)
            else:
                self.season = None
    
    def get_ai_info(self):
        """
        获取AI识别信息
        :return: AI识别信息对象或None
        """
        from app.models.clothes_ai_info import ClothesAiInfo
        return ClothesAiInfo.query.filter_by(account_id=self.account_id, clothes_id=self.id).first()
    
    def get_tags(self):
        """
        获取衣物的所有标签
        :return: 标签列表
        """
        from app.models.clothes_tag import ClothesTag
        from app.models.tag import Tag
        
        # 获取所有关联记录
        clothes_tags = ClothesTag.query.filter_by(account_id=self.account_id, clothes_id=self.id).all()
        
        # 获取标签ID列表
        tag_ids = [ct.tag_id for ct in clothes_tags]
        
        # 查询标签
        if tag_ids:
            return Tag.query.filter(Tag.id.in_(tag_ids)).all()
        return []
    
    def add_tag(self, tag):
        """
        添加标签
        :param tag: 标签对象
        """
        from app.models.clothes_tag import ClothesTag
        
        if not self.has_tag(tag):
            clothes_tag = ClothesTag(account_id=self.account_id, clothes_id=self.id, tag_id=tag.id)
            db.session.add(clothes_tag)
            db.session.commit()
    
    def remove_tag(self, tag):
        """
        移除标签
        :param tag: 标签对象
        """
        from app.models.clothes_tag import ClothesTag
        
        clothes_tag = ClothesTag.query.filter_by(
            account_id=self.account_id, 
            clothes_id=self.id, 
            tag_id=tag.id
        ).first()
        
        if clothes_tag:
            db.session.delete(clothes_tag)
            db.session.commit()
    
    def has_tag(self, tag):
        """
        检查是否有某个标签
        :param tag: 标签对象
        :return: 布尔值
        """
        from app.models.clothes_tag import ClothesTag
        
        return ClothesTag.query.filter_by(
            account_id=self.account_id, 
            clothes_id=self.id, 
            tag_id=tag.id
        ).count() > 0
    
    @classmethod
    def get_by_id(cls, account_id, clothes_id):
        """
        通过ID获取衣物
        :param account_id: 账号ID
        :param clothes_id: 衣物ID
        :return: 衣物对象或None
        """
        return cls.query.filter_by(account_id=account_id, id=clothes_id).first()
    
    @classmethod
    def get_by_category(cls, account_id, category):
        """
        通过分类获取衣物
        :param account_id: 账号ID
        :param category: 分类
        :return: 衣物列表
        """
        return cls.query.filter_by(account_id=account_id, category=category).all()
    
    @classmethod
    def get_by_status(cls, account_id, status):
        """
        通过状态获取衣物
        :param account_id: 账号ID
        :param status: 状态
        :return: 衣物列表
        """
        return cls.query.filter_by(account_id=account_id, status=status).all()
    
    @classmethod
    def get_by_season(cls, account_id, season):
        """
        通过季节获取衣物
        :param account_id: 账号ID
        :param season: 季节
        :return: 衣物列表
        """
        return cls.query.filter(
            cls.account_id == account_id,
            cls.season.like(f'%{season}%')
        ).all()
    
    def to_dict(self):
        """
        将衣物对象转换为字典
        :return: 衣物信息字典
        """
        return {
            'id': self.id,
            'account_id': self.account_id,
            'name': self.name,
            'category': self.category,
            'color': self.color,
            'season': self.season_list,
            'style': self.style,
            'status': self.status,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat()
        } 