from app import db
from app.models.user_body_info import UserBodyInfo
from app.utils.oss_helper import OSSHelper

class UserBodyService:
    @staticmethod
    def get_user_body_info(account_id):
        """
        获取用户身材信息
        :param account_id: 账号ID
        :return: 用户身材信息对象或None
        """
        return UserBodyInfo.get_by_account_id(account_id)
    
    @staticmethod
    def create_or_update_body_info(account_id, avatar_url=None, height=None, weight=None, 
                                  upper_body_length=None, lower_body_length=None, body_shape=None):
        """
        创建或更新用户身材信息
        :param account_id: 账号ID
        :param avatar_url: 用户头像URL
        :param height: 身高(cm)
        :param weight: 体重(kg)
        :param upper_body_length: 上身长度(cm)
        :param lower_body_length: 下身长度(cm)
        :param body_shape: 身材类型
        :return: 用户身材信息对象
        """
        return UserBodyInfo.create_or_update(
            account_id=account_id,
            avatar_url=avatar_url,
            height=height,
            weight=weight,
            upper_body_length=upper_body_length,
            lower_body_length=lower_body_length,
            body_shape=body_shape
        )
    
    @staticmethod
    def update_avatar(account_id, avatar_url):
        """
        更新用户头像URL
        :param account_id: 账号ID
        :param avatar_url: 用户头像URL
        :return: 用户身材信息对象
        """
        body_info = UserBodyInfo.get_by_account_id(account_id)
        
        if body_info:
            body_info.update(avatar_url=avatar_url)
        else:
            body_info = UserBodyInfo(account_id=account_id, avatar_url=avatar_url)
            db.session.add(body_info)
            db.session.commit()
            
        return body_info
    
    @staticmethod
    def upload_avatar(account_id, avatar_file):
        """
        上传用户头像文件
        :param account_id: 账号ID
        :param avatar_file: 头像文件(Flask FileStorage对象)
        :return: 成功返回用户身材信息对象，失败返回None
        """
        if not avatar_file:
            return None
            
        # 创建OSS工具实例
        oss_helper = OSSHelper()
        
        # 上传文件到OSS
        object_key = oss_helper.upload_file(account_id, avatar_file, file_type='avatar')
        
        if not object_key:
            return None
            
        # 生成头像URL
        avatar_url = oss_helper.get_public_url(object_key)
        
        # 更新或创建用户身材信息
        return UserBodyService.update_avatar(account_id, avatar_url)
    
    @staticmethod
    def delete_body_info(account_id):
        """
        删除用户身材信息
        :param account_id: 账号ID
        :return: 布尔值，表示是否删除成功
        """
        body_info = UserBodyInfo.get_by_account_id(account_id)
        
        if body_info:
            db.session.delete(body_info)
            db.session.commit()
            return True
        
        return False 