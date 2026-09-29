# 字典檢查報告（Level 3、4、5）

## 完成範圍

| 級別 | 檢查字數 | 相似字對（去重後） | 形近 | 義近 | 兩者都是 |
|---|---|---|---|---|---|
| Level 3 | 999 / 999 | 706 | 280 | 408 | 18 |
| Level 4 | 995 / 995 | 790 | 307 | 461 | 22 |
| Level 5 | 998 / 998 | 864 | 289 | 553 | 22 |
| 合計 | 2,992 | 2,360 | 876 | 1,422 | 62 |

- 每級由 3–4 個 Sonnet 子代理分段平行處理（同一級別分成不重疊的字母段），全部 `apply` 由主代理依序執行，避免同級別互相覆蓋。
- 每批 `apply --dry-run` 都是 0 錯誤；全部 apply 後 `check` 為 0 錯誤、1 警告（fight 的字對例句因不規則變化 fought 找不到原形，是誤報）。
- 未做：Level 1、2、6。

## 品質檢查狀況（重要）

**這次沒有做人工或抽樣品質檢查**，依使用者指示直接 apply，之後由其他 AI 檢查。主代理只做了兩件事：

1. 用 `dict_batch.py` 驗證器擋錯誤（簡體字、缺欄位、字對格式等）。
2. apply 前機械式還原被代理動到的 `phrases`、`confusables`（規範規定原樣保留）：B 代理的 pronounce、proof（confusables），C 代理的 remote（phrases 與 confusables）。

## 需要人工確認的地方

- **字源（origin）**：代理憑記憶補寫，未逐條查證。各代理標為把握中等或較低的包括：
  pickle、reward、rhyme、resemble、thorough、plot、relevant、stereo、tragedy、sibling、skeleton、stack、spouse、sponsor、sole、await、bankrupt、comedy、diploma、cargo、disaster、disappoint、alert、mattress、orchard、mustard、province、purchase、residence、mint、merge、attic、astonish、chapel、calcium、ballot、browse、bureau、canvas、afford、alley、barn、beetle、bait、cupboard、edit、fist、flesh、flood、fold、fond、forever、fountain、freeze、koala、gossip、fuel、governor、heal、grocery、hesitate。
- **敏感或粗俗字義**：sin、suicide、sexual、sexy、queer、stool、suck、dumb、bloody、cock、breast、abortion、cocaine、communism、communist、seduce（seduce/tempt 字對）、ass。
- **內容有較大改動的字**：appeal、credit（各拆 5 個字義）、cricket、bang、attribute、debut、bound、democrat、mortality、miniature、norm、navy、producer、phenomenon、defy、denial、pension、recommend、sacred。
- **字對可能不符收錄標準**：hardware/software、microscope/telescope（同類字）、can/tin、flashlight/torch、check/tick（英美用字差異）、hire/recruit、plot/scheme、sandal/slipper、rip/tear、profit/revenue、efficiency/productivity；低分收錄：erase/wipe 0.473、knowledge/wisdom 0.457、hum/whistle 0.421。
- **候選清單以外、score 填 0.5 的字對**：各代理都有，例如 rob/steal、convince/persuade、air/heir、destination/destiny、discover/invent、passion/patience。
- **記憶法（tip）**：cease/seize、distinct/district、dye/die、elegant/elephant 的 tip 是代理自創聯想，未必好記。
- **字對數量偏多**：Level 4 的 E 段（364 組）、Level 5 的 H、J 段（295、284 組）平均每字超過 1 組，可考慮刪低分義近組。
- **例句是否在 7000 字內**：專案沒有 7000 字表，只能拿字典的 5,938 字粗略比對，代理自行判斷；已知可能超綱的有 hikers、rink、heartbeat、teamwork、ramp、puddle、worksheets、reusable。
- **原有資料的問題（依規定沒動）**：dedicate、delegate、nonsense、youngster、governor vs government、lettuce vs let us 的 confusables，以及 take a gamble、fuel up、make headlines、pearl of wisdom、prevent、pretend 的 phrases 內容有瑕疵；presence 的 forms 有重複（present · present · presenting）；assess 的 ext 只有 14 字。

## 常見錯誤類型（各代理回報，未經主代理逐條驗證）

- 例句太短（少於 8 字）或每個字義只有 1 句，幾乎全部補成 2 句。
- pattern 例句與字義例句是同一句（battery、conductor、consume、content、orphan、peculiar、relieve、perceive、raid 等），已換句。
- 字義錯或太偏：miniature 的「縮圖」、phenomenon 的「事件」、norm、bound 的排序、assault 的比喻用法。
- 字源說法錯誤：assemble（把 similar 當同根字）、outcome、recall；pension 的 related（pending、depend）不同源。
- 假的 commonErrors（其實是正確用法）：aboard、adverse、denial、recommend、sacred、pension、previous、profit、proof。
- 非同義字混進 synonyms（orphan 的 parentless child、photography 的 photographing）、非真反義（prevent 的 cause、protection 的 danger）。

## 還沒做完的

- Level 1、2、6（共 2,946 字）。
- 需要另一個 AI 或人工，依上面的清單審查 Level 3、4、5 的內容。
