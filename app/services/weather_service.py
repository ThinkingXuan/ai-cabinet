"""
天气记录服务类
"""
from datetime import datetime
from app import db
from app.models.weather_log import WeatherLog

class WeatherService:
    """天气记录服务类"""
    
    @staticmethod
    def create_weather(account_id, date, location=None, temperature=None, 
                      weather_condition=None, humidity=None, wind_speed=None):
        """
        创建天气记录
        :param account_id: 用户账号ID
        :param date: 日期
        :param location: 位置
        :param temperature: 温度
        :param weather_condition: 天气状况
        :param humidity: 湿度
        :param wind_speed: 风速
        :return: 天气记录对象
        """
        # 检查当天是否已有记录
        existing_weather = WeatherLog.get_by_date(account_id, date)
        
        if existing_weather:
            # 更新已有记录
            if location is not None:
                existing_weather.location = location
            if temperature is not None:
                existing_weather.temperature = temperature
            if weather_condition is not None:
                existing_weather.weather_condition = weather_condition
            if humidity is not None:
                existing_weather.humidity = humidity
            if wind_speed is not None:
                existing_weather.wind_speed = wind_speed
                
            db.session.commit()
            return existing_weather
        
        # 创建新记录
        weather = WeatherLog(
            account_id=account_id,
            date=date,
            location=location,
            temperature=temperature,
            weather_condition=weather_condition,
            humidity=humidity,
            wind_speed=wind_speed
        )
        
        db.session.add(weather)
        db.session.commit()
        
        return weather
    
    @staticmethod
    def get_weather_by_date(account_id, date):
        """
        获取指定日期的天气记录
        :param account_id: 用户账号ID
        :param date: 日期
        :return: 天气记录对象或None
        """
        return WeatherLog.get_by_date(account_id, date)
    
    @staticmethod
    def get_weather_by_date_range(account_id, start_date, end_date):
        """
        获取日期范围内的天气记录
        :param account_id: 用户账号ID
        :param start_date: 开始日期
        :param end_date: 结束日期
        :return: 天气记录列表
        """
        return WeatherLog.get_by_date_range(account_id, start_date, end_date)
    
    @staticmethod
    def get_weather_by_location(account_id, location):
        """
        获取指定位置的天气记录
        :param account_id: 用户账号ID
        :param location: 位置
        :return: 天气记录列表
        """
        return WeatherLog.get_by_location(account_id, location)
    
    @staticmethod
    def update_weather(account_id, weather_id, date=None, location=None, temperature=None, 
                      weather_condition=None, humidity=None, wind_speed=None):
        """
        更新天气记录
        :param account_id: 用户账号ID
        :param weather_id: 天气记录ID
        :param date: 日期
        :param location: 位置
        :param temperature: 温度
        :param weather_condition: 天气状况
        :param humidity: 湿度
        :param wind_speed: 风速
        :return: 更新后的天气记录对象或None
        """
        weather = WeatherLog.query.filter_by(id=weather_id, account_id=account_id).first()
        
        if not weather:
            return None
        
        if date is not None:
            weather.date = date
        if location is not None:
            weather.location = location
        if temperature is not None:
            weather.temperature = temperature
        if weather_condition is not None:
            weather.weather_condition = weather_condition
        if humidity is not None:
            weather.humidity = humidity
        if wind_speed is not None:
            weather.wind_speed = wind_speed
            
        db.session.commit()
        
        return weather
    
    @staticmethod
    def delete_weather(account_id, weather_id):
        """
        删除天气记录
        :param account_id: 用户账号ID
        :param weather_id: 天气记录ID
        :return: 布尔值，表示是否删除成功
        """
        weather = WeatherLog.query.filter_by(id=weather_id, account_id=account_id).first()
        
        if not weather:
            return False
        
        db.session.delete(weather)
        db.session.commit()
        
        return True

    @staticmethod
    def get_current_weather(account_id):
        """
        获取当前天气信息
        :param account_id: 账号ID
        :return: 天气信息字典
        """
        # 获取今天的日期
        today = datetime.now().date()
        
        # 查询今天的天气记录
        weather_log = WeatherLog.get_by_date(account_id, today)
        
        if weather_log:
            return {
                'weather': weather_log.weather_condition,
                'temperature': float(weather_log.temperature) if weather_log.temperature is not None else None,
                'season': WeatherService.get_season_by_date(today)
            }
        
        # 如果没有记录，返回默认值
        return {
            'weather': None,
            'temperature': None,
            'season': WeatherService.get_season_by_date(today)
        }
    
    @staticmethod
    def get_season_by_date(date=None):
        """
        根据日期计算季节
        :param date: 日期，默认为当前日期
        :return: 季节名称（春、夏、秋、冬）
        """
        if date is None:
            date = datetime.now().date()
        
        # 获取月份
        month = date.month
        
        # 根据月份判断季节
        if 3 <= month <= 5:
            return '春季'
        elif 6 <= month <= 8:
            return '夏季'
        elif 9 <= month <= 11:
            return '秋季'
        else:  # 12, 1, 2
            return '冬季'
    
    @staticmethod
    def get_latest_weather(account_id, days=7):
        """
        获取最近几天的天气记录
        :param account_id: 账号ID
        :param days: 天数，默认7天
        :return: 天气记录列表
        """
        # 获取最近的天气记录
        weather_logs = db.session.query(WeatherLog)\
            .filter_by(account_id=account_id)\
            .order_by(WeatherLog.date.desc())\
            .limit(days)\
            .all()
        
        return [log.to_dict() for log in weather_logs] 