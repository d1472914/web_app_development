"""
認證路由（Auth Routes）

負責處理使用者註冊、登入與登出功能。
URL 前綴：/auth

路由清單：
- GET  /auth/login    — 顯示登入頁面
- POST /auth/login    — 處理登入驗證
- GET  /auth/register — 顯示註冊頁面
- POST /auth/register — 處理帳號註冊
- GET  /auth/logout   — 登出並清除 Session
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """登入頁面與登入處理

    GET:  渲染登入表單（auth/login.html）
    POST: 驗證帳號密碼
          - 成功 → 建立 Session，重導向 /tasks
          - 失敗 → 重新渲染登入頁，顯示錯誤訊息

    使用的 Model 方法：
        - User.get_by_username(username)
        - user.check_password(password)

    使用的 Flask-Login 方法：
        - login_user(user)
    """
    pass


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """註冊頁面與註冊處理

    GET:  渲染註冊表單（auth/register.html）
    POST: 驗證表單資料並建立新帳號
          - 成功 → 重導向 /auth/login，顯示成功訊息
          - 失敗 → 重新渲染註冊頁，顯示錯誤訊息

    表單欄位：
        - username（使用者名稱，必填，唯一）
        - email（電子信箱，必填，唯一）
        - password（密碼，必填）
        - confirm_password（確認密碼，必填，需與 password 一致）

    使用的 Model 方法：
        - User.get_by_username(username) — 檢查重複
        - User.get_by_email(email) — 檢查重複
        - User.create(username, email, password)
    """
    pass


@auth_bp.route('/logout')
@login_required
def logout():
    """登出

    清除使用者 Session，重導向至登入頁面。

    使用的 Flask-Login 方法：
        - logout_user()
    """
    pass
