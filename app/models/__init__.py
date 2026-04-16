"""
任務管理系統 — Model 層

使用 SQLAlchemy ORM 定義資料表結構，提供資料庫操作方法。
"""

from flask_sqlalchemy import SQLAlchemy

# 建立 SQLAlchemy 實例（在 app/__init__.py 中透過 db.init_app(app) 初始化）
db = SQLAlchemy()

# 匯出所有 Model，方便其他模組使用
from .user import User
from .task import Task
from .category import Category

__all__ = ['db', 'User', 'Task', 'Category']
