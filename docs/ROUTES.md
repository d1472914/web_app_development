# 路由設計文件 — 任務管理系統

> **文件版本**：v1.0  
> **建立日期**：2026-04-16  
> **對應文件**：docs/PRD.md、docs/ARCHITECTURE.md、docs/DB_DESIGN.md

---

## 1. 路由總覽表格

### 1.1 認證路由（auth）

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|---------|---------|------|
| 登入頁面 | GET | `/auth/login` | `auth/login.html` | 顯示登入表單 |
| 登入 | POST | `/auth/login` | — | 驗證帳密，成功重導向 `/tasks` |
| 註冊頁面 | GET | `/auth/register` | `auth/register.html` | 顯示註冊表單 |
| 註冊 | POST | `/auth/register` | — | 建立帳號，成功重導向 `/auth/login` |
| 登出 | GET | `/auth/logout` | — | 清除 Session，重導向 `/auth/login` |

### 1.2 任務路由（task）

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|---------|---------|------|
| 任務列表 | GET | `/tasks` | `task/list.html` | 顯示使用者所有任務（支援搜尋與篩選） |
| 新增任務頁面 | GET | `/tasks/create` | `task/create.html` | 顯示新增任務表單 |
| 建立任務 | POST | `/tasks/create` | — | 接收表單，存入 DB，重導向 `/tasks` |
| 編輯任務頁面 | GET | `/tasks/<id>/edit` | `task/edit.html` | 顯示編輯表單（含現有資料） |
| 更新任務 | POST | `/tasks/<id>/edit` | — | 接收表單，更新 DB，重導向 `/tasks` |
| 刪除任務 | POST | `/tasks/<id>/delete` | — | 刪除任務，重導向 `/tasks` |
| 切換完成狀態 | POST | `/tasks/<id>/toggle` | — | 切換完成/未完成，重導向 `/tasks` |

### 1.3 分類路由（category）

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|---------|---------|------|
| 分類列表 | GET | `/categories` | `category/list.html` | 顯示使用者所有分類 |
| 新增分類 | POST | `/categories/create` | — | 建立分類，重導向 `/categories` |
| 編輯分類 | POST | `/categories/<id>/edit` | — | 更新分類名稱，重導向 `/categories` |
| 刪除分類 | POST | `/categories/<id>/delete` | — | 刪除分類，重導向 `/categories` |

---

## 2. 路由詳細說明

### 2.1 認證路由

#### GET `/auth/login` — 登入頁面

- **輸入**：無
- **處理邏輯**：渲染登入表單
- **輸出**：`auth/login.html`
- **錯誤處理**：若使用者已登入，重導向 `/tasks`

#### POST `/auth/login` — 登入

- **輸入**：表單欄位 `username`, `password`
- **處理邏輯**：
  1. 使用 Flask-WTF 驗證表單
  2. 呼叫 `User.get_by_username(username)` 查詢使用者
  3. 呼叫 `user.check_password(password)` 驗證密碼
  4. 呼叫 `login_user(user)` 建立 Session
- **輸出**：重導向 `/tasks`
- **錯誤處理**：帳號不存在或密碼錯誤 → 重新渲染登入頁，顯示錯誤訊息

#### GET `/auth/register` — 註冊頁面

- **輸入**：無
- **處理邏輯**：渲染註冊表單
- **輸出**：`auth/register.html`
- **錯誤處理**：若使用者已登入，重導向 `/tasks`

#### POST `/auth/register` — 註冊

- **輸入**：表單欄位 `username`, `email`, `password`, `confirm_password`
- **處理邏輯**：
  1. 使用 Flask-WTF 驗證表單（密碼一致性、欄位格式）
  2. 檢查 username 與 email 是否已被使用
  3. 呼叫 `User.create(username, email, password)` 建立帳號
- **輸出**：重導向 `/auth/login`，顯示註冊成功訊息
- **錯誤處理**：使用者名稱或 email 重複 → 重新渲染註冊頁，顯示錯誤訊息

#### GET `/auth/logout` — 登出

- **輸入**：無
- **處理邏輯**：呼叫 `logout_user()` 清除 Session
- **輸出**：重導向 `/auth/login`
- **錯誤處理**：需要 `@login_required` 保護

---

### 2.2 任務路由

#### GET `/tasks` — 任務列表

- **輸入**：URL 查詢參數 `q`（關鍵字）、`category`（分類 ID）、`priority`（優先順序）、`status`（完成狀態）
- **處理邏輯**：
  1. 取得 `current_user.id`
  2. 若有篩選參數，呼叫 `Task.search(user_id, keyword, category_id, priority, status)`
  3. 若無篩選參數，呼叫 `Task.get_by_user(user_id)`
  4. 呼叫 `Category.get_by_user(user_id)` 取得分類清單（供篩選下拉選單用）
- **輸出**：`task/list.html`，傳入 `tasks`、`categories`、目前的篩選條件
- **錯誤處理**：需要 `@login_required` 保護

#### GET `/tasks/create` — 新增任務頁面

- **輸入**：無
- **處理邏輯**：
  1. 呼叫 `Category.get_by_user(user_id)` 取得分類清單（供下拉選單）
  2. 渲染新增任務表單
- **輸出**：`task/create.html`，傳入 `categories`
- **錯誤處理**：需要 `@login_required` 保護

#### POST `/tasks/create` — 建立任務

- **輸入**：表單欄位 `title`, `description`, `priority`, `due_date`, `category_id`
- **處理邏輯**：
  1. 使用 Flask-WTF 驗證表單（標題必填）
  2. 呼叫 `Task.create(title, user_id, description, priority, due_date, category_id)`
