/* ============================================
   任務管理系統 — 前端互動邏輯
   ============================================ */

/**
 * 切換分類列表的「檢視模式」與「編輯模式」
 * @param {number} categoryId - 分類 ID
 */
function toggleEditMode(categoryId) {
    const viewMode = document.getElementById('view-mode-' + categoryId);
    const editMode = document.getElementById('edit-mode-' + categoryId);
    
    if (viewMode.classList.contains('d-none')) {
        // 切換回預設顯示
        viewMode.classList.remove('d-none');
        editMode.classList.add('d-none');
        viewMode.classList.add('d-flex');
        editMode.classList.remove('d-flex');
    } else {
        // 切換成編輯狀態
        viewMode.classList.add('d-none');
        editMode.classList.remove('d-none');
        viewMode.classList.remove('d-flex');
        editMode.classList.add('d-flex');
    }
}
