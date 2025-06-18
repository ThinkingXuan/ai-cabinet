"""
阿里云OSS工具类
"""
import os
import uuid
from datetime import datetime
import alibabacloud_oss_v2 as oss
from config import Config

# 从配置中导入OSS相关配置
OSS_ACCESS_KEY_ID = Config.OSS_ACCESS_KEY_ID
OSS_ACCESS_KEY_SECRET = Config.OSS_ACCESS_KEY_SECRET
OSS_REGION = Config.OSS_REGION
OSS_BUCKET_NAME = Config.OSS_BUCKET_NAME
OSS_ENDPOINT = Config.OSS_ENDPOINT
ALLOWED_EXTENSIONS = Config.ALLOWED_EXTENSIONS
OSS_URL_EXPIRATION = Config.OSS_URL_EXPIRATION
OSS_PUBLIC_URL_BASE = Config.OSS_PUBLIC_URL_BASE


class OSSHelper:
    """阿里云OSS工具类"""

    def __init__(self):
        """初始化OSS客户端"""
        # 创建凭证提供者
        credentials_provider = oss.credentials.StaticCredentialsProvider(
            OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET
        )
        
        # 使用SDK的默认配置
        cfg = oss.config.load_default()
        cfg.credentials_provider = credentials_provider
        cfg.region = OSS_REGION
        cfg.endpoint = OSS_ENDPOINT
        
        # 创建OSS客户端
        self.client = oss.Client(cfg)
        self.bucket_name = OSS_BUCKET_NAME

    def allowed_file(self, filename):
        """
        检查文件扩展名是否允许上传
        :param filename: 文件名
        :return: 布尔值
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def generate_object_key(self, account_id, filename, file_type='clothes'):
        """
        生成OSS对象键名
        :param account_id: 用户账号ID
        :param filename: 原始文件名
        :param file_type: 文件类型，默认为clothes，可选avatar
        :return: 对象键名
        """
        # 获取文件扩展名
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        # 生成唯一文件名：文件类型/用户ID/年月日/随机UUID.扩展名
        today = datetime.now().strftime('%Y%m%d')
        unique_id = str(uuid.uuid4()).replace('-', '')
        
        return f"{file_type}/{account_id}/{today}/{unique_id}.{ext}"

    def upload_file(self, account_id, file_storage, file_type='clothes'):
        """
        上传文件到OSS
        :param account_id: 用户账号ID
        :param file_storage: Flask FileStorage对象
        :param file_type: 文件类型，默认为clothes，可选avatar
        :return: 成功返回对象键名，失败返回None
        """
        if not file_storage or not self.allowed_file(file_storage.filename):
            return None
        
        try:
            # 生成对象键名
            object_key = self.generate_object_key(account_id, file_storage.filename, file_type)
            
            # 上传文件
            result = self.client.put_object(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=object_key,
                body=file_storage.stream,
            ))
            
            if result and result.etag:
                return object_key
            
            return None
        except Exception as e:
            print(f"上传文件到OSS失败: {str(e)}")
            return None

    def get_signed_url(self, object_key, expires=OSS_URL_EXPIRATION):
        """
        获取对象的签名URL
        :param object_key: 对象键名
        :param expires: 过期时间（秒）
        :return: 签名URL
        """
        try:
            # 生成签名URL
            request = oss.GetObjectRequest(bucket=self.bucket_name, key=object_key)
            presigned_url = self.client.generate_presigned_url(request, expires_in=expires)
            return presigned_url
        except Exception as e:
            print(f"获取签名URL失败: {str(e)}")
            return None

    def get_public_url(self, object_key):
        """
        获取对象的公共URL
        :param object_key: 对象键名
        :return: 公共URL
        """
        return f"{OSS_PUBLIC_URL_BASE}/{object_key}"

    def delete_object(self, object_key):
        """
        删除OSS对象
        :param object_key: 对象键名
        :return: 布尔值，表示是否删除成功
        """
        try:
            self.client.delete_object(oss.DeleteObjectRequest(
                bucket=self.bucket_name,
                key=object_key
            ))
            return True
        except Exception as e:
            print(f"删除OSS对象失败: {str(e)}")
            return False 