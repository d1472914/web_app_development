# 流程圖文件 — 任務管理系統

> **文件版本**：v1.0  
> **建立日期**：2026-04-09  
> **對應文件**：docs/PRD.md、docs/ARCHITECTURE.md

---

## 1. 使用者流程圖（User Flow）

### 1.1 整體操作流程

從使用者進入網站開始，涵蓋認證、任務管理、分類管理等所有主要功能的操作路徑。

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B{是否已登入？}
    
    B -->|否| C[登入頁面]
    C --> D{有帳號嗎？}
    D -->|否| E[註冊頁面]
    E --> F[填寫帳號密碼]
    F --> G{註冊成功？}
    G -->|是| C
    G -->|否| E
    D -->|是| H[輸入帳號密碼]
    H --> I{登入成功？}
    I -->|否| C
    I -->|是| J[任務列表主頁]
    
    B -->|是| J

    J --> K{要執行什麼操作？}
    
    K -->|新增任務| L[填寫任務表單]
    L --> M[儲存任務]
    M --> J

    K -->|檢視任務| N[查看任務詳情]
    N --> J

    K -->|編輯任務| O[編輯任務表單]
    O --> P[更新任務]
    P --> J

    K -->|刪除任務| Q[確認刪除]
    Q --> R[刪除任務]
    R --> J

    K -->|切換完成狀態| S[標記完成/未完成]
    S --> J

    K -->|篩選/搜尋| T[依條件篩選任務]
    T --> J

    K -->|管理分類| U[分類管理頁面]
    U --> J

    K -->|登出| V[登出系統]
    V --> C
```

### 1.2 任務 CRUD 詳細流程

```mermaid
flowchart LR
    subgraph 新增任務
        A1([點擊新增]) --> A2[填寫標題]
        A2 --> A3[填寫描述]
        A3 --> A4[選擇分類]
        A4 --> A5[設定優先順序]
        A5 --> A6[設定到期日]
        A6 --> A7{表單驗證}
        A7 -->|失敗| A2
        A7 -->|成功| A8[儲存至資料庫]
        A8 --> A9([返回任務列表])
    end

    subgraph 編輯任務
        B1([點擊編輯]) --> B2[載入現有資料]
        B2 --> B3[修改欄位]
        B3 --> B4{表單驗證}
        B4 -->|失敗| B3
        B4 -->|成功| B5[更新資料庫]
        B5 --> B6([返回任務列表])
    end

    subgraph 刪除任務
        C1([點擊刪除]) --> C2{確認刪除？}
        C2 -->|取消| C3([返回列表])
        C2 -->|確認| C4[從資料庫刪除]
        C4 --> C5([返回任務列表])
    end
```

### 1.3 認證流程

```mermaid
flowchart LR
    subgraph 註冊流程
        R1([進入註冊頁]) --> R2[輸入使用者名稱]
        R2 --> R3[輸入 Email]
        R3 --> R4[輸入密碼]
        R4 --> R5[確認密碼]
        R5 --> R6{驗證通過？}
        R6 -->|使用者名稱重複| R2
        R6 -->|密碼不一致| R4
        R6 -->|成功| R7[建立帳號]
        R7 --> R8([跳轉登入頁])
    end

    subgraph 登入流程
        L1([進入登入頁]) --> L2[輸入帳號]
        L2 --> L3[輸入密碼]
        L3 --> L4{驗證通過？}
        L4 -->|帳號不存在| L2
        L4 -->|密碼錯誤| L3
        L4 -->|成功| L5[建立 Session]
        L5 --> L6([跳轉任務列表])
    end
```

---

## 2. 系統序列圖（Sequence Diagram）

### 2.1 使用者註冊流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Form as Flask-WTF
    participant Model as User Model
    participant DB as SQLite

    User->>Browser: 點擊「註冊」連結
    Browser->>Flask: GET /auth/register
    Flask-->>Browser: 回傳註冊頁面 HTML

    User->>Browser: 填寫表單並送出
    Browser->>Flask: POST /auth/register
    Flask->>Form: 驗證表單資料
    
    alt 驗證失敗
        Form-->>Flask: 回傳錯誤訊息
        Flask-->>Browser: 重新渲染註冊頁（含錯誤提示）
    else 驗證成功
        Form-->>Flask: 驗證通過
        Flask->>Model: 建立 User 物件（密碼雜湊）
        Model->>DB: INSERT INTO users
        DB-->>Model: 成功
        Model-->>Flask: 回傳新使用者
        Flask-->>Browser: 重導向 /auth/login
        Browser-->>User: 顯示登入頁面（含成功訊息）
    end
```

### 2.2 使用者登入流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Form as Flask-WTF
    participant Model as User Model
    participant DB as SQLite

    User->>Browser: 點擊「登入」
    Browser->>Flask: GET /auth/login
    Flask-->>Browser: 回傳登入頁面 HTML

    User->>Browser: 輸入帳號密碼並送出
    Browser->>Flask: POST /auth/login
    Flask->>Form: 驗證表單資料
    Form-->>Flask: 驗證通過
    Flask->>Model: 查詢使用者帳號
    Model->>DB: SELECT * FROM users WHERE username=?
    DB-->>Model: 回傳使用者資料

    alt 帳號不存在或密碼錯誤
        Model-->>Flask: 驗證失敗
        Flask-->>Browser: 重新渲染登入頁（含錯誤提示）
    else 驗證成功
        Model-->>Flask: 驗證通過
        Flask->>Flask: 建立 Session（login_user）
        Flask-->>Browser: 重導向 /tasks
        Browser-->>User: 顯示任務列表
    end
