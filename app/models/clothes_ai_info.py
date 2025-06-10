from datetime import datetime
from app import db
from sqlalchemy import UniqueConstraint

class ClothesAiInfo(db.Model):
    """衣物AI识别信息模型"""
    __tablename__ = 'clothes_ai_info'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='识别记录ID')
    account_id = db.Column(db.String(64), nullable=False, index=True, comment='所属账号')
    clothes_id = db.Column(db.Integer, nullable=False, comment='衣物ID')
    detected_category = db.Column(db.String(50), nullable=True, comment='AI识别分类')
    detected_color = db.Column(db.String(30), nullable=True, comment='AI识别颜色')
    detected_texture = db.Column(db.String(50), nullable=True, comment='纹理/图案')
    ai_confidence = db.Column(db.Numeric(5, 2), nullable=True, comment='识别置信度')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 添加联合唯一约束
    __table_args__ = (
        UniqueConstraint('account_id', 'clothes_id', name='uix_ai_info_account_clothes'),
    )

    def __init__(self, account_id, clothes_id, detected_category=None, 
                 detected_color=None, detected_texture=None, ai_confidence=None):
        self.account_id = account_id
        self.clothes_id = clothes_id
        self.detected_category = detected_category
        self.detected_color = detected_color
        self.detected_texture = detected_texture
        self.ai_confidence = ai_confidence
    
    def get_clothes(self):
        """
        获取关联的衣物
        :return: 衣物对象或None
        """
        from app.models.clothes import Clothes
        return Clothes.get_by_id(self.account_id, self.clothes_id)
    
    @classmethod
    def get_by_clothes_id(cls, account_id, clothes_id):
        """
        通过衣物ID获取AI识别信息
        :param account_id: 账号ID
        :param clothes_id: 衣物ID
        :return: AI识别信息对象或None
        """
        return cls.query.filter_by(account_id=account_id, clothes_id=clothes_id).first()
    
    @classmethod
    def get_or_create(cls, account_id, clothes_id):
        """
        获取或创建AI识别信息
        :param account_id: 账号ID
        :param clothes_id: 衣物ID
        :return: AI识别信息对象
        """
        ai_info = cls.get_by_clothes_id(account_id, clothes_id)
        if not ai_info:
            ai_info = cls(account_id=account_id, clothes_id=clothes_id)
            db.session.add(ai_info)
            db.session.commit()
        return ai_info
    
    @classmethod
    def update_ai_info(cls, account_id, clothes_id, detected_category=None, 
                      detected_color=None, detected_texture=None, ai_confidence=None):
        """
        更新AI识别信息
        :param account_id: 账号ID
        :param clothes_id: 衣物ID
        :param detected_category: AI识别分类
        :param detected_color: AI识别颜色
        :param detected_texture: 纹理/图案
        :param ai_confidence: 识别置信度
        :return: AI识别信息对象
        """
        ai_info = cls.get_or_create(account_id, clothes_id)
        
        if detected_category is not None:
            ai_info.detected_category = detected_category
        if detected_color is not None:
            ai_info.detected_color = detected_color
        if detected_texture is not None:
            ai_info.detected_texture = detected_texture
        if ai_confidence is not None:
            ai_info.ai_confidence = ai_confidence
            
        db.session.commit()
        return ai_info
    
    def to_dict(self):
        """
        将AI识别信息对象转换为字典
        :return: AI识别信息字典
        """
        return {
            'id': self.id,
            'account_id': self.account_id,
            'clothes_id': self.clothes_id,
            'detected_category': self.detected_category,
            'detected_color': self.detected_color,
            'detected_texture': self.detected_texture,
            'ai_confidence': float(self.ai_confidence) if self.ai_confidence is not None else None,
            'updated_at': self.updated_at.isoformat()
        } 