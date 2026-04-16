"""
User Model — 使用者資料表

負責：
- 儲存使用者帳號資訊（username、email、密碼雜湊）
- 提供密碼驗證方法
- 整合 Flask-Login，支援登入狀態管理
"""

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class User(UserMixin, db.Model):
    """使用者模型"""

    __tablename__ = 'users'

    # ---- 欄位定義 ----
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # ---- 關聯定義 ----
    # 一對多：一個使用者擁有多筆任務
    tasks = db.relationship('Task', backref='owner', lazy='dynamic',
                            cascade='all, delete-orphan')
    # 一對多：一個使用者擁有多個分類
    categories = db.relationship('Category', backref='owner', lazy='dynamic',
                                 cascade='all, delete-orphan')

    # ---- 密碼處理 ----
    def set_password(self, password):
        """將明文密碼轉為雜湊值後儲存"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """驗證輸入的密碼是否與儲存的雜湊值一致"""
        return check_password_hash(self.password_hash, password)

    # ---- CRUD 方法 ----
    @staticmethod
    def create(username, email, password):
        """建立新使用者

        Args:
            username: 使用者名稱
            email: 電子信箱
            password: 明文密碼（會自動雜湊）

        Returns:
            User: 新建立的使用者物件
        """
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_all():
        """取得所有使用者"""
        return User.query.all()

    @staticmethod
    def get_by_id(user_id):
        """依 ID 取得使用者"""
        return User.query.get(user_id)

    @staticmethod
    def get_by_username(username):
        """依使用者名稱取得使用者"""
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_by_email(email):
        """依電子信箱取得使用者"""
        return User.query.filter_by(email=email).first()

    def update(self, **kwargs):
        """更新使用者資料

        Args:
            **kwargs: 要更新的欄位（如 username, email）
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        """刪除使用者（連同其所有任務與分類）"""
        db.session.delete(self)
        db.session.commit()

    # ---- 魔術方法 ----
    def __repr__(self):
        return f'<User {self.username}>'
