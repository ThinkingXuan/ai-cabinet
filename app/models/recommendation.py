from datetime import datetime
from app import db

class Recommendation(db.Model):
    """穿搭推荐模型"""
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='推荐ID')
    account_id = db.Column(db.String(64), nullable=False, index=True, comment='所属账号ID')
    outfit_id = db.Column(db.Integer, nullable=True, comment='推荐的穿搭ID')
    reason = db.Column(db.String(255), nullable=True, comment='推荐理由')
    recommendation_type = db.Column(db.String(50), nullable=True, comment='推荐类型')
    weather_condition = db.Column(db.String(50), nullable=True, comment='天气条件')
    occasion = db.Column(db.String(50), nullable=True, comment='场合')
    is_viewed = db.Column(db.Boolean, default=False, comment='是否已查看')
    is_liked = db.Column(db.Boolean, default=False, comment='是否喜欢')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    def __init__(self, account_id, date, outfit_id=None, feedback='neutral', generated_by_ai=True):
        self.account_id = account_id
        self.date = date
        self.outfit_id = outfit_id
        self.feedback = feedback
        self.generated_by_ai = generated_by_ai
    
    def set_feedback(self, feedback):
        """
        设置用户反馈
        :param feedback: 反馈类型
        """
        if feedback in ['like', 'dislike', 'neutral']:
            self.feedback = feedback
            db.session.commit()
    
    @classmethod
    def get_by_id(cls, recommendation_id):
        """
        通过ID获取推荐记录
        :param recommendation_id: 推荐记录ID
        :return: 推荐记录对象或None
        """
        return cls.query.get(recommendation_id)
    
    @classmethod
    def get_by_date(cls, account_id, date):
        """
        通过日期获取推荐记录
        :param account_id: 账号ID
        :param date: 日期
        :return: 推荐记录对象或None
        """
        return cls.query.filter_by(account_id=account_id, date=date).first()
    
    @classmethod
    def get_by_outfit(cls, account_id, outfit_id):
        """
        通过搭配ID获取推荐记录
        :param account_id: 账号ID
        :param outfit_id: 搭配ID
        :return: 推荐记录列表
        """
        return cls.query.filter_by(account_id=account_id, outfit_id=outfit_id).all()
    
    @classmethod
    def get_by_feedback(cls, account_id, feedback):
        """
        通过反馈类型获取推荐记录
        :param account_id: 账号ID
        :param feedback: 反馈类型
        :return: 推荐记录列表
        """
        return cls.query.filter_by(account_id=account_id, feedback=feedback).all()
    
    def to_dict(self):
        """
        将推荐记录对象转换为字典
        :return: 推荐记录信息字典
        """
        return {
            'id': self.id,
            'account_id': self.account_id,
            'date': self.date.isoformat(),
            'outfit_id': self.outfit_id,
            'feedback': self.feedback,
            'generated_by_ai': self.generated_by_ai,
            'created_at': self.created_at.isoformat()
        } 