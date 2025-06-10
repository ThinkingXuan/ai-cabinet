from datetime import datetime
from app import db

class WeatherLog(db.Model):
    """天气记录模型"""
    __tablename__ = 'weather_logs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='记录ID')
    account_id = db.Column(db.String(64), nullable=False, index=True, comment='所属账号ID')
    date = db.Column(db.Date, nullable=False, comment='日期')
    location = db.Column(db.String(100), nullable=True, comment='位置')
    temperature = db.Column(db.Numeric(5, 2), nullable=True, comment='温度')
    weather_condition = db.Column(db.String(50), nullable=True, comment='天气情况')
    humidity = db.Column(db.Integer, nullable=True, comment='湿度')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')

    def __init__(self, account_id, date, location=None, temperature=None, condition=None):
        self.account_id = account_id
        self.date = date
        self.location = location
        self.temperature = temperature
        self.condition = condition
    
    @classmethod
    def get_by_id(cls, weather_log_id):
        """
        通过ID获取天气记录
        :param weather_log_id: 天气记录ID
        :return: 天气记录对象或None
        """
        return cls.query.get(weather_log_id)
    
    @classmethod
    def get_by_date(cls, account_id, date):
        """
        通过日期获取天气记录
        :param account_id: 账号ID
        :param date: 日期
        :return: 天气记录对象或None
        """
        return cls.query.filter_by(account_id=account_id, date=date).first()
    
    @classmethod
    def get_by_location(cls, account_id, location):
        """
        通过位置获取天气记录
        :param account_id: 账号ID
        :param location: 位置
        :return: 天气记录列表
        """
        return cls.query.filter_by(account_id=account_id, location=location).all()
    
    @classmethod
    def get_by_date_range(cls, account_id, start_date, end_date):
        """
        通过日期范围获取天气记录
        :param account_id: 账号ID
        :param start_date: 开始日期
        :param end_date: 结束日期
        :return: 天气记录列表
        """
        return cls.query.filter(
            cls.account_id == account_id,
            cls.date >= start_date,
            cls.date <= end_date
        ).all()
    
    def to_dict(self):
        """
        将天气记录对象转换为字典
        :return: 天气记录信息字典
        """
        return {
            'id': self.id,
            'account_id': self.account_id,
            'date': self.date.isoformat(),
            'location': self.location,
            'temperature': float(self.temperature) if self.temperature is not None else None,
            'condition': self.condition,
            'created_at': self.created_at.isoformat()
        } 