```

### 2.3 新增任務流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Form as Flask-WTF
    participant Model as Task Model
    participant DB as SQLite

    User->>Browser: 點擊「新增任務」
    Browser->>Flask: GET /tasks/create
    Flask-->>Browser: 回傳新增任務表單 HTML

    User->>Browser: 填寫標題、描述、分類、優先順序、到期日
    User->>Browser: 點擊「儲存」
    Browser->>Flask: POST /tasks/create
    Flask->>Form: 驗證表單資料（標題必填、日期格式等）

    alt 驗證失敗
        Form-->>Flask: 回傳錯誤
        Flask-->>Browser: 重新渲染表單（含錯誤提示）
    else 驗證成功
        Form-->>Flask: 驗證通過
        Flask->>Model: 建立 Task 物件
        Model->>DB: INSERT INTO tasks (title, description, priority, due_date, user_id, category_id)
        DB-->>Model: 成功
        Model-->>Flask: 回傳新任務
        Flask-->>Browser: 重導向 /tasks（含成功訊息）
        Browser-->>User: 顯示更新後的任務列表
    end
```

### 2.4 編輯任務流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Task Model
    participant DB as SQLite

    User->>Browser: 點擊任務的「編輯」按鈕
    Browser->>Flask: GET /tasks/1/edit
    Flask->>Model: 查詢任務資料
    Model->>DB: SELECT * FROM tasks WHERE id=1
    DB-->>Model: 回傳任務資料
    Model-->>Flask: 回傳 Task 物件
    Flask-->>Browser: 回傳已填入資料的編輯表單

    User->>Browser: 修改內容並送出
    Browser->>Flask: POST /tasks/1/edit
    Flask->>Model: 更新 Task 物件
    Model->>DB: UPDATE tasks SET ... WHERE id=1
    DB-->>Model: 成功
    Flask-->>Browser: 重導向 /tasks
    Browser-->>User: 顯示更新後的任務列表
```

### 2.5 刪除任務流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Task Model
    participant DB as SQLite

    User->>Browser: 點擊任務的「刪除」按鈕
    Browser->>Flask: POST /tasks/1/delete
    Flask->>Model: 查詢並刪除任務
    Model->>DB: DELETE FROM tasks WHERE id=1
    DB-->>Model: 成功
    Flask-->>Browser: 重導向 /tasks（含成功訊息）
    Browser-->>User: 顯示更新後的任務列表
```

### 2.6 切換完成狀態流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Task Model
    participant DB as SQLite

    User->>Browser: 點擊任務的「完成」勾選框
    Browser->>Flask: POST /tasks/1/toggle
    Flask->>Model: 切換 is_completed 狀態
    Model->>DB: UPDATE tasks SET is_completed = NOT is_completed WHERE id=1
    DB-->>Model: 成功
    Flask-->>Browser: 重導向 /tasks
    Browser-->>User: 顯示更新後的狀態
```

---

## 3. 功能清單對照表

| 功能 | URL 路徑 | HTTP 方法 | 說明 |
|------|---------|-----------|------|
| 首頁（任務列表） | `/tasks` | GET | 顯示目前使用者的所有任務 |
| 新增任務頁面 | `/tasks/create` | GET | 顯示新增任務表單 |
| 新增任務 | `/tasks/create` | POST | 處理表單送出，建立新任務 |
| 編輯任務頁面 | `/tasks/<id>/edit` | GET | 顯示編輯任務表單（含現有資料） |
| 編輯任務 | `/tasks/<id>/edit` | POST | 處理表單送出，更新任務 |
| 刪除任務 | `/tasks/<id>/delete` | POST | 刪除指定任務 |
| 切換完成狀態 | `/tasks/<id>/toggle` | POST | 切換任務的完成 / 未完成狀態 |
| 搜尋與篩選 | `/tasks?q=&category=&priority=&status=` | GET | 依條件篩選任務列表 |
| 註冊頁面 | `/auth/register` | GET | 顯示註冊表單 |
| 註冊 | `/auth/register` | POST | 處理註冊表單，建立帳號 |
| 登入頁面 | `/auth/login` | GET | 顯示登入表單 |
| 登入 | `/auth/login` | POST | 處理登入驗證 |
| 登出 | `/auth/logout` | GET | 登出並清除 Session |
| 分類列表 | `/categories` | GET | 顯示使用者的所有分類 |
| 新增分類 | `/categories/create` | POST | 建立新分類 |
| 編輯分類 | `/categories/<id>/edit` | POST | 更新分類名稱 |
| 刪除分類 | `/categories/<id>/delete` | POST | 刪除指定分類 |

---

> **下一步**：完成流程圖後，進入資料庫設計（`/db-design`）。
