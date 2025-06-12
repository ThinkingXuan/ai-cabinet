"""
衣物服务类
"""
import random
from datetime import datetime
from app import db
from app.models.clothes import Clothes
from app.models.clothes_ai_info import ClothesAiInfo
from app.utils.oss_helper import OSSHelper
from app.services.ai_vision_service import AIVisionService

class ClothesService:
    """衣物服务类"""
    
    def __init__(self):
        """初始化"""
        self.oss_helper = OSSHelper()
        self.ai_service = AIVisionService()
    
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
            
            # 创建衣物记录（使用AI识别数据）
            clothes = self._create_clothes_with_ai_recognition(account_id, image_url)
            
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
    
    def _create_clothes_with_ai_recognition(self, account_id, image_url):
        """
        使用AI识别创建衣物记录
        :param account_id: 用户账号ID
        :param image_url: 图片URL
        :return: 衣物对象
        """
        try:
            # 调用AI服务识别图片
            ai_result = self.ai_service.analyze_clothing_image(image_url)
            
            if ai_result["success"]:
                # 从AI识别结果中提取信息
                data = ai_result["data"]
                category = data.get("category", "未分类")
                color = data.get("color", "未知")
                season = data.get("season", "")
                style = data.get("style", "普通")
                confidence = data.get("confidence", 0)
                
                # 创建衣物记录
                clothes = Clothes(
                    account_id=account_id,
                    name=f"{color}{category}",
                    category=category,
                    color=color,
                    season=season,
                    style=style,
                    status="available",
                    image_url=image_url
                )
                
                db.session.add(clothes)
                db.session.commit()
                
                # 创建AI识别信息记录
                self._create_ai_info(account_id, clothes.id, data, confidence)
                
                return clothes
            else:
                # AI识别失败，使用默认数据
                print(f"AI识别失败: {ai_result['message']}")
                return self._create_clothes_with_default_data(account_id, image_url)
                
        except Exception as e:
            db.session.rollback()
            print(f"创建衣物记录失败: {str(e)}")
            return self._create_clothes_with_default_data(account_id, image_url)
    
    def _create_ai_info(self, account_id, clothes_id, ai_data, confidence):
        """
        创建AI识别信息记录
        :param account_id: 用户账号ID
        :param clothes_id: 衣物ID
        :param ai_data: AI识别数据
        :param confidence: 识别置信度
        :return: AI识别信息对象
        """
        try:
            # 创建或更新AI识别信息
            ai_info = ClothesAiInfo.update_ai_info(
                account_id=account_id,
                clothes_id=clothes_id,
                detected_category=ai_data.get("category"),
                detected_color=ai_data.get("color"),
                detected_texture=ai_data.get("texture", None),  # 纹理可能不存在
                ai_confidence=float(confidence) / 100.0 if confidence else None  # 转换为0-1范围
            )
            return ai_info
        except Exception as e:
            print(f"创建AI识别信息失败: {str(e)}")
            return None
    
    def _create_clothes_with_default_data(self, account_id, image_url):
        """
        使用默认数据创建衣物记录（当AI识别失败时使用）
        :param account_id: 用户账号ID
        :param image_url: 图片URL
        :return: 衣物对象
        """
        # 默认数据
        categories = ["上衣", "裤子", "裙子", "外套", "鞋子", "配饰"]
        colors = ["红色", "蓝色", "黑色", "白色", "灰色", "粉色", "黄色", "绿色"]
        seasons = ["spring", "summer", "autumn", "winter"]
        styles = ["休闲", "正式", "运动", "复古", "时尚", "简约"]
        
        # 随机选择默认数据
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
    
    def update_clothes(self, account_id, clothes_id, name=None, category=None, color=None, season=None, style=None):
        """
        更新衣物信息
        :param account_id: 用户账号ID
        :param clothes_id: 衣物ID
        :param name: 衣物名称
        :param category: 分类
        :param color: 颜色
        :param season: 季节
        :param style: 风格
        :return: 更新结果字典
        """
        # 查询衣物
        clothes = self.get_clothes_by_id(account_id, clothes_id)
        
        if not clothes:
            return {
                "success": False,
                "message": "衣物不存在"
            }
        
        try:
            # 更新字段
            if name is not None:
                clothes.name = name
            
            if category is not None:
                clothes.category = category
            
            if color is not None:
                clothes.color = color
            
            if season is not None:
                clothes.season_list = season.split(',') if isinstance(season, str) else season
            
            if style is not None:
                clothes.style = style
            
            # 保存更新
            db.session.commit()
            
            return {
                "success": True,
                "data": clothes.to_dict()
            }
        
        except Exception as e:
            db.session.rollback()
            print(f"更新衣物失败: {str(e)}")
            return {
                "success": False,
                "message": f"更新衣物失败: {str(e)}"
            }
    
    def reanalyze_clothes(self, account_id, clothes_id):
        """
        重新使用AI识别衣物
        :param account_id: 用户账号ID
        :param clothes_id: 衣物ID
        :return: AI识别结果字典
        """
        # 查询衣物
        clothes = self.get_clothes_by_id(account_id, clothes_id)
        
        if not clothes:
            return {
                "success": False,
                "message": "衣物不存在"
            }
        
        # 检查衣物是否有图片URL
        if not clothes.image_url:
            return {
                "success": False,
                "message": "衣物没有图片，无法进行AI识别"
            }
        
        try:
            # 调用AI服务识别图片
            ai_result = self.ai_service.analyze_clothing_image(clothes.image_url)
            
            if ai_result["success"]:
                # 从AI识别结果中提取信息
                data = ai_result["data"]
                confidence = data.get("confidence", 0)
                
                # 更新AI识别信息记录
                ai_info = self._create_ai_info(account_id, clothes_id, data, confidence)
                
                # 返回AI识别结果，但不更新clothes表
                return {
                    "success": True,
                    "result": {
                        "message": "AI识别成功",
                        "ai_result": data,
                        "clothes_id": clothes_id,
                        "image_url": clothes.image_url
                    }
                }
            else:
                return {
                    "success": False,
                    "message": f"AI识别失败: {ai_result['message']}",
                    "raw_response": ai_result.get("raw_response")
                }
                
        except Exception as e:
            print(f"重新识别衣物失败: {str(e)}")
            return {
                "success": False,
                "message": f"重新识别衣物失败: {str(e)}"
            } 