from datetime import datetime
from app import db
from sqlalchemy import UniqueConstraint

class SharedWardrobe(db.Model):
    """衣柜共享模型"""
    __tablename__ = 'shared_wardrobes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='共享ID')
    account_id = db.Column(db.String(64), nullable=False, index=True, comment='拥有者账号')
    shared_with_account_id = db.Column(db.String(64), nullable=False, index=True, comment='被共享账号')
    role = db.Column(db.Enum('read', 'write'), default='read', comment='共享权限')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint('account_id', 'shared_with_account_id', name='uix_shared_wardrobe'),
    )

    def __init__(self, account_id, shared_with_account_id, role='read'):
        self.account_id = account_id
        self.shared_with_account_id = shared_with_account_id
        self.role = role
    
    def update_role(self, role):
        """
        更新共享权限
        :param role: 权限类型
        """
        if role in ['read', 'write']:
            self.role = role
            db.session.commit()
    
    @classmethod
    def get_by_id(cls, shared_id):
        """
        通过ID获取共享记录
        :param shared_id: 共享记录ID
        :return: 共享记录对象或None
        """
        return cls.query.get(shared_id)
    
    @classmethod
    def get_by_accounts(cls, account_id, shared_with_account_id):
        """
        通过账号获取共享记录
        :param account_id: 拥有者账号ID
        :param shared_with_account_id: 被共享账号ID
        :return: 共享记录对象或None
        """
        return cls.query.filter_by(
            account_id=account_id, 
            shared_with_account_id=shared_with_account_id
        ).first()
    
    @classmethod
    def get_shared_by_me(cls, account_id):
        """
        获取我共享给他人的记录
        :param account_id: 拥有者账号ID
        :return: 共享记录列表
        """
        return cls.query.filter_by(account_id=account_id).all()
    
    @classmethod
    def get_shared_with_me(cls, shared_with_account_id):
        """
        获取他人共享给我的记录
        :param shared_with_account_id: 被共享账号ID
        :return: 共享记录列表
        """
        return cls.query.filter_by(shared_with_account_id=shared_with_account_id).all()
    
    @classmethod
    def check_access(cls, owner_account_id, viewer_account_id, required_role='read'):
        """
        检查是否有访问权限
        :param owner_account_id: 拥有者账号ID
        :param viewer_account_id: 查看者账号ID
        :param required_role: 所需权限
        :return: 布尔值，表示是否有权限
        """
        # 自己总是有权限访问自己的衣柜
        if owner_account_id == viewer_account_id:
            return True
        
        shared = cls.get_by_accounts(owner_account_id, viewer_account_id)
        if not shared:
            return False
        
        # 如果需要写权限，则检查是否有写权限
        if required_role == 'write':
            return shared.role == 'write'
        
        # 否则只需要读权限，任何权限都可以
        return True
    
    def to_dict(self):
        """
        将共享记录对象转换为字典
        :return: 共享记录信息字典
        """
        return {
            'id': self.id,
            'account_id': self.account_id,
            'shared_with_account_id': self.shared_with_account_id,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        } 