# EnRecall 字典任務包（從這裡開始）

你是字典編輯。這包是台灣高中生背單字 App「EnRecall」的英文字典（學測 7000 字範圍，共 5,938 字），
要逐字**檢查錯誤、補齊內容、整理相似字（形近／義近）**。

## 先做這些

1. 解壓後，依序讀：
   1. `docs/cloud-dict-task.md`：任務規範（最重要，每條都要遵守）
   2. `docs/codex-dict-prompt.md`：欄位格式與書寫風格 1–37 條（和任務規範衝突時，以任務規範為準）
   3. `docs/similar-format.md`：相似字對格式
   4. `docs/cloud-dict-example.json`：一批完整範例
2. 執行 `python scripts/dict_batch.py status` 看進度（只需要 Python 3 標準函式庫）。
3. 從 Level 3 開始，每批 20 字：`show` → 判斷、修改 → 寫 JSON → `apply --dry-run` → `apply`。

## 成果怎麼交回

- 這包沒有 git。**每做完 100 字（5 批）就執行 `python scripts/dict_batch.py pack`**，
  產生 `out/dict-result-<時間>.zip`，提供給使用者下載。對話中斷時最多只損失 100 字。
- 每次打包的 ZIP 都包含**到目前為止的全部成果**，使用者只要保留最新一份。
- 如果使用者之後在新的對話上傳最新的 dict-result ZIP，把它解壓覆蓋到這包的根目錄，就能接著做。

## 資料夾

| 路徑 | 內容 |
|---|---|
| `packs/dict/level1–6.json` | 字典本體（要修改的對象，只能透過 apply 寫入） |
| `packs/dict/similar-candidates.json` | 演算法算好的相似字候選（只讀，show 會自動帶出） |
| `packs/dict/similar/` | 你寫的相似字對（apply 自動產生） |
| `packs/dict/review/` | 進度（apply 自動產生） |
| `scripts/dict_batch.py` | 批次工具：status／show／apply／check／pack |
