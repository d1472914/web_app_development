"""
任務管理系統 — 應用程式設定

提供不同環境（開發 / 測試 / 正式）的設定類別。
"""

import os

# 專案根目錄路徑
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """基礎設定（共用）"""

    # Flask Secret Key — 用於 Session 加密與 CSRF Token
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-please-change-in-production'

    # SQLAlchemy 設定
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """開發環境設定"""
    DEBUG = True


class TestingConfig(Config):
    """測試環境設定"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'test.db')
    WTF_CSRF_ENABLED = False  # 測試時關閉 CSRF


class ProductionConfig(Config):
    """正式環境設定"""
    DEBUG = False


# 設定對照表
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
