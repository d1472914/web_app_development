"""
認證表單 — 登入與註冊

使用 Flask-WTF 定義表單驗證規則，自動提供 CSRF 防護。
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    """登入表單"""
    username = StringField('使用者名稱', validators=[
        DataRequired(message='請輸入使用者名稱')
    ])
    password = PasswordField('密碼', validators=[
        DataRequired(message='請輸入密碼')
    ])
    submit = SubmitField('登入')


class RegisterForm(FlaskForm):
    """註冊表單"""
    username = StringField('使用者名稱', validators=[
        DataRequired(message='請輸入使用者名稱'),
        Length(min=2, max=80, message='使用者名稱長度需在 2 到 80 字之間')
    ])
    email = StringField('電子信箱', validators=[
        DataRequired(message='請輸入電子信箱'),
        Email(message='請輸入有效的電子信箱格式')
    ])
    password = PasswordField('密碼', validators=[
        DataRequired(message='請輸入密碼'),
        Length(min=6, message='密碼長度至少 6 個字元')
    ])
    confirm_password = PasswordField('確認密碼', validators=[
        DataRequired(message='請再次輸入密碼'),
        EqualTo('password', message='兩次輸入的密碼不一致')
    ])
    submit = SubmitField('註冊')
