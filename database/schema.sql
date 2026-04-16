-- ============================================
-- 任務管理系統 — SQLite 資料庫建表語法
-- 建立日期：2026-04-16
-- ============================================

-- 啟用外鍵約束（SQLite 預設關閉）
PRAGMA foreign_keys = ON;

-- --------------------------------------------
-- 1. 使用者資料表
-- --------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    username        VARCHAR(80)  NOT NULL UNIQUE,
    email           VARCHAR(120) NOT NULL UNIQUE,
    password_hash   VARCHAR(256) NOT NULL,
    created_at      DATETIME     NOT NULL DEFAULT (datetime('now'))
);

-- --------------------------------------------
-- 2. 分類資料表
-- --------------------------------------------
CREATE TABLE IF NOT EXISTS categories (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            VARCHAR(50)  NOT NULL,
    user_id         INTEGER      NOT NULL,
    created_at      DATETIME     NOT NULL DEFAULT (datetime('now')),

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE (name, user_id)
);

-- 索引：加速查詢使用者的分類
CREATE INDEX IF NOT EXISTS idx_categories_user_id ON categories(user_id);

-- --------------------------------------------
-- 3. 任務資料表
-- --------------------------------------------
CREATE TABLE IF NOT EXISTS tasks (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    title           VARCHAR(200) NOT NULL,
    description     TEXT,
    is_completed    BOOLEAN      NOT NULL DEFAULT 0,
    priority        VARCHAR(10)  NOT NULL DEFAULT 'medium',
    due_date        DATE,
    user_id         INTEGER      NOT NULL,
    category_id     INTEGER,
    created_at      DATETIME     NOT NULL DEFAULT (datetime('now')),
    updated_at      DATETIME     NOT NULL DEFAULT (datetime('now')),

    FOREIGN KEY (user_id)     REFERENCES users(id)      ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id)  ON DELETE SET NULL
);

-- 索引：加速查詢使用者的任務
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);

-- 複合索引：加速依完成狀態篩選
CREATE INDEX IF NOT EXISTS idx_tasks_user_completed ON tasks(user_id, is_completed);

-- 索引：加速依分類篩選
CREATE INDEX IF NOT EXISTS idx_tasks_category_id ON tasks(category_id);
