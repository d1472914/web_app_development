"""
任務管理系統 — 應用程式入口點

執行方式：
    python app.py

或使用 Flask CLI：
    flask run
"""

from dotenv import load_dotenv

# 載入 .env 環境變數（需在 import app 之前）
load_dotenv()

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