- **輸出**：重導向 `/tasks`，顯示成功訊息
- **錯誤處理**：驗證失敗 → 重新渲染表單，顯示錯誤訊息

#### GET `/tasks/<id>/edit` — 編輯任務頁面

- **輸入**：URL 參數 `id`（任務 ID）
- **處理邏輯**：
  1. 呼叫 `Task.get_by_id(id)` 取得任務
  2. 確認任務屬於 `current_user`
  3. 呼叫 `Category.get_by_user(user_id)` 取得分類清單
  4. 渲染編輯表單，預填現有資料
- **輸出**：`task/edit.html`，傳入 `task`、`categories`
- **錯誤處理**：任務不存在 → 404；非本人任務 → 403

#### POST `/tasks/<id>/edit` — 更新任務

- **輸入**：URL 參數 `id` + 表單欄位 `title`, `description`, `priority`, `due_date`, `category_id`
- **處理邏輯**：
  1. 呼叫 `Task.get_by_id(id)` 取得任務
  2. 確認任務屬於 `current_user`
  3. 呼叫 `task.update(title=..., description=..., ...)` 更新資料
- **輸出**：重導向 `/tasks`，顯示成功訊息
- **錯誤處理**：驗證失敗 → 重新渲染表單；非本人任務 → 403

#### POST `/tasks/<id>/delete` — 刪除任務

- **輸入**：URL 參數 `id`（任務 ID）
- **處理邏輯**：
  1. 呼叫 `Task.get_by_id(id)` 取得任務
  2. 確認任務屬於 `current_user`
  3. 呼叫 `task.delete()` 刪除任務
- **輸出**：重導向 `/tasks`，顯示成功訊息
- **錯誤處理**：任務不存在 → 404；非本人任務 → 403

#### POST `/tasks/<id>/toggle` — 切換完成狀態

- **輸入**：URL 參數 `id`（任務 ID）
- **處理邏輯**：
  1. 呼叫 `Task.get_by_id(id)` 取得任務
  2. 確認任務屬於 `current_user`
  3. 呼叫 `task.toggle_completed()` 切換狀態
- **輸出**：重導向 `/tasks`
- **錯誤處理**：任務不存在 → 404；非本人任務 → 403

---

### 2.3 分類路由

#### GET `/categories` — 分類列表

- **輸入**：無
- **處理邏輯**：
  1. 呼叫 `Category.get_by_user(current_user.id)` 取得分類清單
  2. 對每個分類計算其任務數量
- **輸出**：`category/list.html`，傳入 `categories`
- **錯誤處理**：需要 `@login_required` 保護

#### POST `/categories/create` — 新增分類

- **輸入**：表單欄位 `name`
- **處理邏輯**：
  1. 驗證分類名稱不為空
  2. 呼叫 `Category.create(name, user_id)`
- **輸出**：重導向 `/categories`，顯示成功訊息
- **錯誤處理**：分類名稱重複 → 顯示錯誤訊息

#### POST `/categories/<id>/edit` — 編輯分類

- **輸入**：URL 參數 `id` + 表單欄位 `name`
- **處理邏輯**：
  1. 呼叫 `Category.get_by_id(id)` 取得分類
  2. 確認分類屬於 `current_user`
  3. 呼叫 `category.update(name=...)` 更新名稱
- **輸出**：重導向 `/categories`，顯示成功訊息
- **錯誤處理**：分類不存在 → 404；非本人分類 → 403

#### POST `/categories/<id>/delete` — 刪除分類

- **輸入**：URL 參數 `id`（分類 ID）
- **處理邏輯**：
  1. 呼叫 `Category.get_by_id(id)` 取得分類
  2. 確認分類屬於 `current_user`
  3. 呼叫 `category.delete()` 刪除（其下任務的 `category_id` 會自動設為 NULL）
- **輸出**：重導向 `/categories`，顯示成功訊息
- **錯誤處理**：分類不存在 → 404；非本人分類 → 403

---

## 3. Jinja2 模板清單

所有模板位於 `app/templates/`，皆繼承 `base.html` 基礎模板。

| 模板路徑 | 說明 | 繼承 |
|---------|------|------|
| `base.html` | 基礎模板（HTML head、navbar、footer、flash 訊息） | — |
| `auth/login.html` | 登入頁面（帳號、密碼表單） | `base.html` |
| `auth/register.html` | 註冊頁面（帳號、email、密碼、確認密碼表單） | `base.html` |
| `task/list.html` | 任務列表主頁（含搜尋篩選列、任務卡片/表格） | `base.html` |
| `task/create.html` | 新增任務表單（標題、描述、分類、優先順序、到期日） | `base.html` |
| `task/edit.html` | 編輯任務表單（預填現有資料） | `base.html` |
| `category/list.html` | 分類管理頁面（分類列表、新增/編輯/刪除操作） | `base.html` |

### 模板繼承結構

```
base.html
├── auth/login.html
├── auth/register.html
├── task/list.html
├── task/create.html
├── task/edit.html
└── category/list.html
```

---

## 4. URL 設計原則

1. **使用名詞**：URL 以資源名稱為主（`/tasks`、`/categories`）
2. **Blueprint 前綴**：認證路由使用 `/auth` 前綴
3. **POST 取代 DELETE/PUT**：因 HTML 表單僅支援 GET/POST，刪除與更新皆使用 POST
4. **權限保護**：所有任務與分類路由皆需 `@login_required`
5. **所有權驗證**：操作資料前必須確認該資料屬於 `current_user`

---

> **下一步**：完成路由設計後，進入程式碼實作（`/implementation`）。
