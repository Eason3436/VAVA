# Level 2–5 缺漏排查（2026-10-12）

比對基準：大考中心《高中英文參考詞彙表》（111 學年度起適用，6,012 詞條）。
排查範圍：`packs/dict/level2–5.json`。`dict_batch.py check` 結果：0 錯誤、2 警告（won、struck，已知可忽略）。

## 1. 收字與級別

- 字典 5,938 字全部在官方詞彙表內，**級別 0 筆不一致**。
- 官方表有、字典沒有獨立條目的字，分成三類：

### 1.1 功能詞（整本字典刻意不收，L1 也一樣不收 the、of、and 等）

| 級別 | 字 |
|---|---|
| L2 | against、among、nor、per、till、toward(s)、unless、upon、whoever、whom |
| L3 | beneath、onto |
| L4 | concerning、despite、including、regarding |
| L5 | lest、versus、via、whereas |

這些都是學測常考的介系詞與連接詞，尤其 despite、unless、whereas、against、among。
若 App 需要收，要另外決定；依任務規範「不新增、刪除字」，本次沒有動。

### 1.2 真的漏掉的實詞

| 級別 | 字 | 說明 |
|---|---|---|
| L2 | café／cafe | 字典完全沒有，也沒掛在其他字下 |
| L4 | capitalism | 官方掛在 capital(ism)；capital 的 forms 有 capitalist，沒有 capitalism |

### 1.3 官方列為異體或並列詞，字典條目裡完全沒提到

官方把這些字和主條目寫成同一詞條（例如 refrigerator/fridge），但字典的主條目 forms、字義、例句都沒出現：

| 級別 | 缺的字 → 應掛的主條目 |
|---|---|
| L2 | fridge → refrigerator、coke → cola、cop → policeman、railway → railroad、metro／underground → subway、salesman／saleswoman → salesperson、heroine → hero、firewoman → fireman、forwards → forward、anyplace → anywhere、judgement → judgment |
| L3 | advisor → adviser、disc → disk、mike → microphone、humankind → mankind |
| L4 | wizard → witch |

建議做法：補進主條目的 `forms`（例如 refrigerator 的 forms 加上 fridge），不必新增字。
REPORT.md 原本列為「字典沒收」的 fridge，其實就是這一類。

其餘 -ment 名詞（argument、equipment、achievement……）與 -s 形（wages、savings、statistics……）都已寫在主條目的 forms，沒有缺。

## 2. 詞性缺漏（對照官方標的詞性）

官方會把罕用詞性也列出，所以大部分不用補（lamb v.、steel v.、drug v. 等是刻意刪的）。
下面只列**學測會用到、建議補**的：

| 級別 | 字 | 缺的字義 |
|---|---|---|
| L2 | better | v. 改善（better oneself） |
| L2 | daily | n. 日報 |
| L2 | express | n. 快車 |
| L2 | fry | n. 薯條（fries，常見） |
| L2 | divide | n. 分歧；差距（digital divide） |
| L4 | contrary | n. 相反（on the contrary，常考，目前完全沒有） |
| L4 | transfer | n. 轉乘；轉學；轉帳 |
| L4 | resolve | n. 決心 |
| L4 | noble | n. 貴族 |
| L5 | combat | n. 戰鬥（名詞比動詞常見） |
| L5 | resume | n. 履歷（résumé） |

全部 153 筆詞性差異（L2 43、L3 10、L4 28、L5 72）見附錄。

## 3. 欄位內容缺漏

| 項目 | L2 | L3 | L4 | L5 | 規範 |
|---|---|---|---|---|---|
| 字數／字義數 | 989／1,649 | 999／1,495 | 995／1,428 | 998／1,432 | — |
| **已逐字檢查** | **989（完成）** | **0** | **0** | **0** | — |
| 字義只有 1 句例句 | 0 | 1,411 | 1,379 | 1,408 | 每字義 2 句 |
| 字義沒有 ext | 377 | 644 | 954 | 1,016 | 盡量補 |
| 字義沒有搭配 | 6 | 77 | 126 | 119 | 2–4 個 |
| 沒有 origin | 398 | 452 | 373 | 339 | 可查證才寫 |
| 沒有 commonErrors | 655 | 601 | 699 | 779 | 不硬湊 |
| 同義字少於 2 個 | 381 | 165 | 71 | 83 | 2–4 個 |
| 沒有 forms | 73 | 47 | 36 | 50 | 不可數名詞、副詞可留空 |
| 相似字對 | 565 組 | 0 | 0 | 0 | 0–5 組／字 |

