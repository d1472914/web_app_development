"""
任務表單 — 新增與編輯任務

使用 Flask-WTF 定義表單驗證規則，自動提供 CSRF 防護。
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class TaskForm(FlaskForm):
    """任務新增 / 編輯表單"""
    title = StringField('任務標題', validators=[
        DataRequired(message='請輸入任務標題'),
        Length(max=200, message='標題不可超過 200 個字')
    ])
    description = TextAreaField('任務描述', validators=[
        Optional()
    ])
    priority = SelectField('優先順序', choices=[
        ('low', '低'),
        ('medium', '中'),
        ('high', '高')
    ], default='medium')
    due_date = DateField('到期日', validators=[
        Optional()
    ], format='%Y-%m-%d')
    category_id = SelectField('分類', coerce=int, validators=[
        Optional()
    ])
    submit = SubmitField('儲存')
