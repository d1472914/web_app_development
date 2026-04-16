"""
任務管理系統 — Flask App 工廠函式

使用 Application Factory Pattern 建立 Flask 應用程式實例。
負責初始化所有擴充套件、註冊 Blueprint、設定 Flask-Login。
"""

import os
from flask import Flask
from flask_login import LoginManager
from config import config
from .models import db


# Flask-Login 實例
login_manager = LoginManager()
login_manager.login_view = 'auth.login'           # 未登入時重導向的路由
login_manager.login_message = '請先登入才能使用此功能。'  # 未登入時的提示訊息
login_manager.login_message_category = 'warning'


def create_app(config_name=None):
    """建立並設定 Flask 應用程式

    Args:
        config_name: 設定名稱（'development' / 'testing' / 'production'）
                     若未指定，從環境變數 FLASK_ENV 讀取，預設為 'development'

    Returns:
        Flask: 設定完成的 Flask 應用程式實例
    """
    app = Flask(__name__)

    # 載入設定
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config.get(config_name, config['default']))

    # 確保 instance 資料夾存在
    os.makedirs(app.instance_path, exist_ok=True)

    # 初始化擴充套件
    db.init_app(app)
    login_manager.init_app(app)

    # 設定 Flask-Login 的 user_loader
    from .models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        """Flask-Login 回呼函式：根據 user_id 載入使用者物件"""
        return User.get_by_id(int(user_id))

    # 註冊 Blueprint
    from .routes import register_blueprints
    register_blueprints(app)

    # 建立資料庫表格（如果不存在）
    with app.app_context():
        db.create_all()

    return app
