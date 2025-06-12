"""
AI视觉服务类，用于调用OpenAI API识别服装图片
"""
import json
import time
import requests
from openai import OpenAI
from config import Config

class AIVisionService:
    """AI视觉服务类"""
    
    def __init__(self):
        """初始化OpenAI客户端"""
        self.api_key = Config.OPENAI_API_KEY
        self.model = Config.OPENAI_MODEL
        self.max_retries = Config.OPENAI_MAX_RETRIES
        self.system_prompt = Config.AI_VISION_SYSTEM_PROMPT
        self.user_prompt = Config.AI_VISION_USER_PROMPT
        
        # 初始化OpenAI客户端，不使用proxies参数
        self.client = OpenAI(
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            api_key=self.api_key
        )
        
    def analyze_clothing_image(self, image_url):
        """
        分析服装图片，识别类别、颜色、季节和风格
        :param image_url: 图片URL
        :return: 识别结果字典
        """
        # 重试机制
        for attempt in range(self.max_retries):
            try:
                # 调用OpenAI API
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": [
                            {"type": "text", "text": self.user_prompt},
                            {"type": "image_url", "image_url": {"url": image_url}}
                        ]}
                    ],
                    max_tokens=4096,
                    response_format={"type": "json_object"},
                    temperature=1,
                    top_p=0.7,
                    frequency_penalty=0,
                )
                
                # 解析响应
                if response and response.choices and len(response.choices) > 0:
                    result_text = response.choices[0].message.content
                    print(result_text)
                    try:
                        result = json.loads(result_text)
                        # 验证返回的JSON是否包含所需字段
                        required_fields = ["category", "color", "season", "style", "confidence"]
                        if all(field in result for field in required_fields):
                            return {
                                "success": True,
                                "data": result,
                                "raw_response": result_text
                            }
                        else:
                            missing_fields = [field for field in required_fields if field not in result]
                            return {
                                "success": False,
                                "message": f"返回的JSON缺少必要字段: {', '.join(missing_fields)}",
                                "raw_response": result_text
                            }
                    except json.JSONDecodeError:
                        return {
                            "success": False,
                            "message": "无法解析返回的JSON",
                            "raw_response": result_text
                        }
                
                return {
                    "success": False,
                    "message": "API返回的响应格式不正确",
                    "raw_response": str(response)
                }
                
            except Exception as e:
                # 如果不是最后一次尝试，等待一段时间后重试
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避策略
                else:
                    return {
                        "success": False,
                        "message": f"调用OpenAI API失败: {str(e)}",
                        "raw_response": None
                    }
        
        return {
            "success": False,
            "message": "超过最大重试次数",
            "raw_response": None
        }
    
    def is_valid_image_url(self, url):
        """
        检查URL是否为有效的图片URL
        :param url: 图片URL
        :return: 布尔值
        """
        try:
            response = requests.head(url, timeout=5)
            content_type = response.headers.get('Content-Type', '')
            return response.status_code == 200 and content_type.startswith('image/')
        except Exception:
            return False 