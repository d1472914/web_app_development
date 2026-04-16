"""
任務管理系統 — 路由層

使用 Flask Blueprint 模組化路由，將認證、任務、分類三個功能模組分開管理。
"""

from .auth import auth_bp
from .task import task_bp
from .category import category_bp


def register_blueprints(app):
    """註冊所有 Blueprint 到 Flask App

    Args:
        app: Flask 應用程式實例
    """
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(task_bp)
    app.register_blueprint(category_bp)
