"""
任務路由（Task Routes）

負責處理任務的 CRUD、完成狀態切換、搜尋與篩選功能。
URL 前綴：/tasks

路由清單：
- GET  /tasks              — 任務列表（支援搜尋篩選）
- GET  /tasks/create       — 顯示新增任務表單
- POST /tasks/create       — 建立新任務
- GET  /tasks/<id>/edit    — 顯示編輯任務表單
- POST /tasks/<id>/edit    — 更新任務
- POST /tasks/<id>/delete  — 刪除任務
- POST /tasks/<id>/toggle  — 切換完成狀態
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models.task import Task
from ..models.category import Category
from ..forms.task_forms import TaskForm

task_bp = Blueprint('task', __name__)


@task_bp.route('/tasks')
@login_required
def task_list():
    """任務列表頁面

    顯示目前使用者的所有任務，支援搜尋與篩選。

    URL 查詢參數（均為選填）：
        - q: 搜尋關鍵字（搜尋標題與描述）
        - category: 分類 ID
        - priority: 優先順序（high / medium / low）
        - status: 完成狀態（completed / pending）

    使用的 Model 方法：
        - Task.search(user_id, keyword, category_id, priority, status)
        - Task.get_by_user(user_id)
        - Category.get_by_user(user_id) — 取得分類清單供篩選下拉選單

    渲染模板：task/list.html
    傳入變數：tasks, categories, 目前的篩選條件
    """
    keyword = request.args.get('q')
    category_id = request.args.get('category', type=int)
    priority = request.args.get('priority')
    status = request.args.get('status')
    
    if any([keyword, category_id, priority, status]):
        tasks = Task.search(current_user.id, keyword, category_id, priority, status)
    else:
        tasks = Task.get_by_user(current_user.id)
        
    categories = Category.get_by_user(current_user.id)
    return render_template('task/list.html', tasks=tasks, categories=categories, 
                           filters={'q': keyword, 'category': category_id, 'priority': priority, 'status': status})


@task_bp.route('/tasks/create', methods=['GET', 'POST'])
@login_required
def task_create():
    """新增任務頁面與建立處理

    GET:  渲染新增任務表單（task/create.html）
    POST: 驗證表單並建立新任務
          - 成功 → 重導向 /tasks，顯示成功訊息
          - 失敗 → 重新渲染表單，顯示錯誤訊息

    表單欄位：
        - title（任務標題，必填）
        - description（任務描述，選填）
        - priority（優先順序，預設 medium）
        - due_date（到期日，選填）
        - category_id（分類 ID，選填）

    使用的 Model 方法：
        - Category.get_by_user(user_id) — 取得分類清單供下拉選單
        - Task.create(title, user_id, description, priority, due_date, category_id)

    渲染模板：task/create.html
    傳入變數：categories
    """
    form = TaskForm()
    # 填入分類選項
    categories = Category.get_by_user(current_user.id)
    form.category_id.choices = [(0, '無分類')] + [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        category_val = form.category_id.data if form.category_id.data != 0 else None
        Task.create(
            title=form.title.data,
            user_id=current_user.id,
            description=form.description.data,
            priority=form.priority.data,
            due_date=form.due_date.data,
            category_id=category_val
        )
        flash('任務建立成功！', 'success')
        return redirect(url_for('task.task_list'))
        
    return render_template('task/create.html', form=form, categories=categories)


@task_bp.route('/tasks/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def task_edit(id):
    """編輯任務頁面與更新處理

    GET:  載入任務現有資料，渲染編輯表單（task/edit.html）
    POST: 驗證表單並更新任務
          - 成功 → 重導向 /tasks，顯示成功訊息
          - 失敗 → 重新渲染表單，顯示錯誤訊息

    URL 參數：
        - id: 任務 ID

    使用的 Model 方法：
        - Task.get_by_id(id) — 取得任務
        - Category.get_by_user(user_id) — 取得分類清單供下拉選單
        - task.update(title=..., description=..., priority=..., due_date=..., category_id=...)

    錯誤處理：
        - 任務不存在 → 404
        - 任務不屬於 current_user → 403

    渲染模板：task/edit.html
    傳入變數：task, categories
    """
    task = Task.get_by_id(id)
    if not task:
        flash('找不到該任務。', 'danger')
        return redirect(url_for('task.task_list'))
    if task.user_id != current_user.id:
        flash('您沒有權限編輯此任務。', 'danger')
        return redirect(url_for('task.task_list'))
        
    form = TaskForm(obj=task)
    categories = Category.get_by_user(current_user.id)
    form.category_id.choices = [(0, '無分類')] + [(c.id, c.name) for c in categories]
    
    # 預設選取正確的分類
    if request.method == 'GET':
        form.category_id.data = task.category_id if task.category_id else 0
        
    if form.validate_on_submit():
        category_val = form.category_id.data if form.category_id.data != 0 else None
        task.update(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data,
            due_date=form.due_date.data,
            category_id=category_val
        )
        flash('任務更新成功！', 'success')
        return redirect(url_for('task.task_list'))
        
    return render_template('task/edit.html', form=form, task=task, categories=categories)


@task_bp.route('/tasks/<int:id>/delete', methods=['POST'])
@login_required
def task_delete(id):
    """刪除任務

    URL 參數：
        - id: 任務 ID

    使用的 Model 方法：
        - Task.get_by_id(id) — 取得任務
        - task.delete() — 刪除任務

    錯誤處理：
        - 任務不存在 → 404
        - 任務不屬於 current_user → 403

    成功 → 重導向 /tasks，顯示成功訊息
    """
    task = Task.get_by_id(id)
    if not task:
        flash('找不到該任務。', 'danger')
    elif task.user_id != current_user.id:
        flash('您沒有權限刪除此任務。', 'danger')
    else:
        task.delete()
        flash('任務已刪除。', 'success')
        
    return redirect(url_for('task.task_list'))


@task_bp.route('/tasks/<int:id>/toggle', methods=['POST'])
@login_required
def task_toggle(id):
    """切換任務完成狀態

    URL 參數：
        - id: 任務 ID

    使用的 Model 方法：
        - Task.get_by_id(id) — 取得任務
        - task.toggle_completed() — 切換 is_completed

    錯誤處理：
        - 任務不存在 → 404
        - 任務不屬於 current_user → 403

    成功 → 重導向 /tasks
    """
    task = Task.get_by_id(id)
    if not task:
        flash('找不到該任務。', 'danger')
    elif task.user_id != current_user.id:
        flash('您沒有權限操作此任務。', 'danger')
    else:
        task.toggle_completed()
        
    return redirect(url_for('task.task_list'))
