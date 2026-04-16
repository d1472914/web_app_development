"""
Task Model — 任務資料表

負責：
- 儲存任務資料（標題、描述、狀態、優先順序、到期日等）
- 提供 CRUD 與篩選查詢方法
- 自動追蹤建立時間與更新時間
"""

from datetime import datetime, date
from . import db


class Task(db.Model):
    """任務模型"""

    __tablename__ = 'tasks'

    # ---- 欄位定義 ----
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_completed = db.Column(db.Boolean, nullable=False, default=False)
    priority = db.Column(db.String(10), nullable=False, default='medium')
    due_date = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id',
                            ondelete='SET NULL'), nullable=True, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    # ---- 關聯定義 ----
    # backref 'owner' 定義在 User Model
    # backref 'category' 定義在 Category Model

    # ---- 屬性方法 ----
    @property
    def is_overdue(self):
        """判斷任務是否已逾期"""
        if self.due_date and not self.is_completed:
            return self.due_date < date.today()
        return False

    @property
    def is_due_soon(self):
        """判斷任務是否即將到期（3 天內）"""
        if self.due_date and not self.is_completed:
            days_left = (self.due_date - date.today()).days
            return 0 <= days_left <= 3
        return False

    # ---- CRUD 方法 ----
    @staticmethod
    def create(title, user_id, description=None, priority='medium',
               due_date=None, category_id=None):
        """建立新任務

        Args:
            title: 任務標題（必填）
            user_id: 所屬使用者 ID（必填）
            description: 任務描述
            priority: 優先順序（high / medium / low）
            due_date: 到期日
            category_id: 所屬分類 ID

        Returns:
            Task: 新建立的任務物件
        """
        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            user_id=user_id,
            category_id=category_id
        )
        db.session.add(task)
        db.session.commit()
        return task

    @staticmethod
    def get_all():
        """取得所有任務"""
        return Task.query.all()

    @staticmethod
    def get_by_id(task_id):
        """依 ID 取得任務"""
        return Task.query.get(task_id)

    @staticmethod
    def get_by_user(user_id):
        """取得指定使用者的所有任務（依建立時間倒序）"""
        return Task.query.filter_by(user_id=user_id)\
                         .order_by(Task.created_at.desc()).all()

    @staticmethod
    def search(user_id, keyword=None, category_id=None,
               priority=None, status=None):
        """依條件搜尋與篩選任務

        Args:
            user_id: 使用者 ID（必填）
            keyword: 搜尋關鍵字（搜尋標題與描述）
            category_id: 分類 ID
            priority: 優先順序篩選
            status: 完成狀態（'completed' / 'pending'）

        Returns:
            list[Task]: 符合條件的任務列表
        """
        query = Task.query.filter_by(user_id=user_id)

        if keyword:
            query = query.filter(
                db.or_(
                    Task.title.ilike(f'%{keyword}%'),
                    Task.description.ilike(f'%{keyword}%')
                )
            )

        if category_id:
            query = query.filter_by(category_id=category_id)

        if priority:
            query = query.filter_by(priority=priority)

        if status == 'completed':
            query = query.filter_by(is_completed=True)
        elif status == 'pending':
            query = query.filter_by(is_completed=False)

        return query.order_by(Task.created_at.desc()).all()

    def update(self, **kwargs):
        """更新任務資料

        Args:
            **kwargs: 要更新的欄位（如 title, description, priority 等）
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def toggle_completed(self):
        """切換完成狀態"""
        self.is_completed = not self.is_completed
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def delete(self):
        """刪除任務"""
        db.session.delete(self)
        db.session.commit()

    # ---- 魔術方法 ----
    def __repr__(self):
        return f'<Task {self.title}>'
