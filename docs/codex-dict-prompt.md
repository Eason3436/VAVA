# 給 Codex 的提示詞：產生 EnRecall 字典匯入檔

把下面整段（從「你的任務」到最後）貼給 Codex，再附上要處理的字表。

---

## 你的任務

你要替台灣高中生的背單字 App 產生字典資料，輸出成一個 JSON 檔讓 App 匯入。
讀者是準備學測的高中生（程度約 CEFR B1–B2）。內容要正確、精簡、好懂，寧可少寫也不要寫錯。

輸入：一份英文單字清單（每行一個字，可能附詞性或學測級別）。
輸出：一個 UTF-8 JSON 檔，結構如下。只輸出 JSON，不要任何說明文字、不要 Markdown 程式碼框。

```
{ "version": 3, "words": [ 單字物件, ... ] }
```

每個單字依序處理，一字一個物件，順序與輸入相同。遇到拼錯或不存在的字，照原樣保留 `word`，其餘欄位留空陣列或空字串，不要自己改成別的字。

## 單字物件的欄位

```
{
  "word": "原樣照抄輸入的字",
  "phonetic": "/KK 或 IPA 音標/",
  "level": 1–6 的整數（輸入有給才填，沒給就省略這個欄位）,
  "forms": "詞形變化 · 派生詞",
  "meanings": [
    {
      "pos": "詞性",
      "zh": "中文字義",
      "ext": "字義引申",
      "examples": [ { "en": "英文例句", "zh": "中文翻譯" } ],
      "patterns": [ { "pattern": "句型", "en": "英文例句", "zh": "中文翻譯" } ],
      "collocations": [ { "en": "搭配", "zh": "中文" } ]
    }
  ],
  "synonyms": [ { "word": "相似字", "note": "差別", "example": "短搭配" } ],
  "antonyms": [ { "word": "反義字", "zh": "中文" } ],
  "confusables": [ { "words": "A vs B", "note": "差別", "wrong": "錯句", "right": "對句" } ],
  "commonErrors": [ { "wrong": "錯誤用法", "right": "正確用法", "note": "說明", "exWrong": "錯誤例句", "exRight": "正確例句" } ],
  "breakdownApplicable": true 或 false,
  "breakdown": [ { "part": "詞素", "type": "字首｜字根｜字尾｜完整詞", "gloss": "詞素意思" } ],
  "origin": "字源說明",
  "related": [ { "word": "同根字", "note": "中文字義" } ],
  "phrases": [
    {
      "phrase": "片語原形",
      "zh": "中文",
      "example": "英文例句",
      "exampleZh": "中文翻譯",
      "cloze": true 或 false,
      "answer": "片語在例句中一字不差的寫法",
      "distractors": ["錯誤選項1", "錯誤選項2", "錯誤選項3"],
      "whys": ["選項1為什麼錯", "選項2為什麼錯", "選項3為什麼錯"],
      "notes": ["用法說明"]
    }
  ]
}
```

## 書寫風格（最重要，每一條都要遵守）

### 語言
1. 中文一律用**台灣繁體中文**與台灣用語：「影片」不是「視頻」、「資訊」不是「信息」、「品質」不是「質量」、「軟體」不是「軟件」、「網路」不是「網絡」、「計程車」不是「出租車」、「垃圾」不是「垃圾」以外的說法、「捷運」不是「地鐵」。
2. 不可以出現任何簡體字。寫完自己檢查一次。
3. 中文標點用全形：，。、；：「」（）？！。英文句子裡用半形標點。
4. 中文裡不要夾雜英文解釋（例外：提到英文單字、片語或句型本身時直接寫英文，不加引號）。

### 語氣
5. 用平實、像老師上課講解的口吻。不要用「讓我們」「值得注意的是」「總而言之」「非常重要」「小心」這類贅詞與口號。
6. 不要加表情符號、不要加粗體或任何 Markdown 符號、不要加「💡」「⚠️」「重點：」這種標記。
7. 不要自稱、不要對讀者喊話（不要寫「你可以記成…」「同學要注意…」）。直接陳述事實。

