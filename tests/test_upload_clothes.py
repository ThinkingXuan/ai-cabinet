"""
测试衣物图片上传功能
"""
import os
import requests
import json
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 测试配置
BASE_URL = "http://localhost:8080/ai-cabinet"
TEST_IMAGE_PATH = "tests/test_image.jpg"  # 测试图片路径

def login():
    """
    登录获取token
    """
    login_url = f"{BASE_URL}/api/auth/login"
    login_data = {
        "username": "testuser",
        "password": "password123"
    }
    
    response = requests.post(login_url, json=login_data)
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            return data.get("data", {}).get("token")
    
    print("登录失败:", response.text)
    return None

def upload_clothes_image(token):
    """
    上传衣物图片
    """
    upload_url = f"{BASE_URL}/api/clothes/upload"
    
    # 检查测试图片是否存在
    if not os.path.exists(TEST_IMAGE_PATH):
        print(f"测试图片不存在: {TEST_IMAGE_PATH}")
        return
    
    # 准备文件
    files = [
        ('files[]', ('test_image.jpg', open(TEST_IMAGE_PATH, 'rb'), 'image/jpeg'))
    ]
    
    # 准备请求头
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # 发送请求
    response = requests.post(upload_url, files=files, headers=headers)
    
    # 打印结果
    print("状态码:", response.status_code)
    print("响应内容:", json.dumps(response.json(), ensure_ascii=False, indent=2))
    
    # 关闭文件
    for _, (_, file_obj, _) in files:
        file_obj.close()

def main():
    """
    主函数
    """
    # 登录获取token
    token = login()
    if not token:
        print("获取token失败，无法继续测试")
        return
    
    # 上传衣物图片
    upload_clothes_image(token)

if __name__ == "__main__":
    main() 