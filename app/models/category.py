"""
Category Model — 分類資料表

負責：
- 儲存使用者自訂的任務分類（如：工作、學習、生活）
- 每個分類屬於一個使用者，同一使用者不可建立同名分類
- 刪除分類時，該分類下的任務 category_id 會被設為 NULL
"""

from datetime import datetime
from . import db


class Category(db.Model):
    """分類模型"""

    __tablename__ = 'categories'

    # ---- 欄位定義 ----
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # ---- 唯一約束：同一使用者不可建立同名分類 ----
    __table_args__ = (
        db.UniqueConstraint('name', 'user_id', name='uq_category_name_user'),
    )

    # ---- 關聯定義 ----
    # 一對多：一個分類可包含多筆任務
    tasks = db.relationship('Task', backref='category', lazy='dynamic')

    # ---- CRUD 方法 ----
    @staticmethod
    def create(name, user_id):
        """建立新分類

        Args:
            name: 分類名稱
            user_id: 所屬使用者 ID

        Returns:
            Category: 新建立的分類物件
        """
        category = Category(name=name, user_id=user_id)
        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    def get_all():
        """取得所有分類"""
        return Category.query.all()

    @staticmethod
    def get_by_id(category_id):
        """依 ID 取得分類"""
        return Category.query.get(category_id)

    @staticmethod
    def get_by_user(user_id):
        """取得指定使用者的所有分類（依名稱排序）"""
        return Category.query.filter_by(user_id=user_id)\
                              .order_by(Category.name).all()

    def update(self, **kwargs):
        """更新分類資料

        Args:
            **kwargs: 要更新的欄位（如 name）
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        """刪除分類（該分類下的任務 category_id 會被設為 NULL）"""
        db.session.delete(self)
        db.session.commit()

    # ---- 魔術方法 ----
    def __repr__(self):
        return f'<Category {self.name}>'