### 長度（超過就刪，不要湊）
8. `zh`（字義）：2–10 個字，多個近義用「；」分隔，例「維持；保持」。不要寫成完整句子，不要加「的意思」。
9. `ext`（字義引申）：一句，20–35 字。說明這個意思從字面怎麼來，用「→」串起步驟，例「握住不放 → 讓狀態一直持續」。沒有明確引申關係就留空字串，不要硬掰。
10. `note`、`whys`、`notes` 每一項：一句，15–40 字，句尾加句號（`notes` 若是公式如「= keep in touch with」可不加）。
11. `origin`：一到兩句，40–80 字。只寫可查證的字源（拉丁文、希臘文、古法語、古英語等），寫出原文拼法與意思。不確定就留空字串。
12. 英文例句：8–18 個字，一句話，不要用分號串兩句。

### 例句內容
13. 例句要是高中生生活或學測常見題材：學校、家庭、社團、考試、旅行、環保、科技、健康、新聞。不要用恐怖、暴力、政治爭議、成人內容。
14. 例句只用學測 7000 字範圍內的字（目標字除外），不要用罕見字、俚語、縮寫（gonna、wanna）。
15. 人名用常見英文名（Amy、Tom、Jenny、Kevin）或 my brother、our teacher 這類稱呼，不要用真實名人。
16. 每個例句只示範一個字義，目標字在句中要明顯、自然。
17. 中文翻譯要通順的台灣口語，不要逐字硬翻（不要出現「被…所…」「對…進行…」這種翻譯腔）。

### 正確性（不確定就不要寫）
18. **禁止編造**。不確定的字源、同根字、片語、搭配，一律留空陣列或空字串。空的欄位 App 會提示「補齊這個字」，寫錯比沒寫更糟。
19. `related`（同根字）必須是真實存在、而且真的同源的英文字，2–4 個，優先選學測範圍內的字。只是拼法像但不同源的不算（例：pineapple 不是 apple 的同根字）。
20. `breakdown` 只拆有公認字源的字。單音節字、外來字、拆了沒幫助的字，`breakdownApplicable` 設 false、`breakdown` 給空陣列。`type` 只能用「字首」「字根」「字尾」「完整詞」四個詞之一；`part` 字首寫成 `re-`、字尾寫成 `-tion`、字根寫成 `-tain-` 或 `tain`；`gloss` 用中文 2–6 字。
21. 音標用一種就好，全檔一致（建議 IPA，例 /meɪnˈteɪn/）。不確定就留空。

### 各欄位的份量
22. `meanings`：只列學測會考的常用字義，1–4 個，依常用程度排序。不要把罕用義、古義、專業術語義放進來。
23. `examples`：每個字義 1–2 句。
24. `patterns`：只寫真的有句型特徵的（接 to V、V-ing、that 子句、介系詞、受詞位置），pattern 用這種寫法：「maintain + N」「maintain that + 子句」「be used to + V-ing」「insist on + N / V-ing」。每個字義 0–3 個，沒有特別句型就給空陣列。
25. `collocations`：每個字義 0–5 個，只列高頻、學測常見的搭配，不要列單純的形容詞＋名詞隨意組合。
26. `synonyms`：2–4 個，第一個放目標字本身，`note` 說清楚每個字跟其他字的差別（語氣、正式度、接什麼、用在什麼情境），不要只寫「意思相近」。
27. `antonyms`：0–3 個，只列真正的反義字。
28. `confusables`：0–2 組，只列學生真的會搞混的（形近如 affect/effect、義近如 remain/maintain、用法近如 rise/raise）。`wrong` 是學生常寫錯的完整句子，`right` 是改正後的句子，兩句要只差在那個關鍵處。
29. `commonErrors`：0–2 個，寫台灣學生真的常犯的錯（中式英文、介系詞、及物與不及物、可數與不可數）。
30. `forms`：列三態、第三人稱、常見派生詞，用「 · 」（前後各一個半形空格）分隔，例「maintained · maintaining · maintenance」。沒有變化的字留空字串。

