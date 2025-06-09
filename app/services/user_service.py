from app import db
from app.models.user import User

class UserService:
    @staticmethod
    def create_user(username, email, password):
        """
        创建新用户
        :param username: 用户名
        :param email: 邮箱
        :param password: 密码
        :return: 用户对象
        """
        user = User(username=username, email=email, password=password)
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
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_user_by_email(email):
        """
        通过邮箱获取用户
        :param email: 邮箱
        :return: 用户对象或None
        """
        return User.query.filter_by(email=email).first()

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