- 沒有任何字缺中文、缺字義、缺音標，也沒有例句缺中英文。
- 沒有 forms 的字幾乎都是副詞、不可數名詞、只有原級的形容詞，屬於正常留空。
  可以補的少數例如 remote（remotely）、raw（rawness）；beware 只用原形，留空正確。
- L2 同義字少於 2 個有 381 字，是逐字檢查時刪掉不合格同義字後留下的，屬於「寧缺勿濫」，不是漏做。

## 4. 結論

1. **最大的缺漏是 L3、L4、L5 還完全沒有逐字檢查**：約 4,200 個字義只有 1 句例句、相似字對 0 組。這部分要照 docs/cloud-dict-task.md 的流程（3 → 4 → 5）一批 20 字做。
2. 收字面：café 和 capitalism 是真的漏收；另有 17 個官方異體字沒有掛在主條目的 forms。
3. 字義面：on the contrary 的 contrary n.、transfer n.、combat n. 等 11 個常用詞性缺字義。
4. 20 個功能詞（despite、unless、among 等）整本字典沒收，要由使用者決定是否新增。

## 附錄：詞性差異全表（官方有、字典沒有）

### Level 2（43）
absent v.、author v.、better n./v.、cartoon v.、curtain v.、daily n.、divide n.、double adv./n.、downstairs n.、drug v.、due adv./n.、express adv./n.、fair adv.、firm adv.、fit adv.、fix n.、forward n.、fry n.、gun v.、hop n.、ill adv./n.、ink v.、iron adj.、lamb v.、none adv.、perfect n.、plus adj.、positive n.、post adv.、roof v.、sour n./v.、sport v.、steel v.、stone v.、such pron.、sudden n.、true adv./v.、upset n.、upstairs n.、vacation v.、whenever adv.、worm v.、worse n.

### Level 3（10）
cable v.、faint n.、freeze n.、meanwhile n.、rough n.、scatter n.、steady adv./n.、unique n.、wrap n.、zipper v.

### Level 4（28）
addict v.、bankrupt n.、cease n.、chew n.、choke n.、concrete v.、contrary n.、counter adj./adv.、damp n./v.、disorder v.、dodge n.、earnest n.、ethnic n.、evidence v.、fetch n.、initial v.、intermediate n./v.、intimate n.、noble n.、resolve n.、revenge v.、scold n.、sculpture v.、slight n./v.、stab n.、transfer n.、universal n.、voyage v.

### Level 5（72）
alternate n.、ballot v.、beloved n.、browse n.、canvas v.、certificate v.、collective n.、colonial n.、combat n.、compact n.、constitutional n.、coordinate adj.、cripple n.、crystal adj.、dome v.、exotic n.、exploit n.、external n.、foul adv.、gross n.、horizontal n.、implement n.、incentive adj.、initiate adj./n.、initiative adj.、jug v.、league v.、legitimate v.、masculine n.、meantime adv.、metropolitan n.、midst prep.、mock n.、neutral n.、nowhere pron.、nutrient adj.、overall n.、overturn n.、patent adj.、pension v.、perspective adj.、plunge n.、prior adv./n.、progressive n.、prospect v.、ranch v.、recipient adj.、regardless adj.、resume n.、retail adv.、rib v.、ridge v.、saint v.、sheer adv.、slap adv.、snatch n.、sneak n.、sole v.、spectacular n.、steer n.、stumble n.、texture v.、torch v.、transit v.、triple n.、ultimate n.、underline n.、verbal n.、vertical n.、whatsoever adj./pron.、whereabouts adv.、yacht v.
