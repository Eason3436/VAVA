# 字典檢查報告

## 進度

| 級別 | 已檢查 | 修改 | 相似字對（visual／semantic／both） |
|---|---|---|---|
| Level 2 | 989／989 | 約 985 字（只有少數字原本完全正確） | 565 組（185／351／29） |
| Level 6 | 908／997（另一個 AI 完成，主代理只抽查、未全面審查） | — | 275 組（109／145／21） |
| Level 1、3、4、5 | 0 | — | — |

- Level 2 全部 1,649 個字義都已補到 2 句例句。ext、搭配和句型也盡量補上了。
- `check` 結果：0 錯誤、2 警告。兩個警告都是例句用了不規則變化（won、struck），驗證器比對不到，句子本身正確。
- Level 3–5 另外做過一輪同義字專項修正（見 commit「同義字修正：Level 3／4／5」），但還沒有逐字完整檢查。

## 最常見的錯誤類型（Level 2）

1. **synonyms 不合格（最多）**
   - 混進片語：deal with、take part in、pick up。
   - 混進上位詞或不同的東西：road 列在 highway 下、machine 列在 engine 下、pot 列在 pan 下。
   - note 自己承認意思不同：blank 列在 empty 下、accept 列在 receive 下。
   - 混進易混字：prevent 列在 avoid 下、lonely 列在 alone 下。
   - 混進字典裡沒有的字：fridge、firefighter、slightly。
2. **一個字義塞了互不相干的意思**
   - 例如 match（比賽／火柴）、post（郵件／職位／柱子）、stamp（郵票／印章／蓋章／跺腳）、toast、tone。
   - 都已拆成各自的字義，每個字義有自己的例句。
3. **commonErrors 的錯句其實是對的**
   - 例如 "She traveled Taiwan"、"stick with the rules"、"bark every day"。
   - 已刪除，或換成學生真的常犯的錯：bark to → bark at、a nice travel → a nice trip、avoid to V → avoid V-ing。
4. **漏掉學測常用字義**
   - 例如 charge 的「充電」、operate 的「動手術」、state 的「州」、strike 的「侵襲」、support 的「扶養」、term 的「關係」（on good terms）。
5. **假反義已刪除**
   - 例如 cancel 的 continue、escape 的 face、value 的 neglect。

## 需要人工確認

- **新增或拆出的字義**：
  - absence（缺乏）、account（占比例）、apply（塗；敷）
  - folk adj.（民間的）、extra adv.（額外地）
  - hall（走廊）、law（定律）、cell（牢房）、positive（陽性的）、rare（三分熟的）
  - responsible（有責任感的）、sense（意義）、state、strike、support、succeed、term、speaker
  - wood（樹林）、triangle（三角鐵）
- **刪除的罕用字義**：
  - author v.（撰寫）、drug v.（使服麻醉藥）、leaf（書頁）、lid（眼皮）、shy（不足的）
  - soap 的 zh 改成只寫「肥皂」，soap opera 保留在搭配中。
- **需要查證的中文或字源**：
  - yam 的中文：台灣常指地瓜，要對照詞彙表。
  - medium rare 的熟度對應。
  - trade 的字源。
  - cabbage、cockroach、chopstick、coin 是新補的字源。
- **字義保留與否**：
  - 照原文保留但可能偏罕用：needle v.（逗弄）、wire v.（電匯）、contract（承包）、saw（see 的過去式字義）。
  - desert 的音標同時寫了兩組（名詞和動詞各一）。
- **字典沒收的字**：
  - 以下是常用字，可能是字表的缺漏，相關的同義字或字對因此沒辦法收：advertisement、complicated、agreement、relaxed、except、everywhere、living、fridge。
  - 部分反義字也不在字典裡（irregular、illegal、unsuitable 等），因為確實是反義，所以保留。
- **commit 訊息的小錯誤**：第二段的 commit 訊息誤寫成「到 policeman」，實際是做到 couple。原因是 eyebrow、hamburger、policeman 在字典檔裡的排序比較前面。
