# 相似字資料格式（字典「相似」分頁）

字典單字頁的「片語」分頁拿掉，換成「相似」分頁，分成兩段：

- **形近**：拼字長得像、容易看錯寫錯（affect／effect、desert／dessert、quiet／quite），也包含讀音很像的（accept／except）。
- **義近**：意思相近、中翻英時容易選錯（affect／influence、borrow／lend、refuse／reject／decline）。

## 資料怎麼來

1. `scripts/similarity.py`：離線算候選，輸出 `packs/dict/similar-candidates.json`（**只是候選，App 不讀**）。
   - 形近 = 0.35 Jaro-Winkler + 0.30 三字母片段 Jaccard + 0.25 OSA 編輯距離 + 0.10 字首字尾，另外加拼字規則（ance/ence、able/ible、雙寫字母…）和讀音（音標編輯距離）的分數。
   - 義近 = 0.55 bge-m3 embedding（以字義為單位）+ 0.25 中文字義詞重疊 + 0.1 中文逐字重疊（借入／借出）+ 0.1 現有同義字清單。
   - 同族字（economic／economical、affect／affection）放在 `family`，不佔名額；反義字保留並標 `ant`（borrow／lend 這種反向字組最常搞混）。
2. LLM（雲端 Claude）逐字看候選，判斷哪些真的值得學，寫出區別 → `packs/dict/similar/level1–6.json`（App 讀這個）。

## `similar-candidates.json`

```json
{ "version": 1, "generated": "2026-09-29", "words": {
  "affect": {
    "level": 3,
    "visual":   [ { "w": "effect", "s": 0.769, "sig": { "base": 0.66, "ng": 0.56, "snd": 0.8 } } ],
    "family":   [ { "w": "affection", "s": 0.70, "sig": {} } ],
    "semantic": [ { "w": "influence", "s": 0.81, "cos": 0.78, "zh": ["影響"], "senses": [0, 1] } ]
  } } }
```

- `sig.rule = 1`：符合拼字規則；`sound = 1`：拼字分數沒進榜，靠讀音補進來。
- 義近的 `senses = [i, j]`：兩個字最相近的是第 i 個和第 j 個字義；`zhOnly = 1`：embedding 沒排進前面，但中文字義完全重疊。

## `similar/levelN.json`（App 讀的）

```json
{ "version": 1, "pairs": [
  {
    "a": "affect", "b": "effect",
    "kind": "visual",
    "score": 0.77,
    "aZh": "v. 影響",
    "bZh": "n. 效果；影響",
    "diff": "affect 多半是動詞「去影響」；effect 多半是名詞「造成的結果」。",
    "points": ["詞性：affect 是 v.，effect 是 n.", "搭配：have an effect on ＝ affect"],
    "tip": "Affect = Action（動作），Effect = End result（結果）。",
    "exA": { "en": "The cold weather affected the harvest.", "zh": "寒冷的天氣影響了收成。" },
    "exB": { "en": "The medicine had no effect on him.", "zh": "這個藥對他沒有效果。" }
  } ] }
```

| 欄位 | 說明 |
|---|---|
| `a`、`b` | 兩個字都要在字典裡，小寫，`a` 依字母順序排在 `b` 前面。一組只寫一次，兩個字的頁面都會顯示。 |
| `kind` | `visual` 形近／`semantic` 義近／`both` 兩種都是（rise／raise）。`both` 在兩段都出現。 |
| `score` | 候選分數（照抄候選檔，形近、義近取較高的），App 用來排序。 |
| `aZh`、`bZh` | 跟這組比較有關的那個字義，帶詞性，不必列出全部字義。 |
| `diff` | 一兩句話講核心差別，高中生看得懂。 |
| `points` | 2–4 點：詞性、語氣或正式程度、及物或不及物、常見搭配、拼字或發音的關鍵差別。 |
| `tip` | 記憶法，一句話。 |
| `exA`、`exB` | 各一句高中程度的例句，句子裡要真的有那個字（可以是變化形）。 |

- 同一組如果兩個級別都寫了，App 以 `(a, b)` 去重，保留先讀到的那筆。
- 形近卡片上不同的字母，由 App 當場比對標色，資料不用存。
