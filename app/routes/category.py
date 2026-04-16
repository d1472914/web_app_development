"""
分類路由（Category Routes）

負責處理任務分類的 CRUD 功能。
URL 前綴：/categories

路由清單：
- GET  /categories              — 分類列表
- POST /categories/create       — 新增分類
- POST /categories/<id>/edit    — 編輯分類
- POST /categories/<id>/delete  — 刪除分類
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models.category import Category

category_bp = Blueprint('category', __name__)


@category_bp.route('/categories')
@login_required
def category_list():
    """分類列表頁面

    顯示目前使用者的所有分類，並顯示每個分類下的任務數量。

    使用的 Model 方法：
        - Category.get_by_user(user_id) — 取得使用者的所有分類

    渲染模板：category/list.html
    傳入變數：categories
    """
    categories = Category.get_by_user(current_user.id)
    return render_template('category/list.html', categories=categories)


@category_bp.route('/categories/create', methods=['POST'])
@login_required
def category_create():
    """新增分類

    表單欄位：
        - name（分類名稱，必填）

    使用的 Model 方法：
        - Category.create(name, user_id)

    錯誤處理：
        - 分類名稱為空 → 顯示錯誤訊息
        - 分類名稱重複（同一使用者） → 顯示錯誤訊息

    成功 → 重導向 /categories，顯示成功訊息
    """
    name = request.form.get('name', '').strip()
    if not name:
        flash('分類名稱不可為空。', 'danger')
        return redirect(url_for('category.category_list'))
    
    # 檢查是否重複
    existing = next((c for c in Category.get_by_user(current_user.id) if c.name == name), None)
    if existing:
        flash(f'分類「{name}」已存在。', 'danger')
        return redirect(url_for('category.category_list'))
        
    Category.create(name=name, user_id=current_user.id)
    flash(f'分類「{name}」建立成功！', 'success')
    return redirect(url_for('category.category_list'))


@category_bp.route('/categories/<int:id>/edit', methods=['POST'])
@login_required
def category_edit(id):
    """編輯分類

    URL 參數：
        - id: 分類 ID

    表單欄位：
        - name（新的分類名稱，必填）

    使用的 Model 方法：
        - Category.get_by_id(id) — 取得分類
        - category.update(name=...) — 更新名稱

    錯誤處理：
        - 分類不存在 → 404
        - 分類不屬於 current_user → 403
        - 新名稱重複 → 顯示錯誤訊息

    成功 → 重導向 /categories，顯示成功訊息
    """
    category = Category.get_by_id(id)
    if not category:
        flash('找不到該分類。', 'danger')
        return redirect(url_for('category.category_list'))
        
    if category.user_id != current_user.id:
        flash('您沒有權限編輯此分類。', 'danger')
        return redirect(url_for('category.category_list'))
        
    name = request.form.get('name', '').strip()
    if not name:
        flash('分類名稱不可為空。', 'danger')
        return redirect(url_for('category.category_list'))
        
    existing = next((c for c in Category.get_by_user(current_user.id) if c.name == name and c.id != id), None)
    if existing:
        flash(f'分類「{name}」已存在。', 'danger')
        return redirect(url_for('category.category_list'))
        
    category.update(name=name)
    flash('分類更新成功！', 'success')
    return redirect(url_for('category.category_list'))


@category_bp.route('/categories/<int:id>/delete', methods=['POST'])
@login_required
def category_delete(id):
    """刪除分類

    刪除分類後，該分類下的任務 category_id 會被自動設為 NULL。

    URL 參數：
        - id: 分類 ID

    使用的 Model 方法：
        - Category.get_by_id(id) — 取得分類
        - category.delete() — 刪除分類

    錯誤處理：
        - 分類不存在 → 404
        - 分類不屬於 current_user → 403

    成功 → 重導向 /categories，顯示成功訊息
    """
    category = Category.get_by_id(id)
    if not category:
        flash('找不到該分類。', 'danger')
    elif category.user_id != current_user.id:
        flash('您沒有權限刪除此分類。', 'danger')
    else:
        name = category.name
        category.delete()
        flash(f'分類「{name}」已刪除。', 'success')
        
    return redirect(url_for('category.category_list'))
