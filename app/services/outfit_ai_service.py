"""
AI穿搭推荐服务
"""
import json
import random
from openai import OpenAI
from config import Config
from app import db
from app.models.clothes import Clothes
from app.models.outfit import Outfit

class OutfitAIService:
    """AI穿搭推荐服务类"""
    
    def __init__(self):
        """初始化OpenAI客户端"""
        self.api_key = Config.OPENAI_API_KEY
        self.model = Config.OPENAI_MODEL
        self.max_retries = Config.OPENAI_MAX_RETRIES
        
        # 初始化OpenAI客户端
        self.client = OpenAI(
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            api_key=self.api_key
        )
    
    def generate_outfit(self, account_id, occasion=None, season=None, style_preference=None, 
                        weather=None, temperature=None, exclude_clothes_ids=None):
        """
        生成穿搭推荐
        :param account_id: 用户账号ID
        :param occasion: 场合
        :param season: 季节
        :param style_preference: 风格偏好
        :param weather: 天气
        :param temperature: 温度
        :param exclude_clothes_ids: 排除的衣物ID列表
        :return: 生成的穿搭对象或错误信息
        """
        # 获取用户可用的衣物
        available_clothes = self._get_available_clothes(account_id, exclude_clothes_ids)
        
        if not available_clothes:
            return {"success": False, "message": "没有可用的衣物进行搭配"}
        
        # 根据过滤条件筛选衣物
        filtered_clothes = self._filter_clothes(available_clothes, season, style_preference)
        
        if not filtered_clothes:
            # 如果过滤后没有衣物，则使用所有可用衣物
            filtered_clothes = available_clothes
        
        # 格式化衣物数据
        clothes_data = self._format_clothes_data(filtered_clothes)
        
        # 构建提示词
        system_prompt, user_prompt = self._build_prompts(
            clothes_data, occasion, season, style_preference, weather, temperature
        )
        
        # 调用OpenAI API
        response = self._call_openai_api(system_prompt, user_prompt)
        
        if not response.get("success", False):
            return response
        
        # 解析响应结果
        result = self._parse_response(response.get("data", {}))
        
        if not result.get("success", False):
            return result
        
        # 创建穿搭
        outfit_data = result.get("data", {})
        clothes_ids = outfit_data.get("clothes_ids", [])
        
        # 验证推荐的衣物都存在
        valid_clothes_ids = self._validate_clothes_ids(account_id, clothes_ids)
        
        if not valid_clothes_ids:
            return {"success": False, "message": "AI推荐的衣物不可用"}
        
        # 创建穿搭对象
        outfit = Outfit(
            account_id=account_id,
            name=outfit_data.get("name", "AI推荐穿搭"),
            clothes_items=valid_clothes_ids,
            description=outfit_data.get("reasoning", "AI自动生成的穿搭推荐"),
            style=style_preference or outfit_data.get("style"),
            season=season or outfit_data.get("season"),
            occasion=occasion or outfit_data.get("occasion")
        )
        
        db.session.add(outfit)
        db.session.commit()
        
        return {"success": True, "outfit": outfit}
    
    def _get_available_clothes(self, account_id, exclude_clothes_ids=None):
        """
        获取用户可用的衣物
        :param account_id: 用户账号ID
        :param exclude_clothes_ids: 排除的衣物ID列表
        :return: 可用衣物列表
        """
        query = Clothes.query.filter_by(account_id=account_id, status='available')
        
        if exclude_clothes_ids:
            query = query.filter(~Clothes.id.in_(exclude_clothes_ids))
        
        return query.all()
    
    def _filter_clothes(self, clothes_list, season=None, style=None):
        """
        根据条件筛选衣物
        :param clothes_list: 衣物列表
        :param season: 季节
        :param style: 风格
        :return: 筛选后的衣物列表
        """
        result = clothes_list
        
        # 按季节筛选
        if season:
            result = [c for c in result if c.season and season in c.season_list]
        
        # 按风格筛选
        if style:
            result = [c for c in result if c.style and style.lower() in c.style.lower()]
        
        return result
    
    def _format_clothes_data(self, clothes_list):
        """
        格式化衣物数据
        :param clothes_list: 衣物列表
        :return: 格式化后的衣物数据列表
        """
        result = []
        for clothes in clothes_list:
            result.append({
                "id": clothes.id,
                "name": clothes.name or f"{clothes.color or ''} {clothes.category or ''}".strip(),
                "category": clothes.category,
                "color": clothes.color,
                "season": clothes.season_list if clothes.season else [],
                "style": clothes.style
            })
        return result
    
    def _build_prompts(self, clothes_data, occasion=None, season=None, 
                     style_preference=None, weather=None, temperature=None):
        """
        构建提示词
        :param clothes_data: 格式化后的衣物数据
        :param occasion: 场合
        :param season: 季节
        :param style_preference: 风格偏好
        :param weather: 天气
        :param temperature: 温度
        :return: 系统提示词和用户提示词
        """
        system_prompt = """你是一个专业的穿搭顾问AI，擅长根据用户的衣物和需求提供合适的穿搭建议。
你需要从用户提供的衣物中选择合适的组合，确保搭配美观且符合场合要求。
你的回答必须是JSON格式，包含名称、选择的衣物ID列表、推荐理由等信息。"""
        
        # 构建用户提示词
        user_prompt = "请根据以下条件，从我的衣橱中选择合适的衣物组合成一套穿搭：\n\n"
        
        # 添加条件信息
        if occasion:
            user_prompt += f"场合：{occasion}\n"
        if season:
            user_prompt += f"季节：{season}\n"
        if style_preference:
            user_prompt += f"风格偏好：{style_preference}\n"
        if weather:
            user_prompt += f"天气：{weather}\n"
        if temperature is not None:
            user_prompt += f"温度：{temperature}℃\n"
        
        user_prompt += "\n我的衣橱中可用的衣物：\n"
        
        # 添加衣物信息
        for i, clothes in enumerate(clothes_data):
            category_text = f"类别：{clothes['category']}" if clothes['category'] else ""
            color_text = f"颜色：{clothes['color']}" if clothes['color'] else ""
            season_text = f"适合季节：{','.join(clothes['season'])}" if clothes['season'] else ""
            style_text = f"风格：{clothes['style']}" if clothes['style'] else ""
            
            details = [d for d in [category_text, color_text, season_text, style_text] if d]
            detail_text = "（" + "，".join(details) + "）" if details else ""
            
            user_prompt += f"{i+1}. ID: {clothes['id']} - {clothes['name']} {detail_text}\n"
        
        user_prompt += "\n请以JSON格式返回结果，包含以下字段：\n"
        user_prompt += "1. name: 穿搭名称\n"
        user_prompt += "2. clothes_ids: 选择的衣物ID数组\n"
        user_prompt += "3. style: 穿搭风格\n"
        user_prompt += "4. season: 适合季节\n"
        user_prompt += "5. occasion: 适合场合\n"
        user_prompt += "6. reasoning: 推荐理由\n\n"
        user_prompt += "请确保选择的衣物组合合理，至少包含上衣和下装。只返回JSON数据，不要有其他说明文字。"
        
        return system_prompt, user_prompt
    
    def _call_openai_api(self, system_prompt, user_prompt):
        """
        调用OpenAI API
        :param system_prompt: 系统提示词
        :param user_prompt: 用户提示词
        :return: 响应结果
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=2048,
                response_format={"type": "json_object"},
                temperature=0.7,
                top_p=1.0
            )
            
            # 解析响应内容
            content = response.choices[0].message.content
            try:
                data = json.loads(content)
                return {"success": True, "data": data}
            except json.JSONDecodeError:
                return {"success": False, "message": "API返回的结果不是有效的JSON格式"}
            
        except Exception as e:
            return {"success": False, "message": f"调用OpenAI API失败: {str(e)}"}
    
    def _parse_response(self, response_data):
        """
        解析OpenAI的响应结果
        :param response_data: 响应数据
        :return: 解析后的结果
        """
        try:
            # 验证必要字段
            if 'name' not in response_data:
                return {"success": False, "message": "响应缺少穿搭名称"}
            
            if 'clothes_ids' not in response_data or not response_data['clothes_ids']:
                return {"success": False, "message": "响应缺少衣物ID列表"}
            
            # 将字符串数字ID转换为整数
            clothes_ids = []
            for item_id in response_data['clothes_ids']:
                try:
                    clothes_ids.append(int(item_id))
                except (ValueError, TypeError):
                    pass
            
            if not clothes_ids:
                return {"success": False, "message": "无法解析衣物ID列表"}
            
            # 更新衣物ID列表
            response_data['clothes_ids'] = clothes_ids
            
            return {"success": True, "data": response_data}
            
        except Exception as e:
            return {"success": False, "message": f"解析响应失败: {str(e)}"}
    
    def _validate_clothes_ids(self, account_id, clothes_ids):
        """
        验证衣物ID是否有效
        :param account_id: 账号ID
        :param clothes_ids: 衣物ID列表
        :return: 有效的衣物ID列表
        """
        if not clothes_ids:
            return []
        
        # 查询用户拥有的衣物
        valid_clothes = Clothes.query.filter(
            Clothes.id.in_(clothes_ids),
            Clothes.account_id == account_id,
            Clothes.status == 'available'
        ).all()
        
        return [clothes.id for clothes in valid_clothes] 