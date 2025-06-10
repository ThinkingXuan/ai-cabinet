from app import db
from app.models.user import User

class UserService:
    @staticmethod
    def create_user(username, password, email=None, gender=None, birthdate=None):
        """
        创建新用户
        :param username: 用户名
        :param password: 密码
        :param email: 邮箱（可选）
        :param gender: 性别（可选）
        :param birthdate: 出生日期（可选）
        :return: 用户对象
        """
        user = User(
            username=username, 
            password=password, 
            email=email,
            gender=gender,
            birthdate=birthdate
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_user_by_username(username):
        """
        通过用户名获取用户
        :param username: 用户名
        :return: 用户对象或None
        """
        return User.get_by_username(username)

    @staticmethod
    def get_user_by_email(email):
        """
        通过邮箱获取用户
        :param email: 邮箱
        :return: 用户对象或None
        """
        if not email:
            return None
        return User.get_by_email(email)

    @staticmethod
    def get_user_by_id(user_id):
        """
        通过用户ID获取用户
        :param user_id: 用户ID
        :return: 用户对象或None
        """
        return User.get_by_id(user_id)

    @staticmethod
    def get_user_by_account_id(account_id):
        """
        通过account_id获取用户
        :param account_id: 全局唯一的账户ID
        :return: 用户对象或None
        """
        return User.get_by_account_id(account_id)

    @staticmethod
    def authenticate_user(username, password):
        """
        验证用户
        :param username: 用户名
        :param password: 密码
        :return: 用户对象或None
        """
        user = UserService.get_user_by_username(username)
        if user and user.check_password(password):
            return user
        return None
    
    @staticmethod
    def update_user_profile(user, gender=None, birthdate=None):
        """
        更新用户资料
        :param user: 用户对象
        :param gender: 性别
        :param birthdate: 出生日期
        :return: 更新后的用户对象
        """
        user.update_profile(gender=gender, birthdate=birthdate)
        return user 