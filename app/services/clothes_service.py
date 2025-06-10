"""
衣物服务类
"""
import random
from datetime import datetime
from app import db
from app.models.clothes import Clothes
from app.utils.oss_helper import OSSHelper

class ClothesService:
    """衣物服务类"""
    
    def __init__(self):
        """初始化"""
        self.oss_helper = OSSHelper()
    
    def upload_clothes_images(self, account_id, files):
        """
        上传衣物图片
        :param account_id: 用户账号ID
        :param files: 文件列表
        :return: 上传结果列表
        """
        if not files or len(files) == 0:
            return {"success": False, "message": "没有上传文件"}
        
        result = []
        
        for file in files:
            # 上传文件到OSS
            object_key = self.oss_helper.upload_file(account_id, file)
            
            if not object_key:
                result.append({
                    "filename": file.filename,
                    "success": False,
                    "message": "文件上传失败"
                })
                continue
            
            # 生成图片URL
            image_url = self.oss_helper.get_public_url(object_key)
            
            # 创建衣物记录（使用mock数据）
            clothes = self._create_clothes_with_mock_data(account_id, image_url)
            
            if clothes:
                result.append({
                    "filename": file.filename,
                    "success": True,
                    "clothes_id": clothes.id,
                    "image_url": image_url
                })
            else:
                result.append({
                    "filename": file.filename,
                    "success": False,
                    "message": "创建衣物记录失败"
                })
                # 删除已上传的文件
                self.oss_helper.delete_object(object_key)
        
        return {
            "success": any(item["success"] for item in result),
            "total": len(files),
            "success_count": sum(1 for item in result if item["success"]),
            "failed_count": sum(1 for item in result if not item["success"]),
            "items": result
        }
    
    def _create_clothes_with_mock_data(self, account_id, image_url):
        """
        使用mock数据创建衣物记录
        :param account_id: 用户账号ID
        :param image_url: 图片URL
        :return: 衣物对象
        """
        # Mock数据
        categories = ["上衣", "裤子", "裙子", "外套", "鞋子", "配饰"]
        colors = ["红色", "蓝色", "黑色", "白色", "灰色", "粉色", "黄色", "绿色"]
        seasons = ["spring", "summer", "autumn", "winter"]
        styles = ["休闲", "正式", "运动", "复古", "时尚", "简约"]
        
        # 随机选择mock数据
        category = random.choice(categories)
        color = random.choice(colors)
        season = ",".join(random.sample(seasons, random.randint(1, 3)))
        style = random.choice(styles)
        name = f"{color}{category}"
        
        try:
            # 创建衣物记录
            clothes = Clothes(
                account_id=account_id,
                name=name,
                category=category,
                color=color,
                season=season,
                style=style,
                status="available",
                image_url=image_url
            )
            
            db.session.add(clothes)
            db.session.commit()
            
            return clothes
        except Exception as e:
            db.session.rollback()
            print(f"创建衣物记录失败: {str(e)}")
            return None
    
    def get_clothes_by_id(self, account_id, clothes_id):
        """
        通过ID获取衣物
        :param account_id: 用户账号ID
        :param clothes_id: 衣物ID
        :return: 衣物对象
        """
        return Clothes.get_by_id(account_id, clothes_id)
    
    def get_clothes_list(self, account_id, category=None, status=None, season=None):
        """
        获取衣物列表
        :param account_id: 用户账号ID
        :param category: 分类
        :param status: 状态
        :param season: 季节
        :return: 衣物列表
        """
        query = Clothes.query.filter_by(account_id=account_id)
        
        if category:
            query = query.filter_by(category=category)
        
        if status:
            query = query.filter_by(status=status)
        
        if season:
            query = query.filter(Clothes.season.like(f'%{season}%'))
        
        return query.all() 