### 片語（克漏字題）
31. 只列含這個字、學測常見的片語，0–4 個。`cloze` 只有學測克漏字或指考常考的才設 true。
32. `example` 要能讓人從上下文判斷出答案，不能換成別的選項也說得通。
33. `answer` 必須和 `example` 裡的寫法一字不差（含時態、人稱、大小寫），例：例句是 She finally gave up smoking.，answer 就是 gave up。
34. `distractors` 3 個，必須是真實存在的片語，而且寫法與 answer 同型（同時態、同人稱），例 answer 是 gave up，選項就是 gave in、gave out、gave away。放進句子一定要錯。
35. `whys` 與 `distractors` 一一對應，每句先說這個片語的意思，再說為什麼不合句子，例「give in 是「屈服、讓步」，沒有戒除的意思。」
36. `notes` 1–2 點：後面接什麼、代名詞放哪裡、常見同義說法。

### 詞性寫法
37. 詞性只能用：`n.`、`v.`、`adj.`、`adv.`、`prep.`、`conj.`、`pron.`、`int.`、`aux.`。及物與不及物都寫 `v.`，不要寫 vt. / vi.。

## 最後自我檢查（輸出前逐項確認）
- JSON 能被標準解析器解析：雙引號、沒有多餘逗號、沒有註解。
- 沒有簡體字、沒有大陸用語、沒有 Markdown 符號與表情符號。
- 每個 `answer` 都能在對應的 `example` 裡找到一字不差的原文。
- 每個 `distractors` 都剛好 3 個，`whys` 也剛好 3 句且順序對應。
- 不確定的內容都已經刪掉或留空，沒有為了填滿欄位而編造。

## 範例（照這個品質與長度寫）

```
{"version":3,"words":[{"word":"maintain","phonetic":"/meɪnˈteɪn/","level":4,"forms":"maintained · maintaining · maintenance","meanings":[{"pos":"v.","zh":"維持；保持","ext":"用手握住不放 → 讓狀態一直持續下去","examples":[{"en":"It is hard to maintain focus for two hours.","zh":"要連續專心兩個小時很難。"}],"patterns":[{"pattern":"maintain + N","en":"She exercises every day to maintain a healthy weight.","zh":"她每天運動來維持健康的體重。"}],"collocations":[{"en":"maintain order","zh":"維持秩序"},{"en":"maintain a balance","zh":"保持平衡"}]},{"pos":"v.","zh":"堅稱；主張","ext":"把一個說法抓住不放 → 一直堅持這麼說","examples":[{"en":"He maintains that he did not take the money.","zh":"他堅稱自己沒有拿那筆錢。"}],"patterns":[{"pattern":"maintain that + 子句","en":"Tom maintains that the test was unfair.","zh":"Tom 堅稱那次考試不公平。"}],"collocations":[]}],"synonyms":[{"word":"maintain","note":"讓狀態或水準持續不變，語氣較正式。","example":"maintain quality"},{"word":"keep","note":"最口語的保持，後面可以直接接形容詞。","example":"keep calm"},{"word":"preserve","note":"保護東西不受損壞，讓它保存下來。","example":"preserve old buildings"}],"antonyms":[{"word":"neglect","zh":"疏於照顧"}],"confusables":[{"words":"remain vs maintain","note":"remain 不接受詞，後面接形容詞；maintain 一定要有受詞。","wrong":"The price maintained high.","right":"The price remained high."}],"commonErrors":[{"wrong":"maintain to V","right":"maintain + N / that 子句","note":"maintain 後面不接不定詞。","exWrong":"He maintained to be innocent.","exRight":"He maintained that he was innocent."}],"breakdownApplicable":true,"breakdown":[{"part":"main-","type":"字根","gloss":"手"},{"part":"-tain","type":"字根","gloss":"握住"}],"origin":"經古法語 maintenir，源自拉丁文 manu tenere，意思是「用手握住」。","related":[{"word":"retain","note":"保留"},{"word":"contain","note":"包含"},{"word":"obtain","note":"獲得"}],"phrases":[{"phrase":"maintain contact with","zh":"與…保持聯繫","example":"We still maintain contact with our old classmates.","exampleZh":"我們還是和老同學保持聯繫。","cloze":false,"answer":"maintain contact with","distractors":["remain contact with","retain contact with","obtain contact with"],"whys":["remain 是「保持某狀態」，不接受詞。","retain 是「保留」，不和 contact with 連用。","obtain 是「獲得」，意思不合。"],"notes":["= keep in touch with"]}]}]}
```

## 要處理的字表

（貼在這裡，每行一個字；可以寫成「maintain,4」附上學測級別。）
