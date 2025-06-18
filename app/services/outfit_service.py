from app import db
from app.models.outfit import Outfit
from app.models.clothes import Clothes

class OutfitService:
    """穿搭服务类"""
    
    @staticmethod
    def create_outfit(account_id, name, clothes_items, image_url=None, description=None, style=None, season=None, occasion=None):
        """
        创建新穿搭
        :param account_id: 用户账号ID
        :param name: 穿搭名称
        :param clothes_items: 包含的衣物ID列表
        :param image_url: 穿搭图片URL
        :param description: 穿搭描述
        :param style: 风格
        :param season: 适合季节
        :param occasion: 适合场合
        :return: 穿搭对象
        """
        # 验证衣物ID是否都属于当前用户
        if clothes_items and len(clothes_items) > 0:
            valid_clothes = Clothes.query.filter(
                Clothes.id.in_(clothes_items),
                Clothes.account_id == account_id
            ).all()
            
            # 如果有无效的衣物ID，则过滤掉
            valid_clothes_ids = [clothes.id for clothes in valid_clothes]
            clothes_items = [item_id for item_id in clothes_items if item_id in valid_clothes_ids]
        
        # 创建穿搭
        outfit = Outfit(
            account_id=account_id, 
            name=name, 
            clothes_items=clothes_items, 
            image_url=image_url,
            description=description,
            style=style,
            season=season,
            occasion=occasion
        )
        
        # 保存到数据库
        db.session.add(outfit)
        db.session.commit()
        
        return outfit
    
    @staticmethod
    def get_outfit_list(account_id, style=None, season=None, occasion=None):
        """
        获取穿搭列表
        :param account_id: 用户账号ID
        :param style: 风格过滤
        :param season: 季节过滤
        :param occasion: 场合过滤
        :return: 穿搭列表
        """
        query = Outfit.query.filter_by(account_id=account_id)
        
        if style:
            query = query.filter_by(style=style)
        
        if season:
            query = query.filter_by(season=season)
        
        if occasion:
            query = query.filter_by(occasion=occasion)
        
        # 按创建时间倒序排列
        query = query.order_by(Outfit.created_at.desc())
        
        return query.all()
    
    @staticmethod
    def get_outfit_by_id(account_id, outfit_id):
        """
        通过ID获取穿搭
        :param account_id: 账号ID
        :param outfit_id: 穿搭ID
        :return: 穿搭对象或None
        """
        return Outfit.get_by_id(account_id, outfit_id)
    
    @staticmethod
    def delete_outfit(account_id, outfit_id):
        """
        删除穿搭
        :param account_id: 账号ID
        :param outfit_id: 穿搭ID
        :return: 布尔值，表示是否删除成功
        """
        outfit = Outfit.get_by_id(account_id, outfit_id)
        
        if outfit:
            db.session.delete(outfit)
            db.session.commit()
            return True
        
        return False 