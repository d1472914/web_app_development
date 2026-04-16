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
    pass


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
    pass


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
    pass


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
    pass


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
    pass
