"""
字典逐字檢查＋補資料＋相似字整理的批次工具（給雲端 Claude 用，流程見 docs/cloud-dict-task.md）。

  python scripts/dict_batch.py status                       # 各級進度
  python scripts/dict_batch.py show --level 3 --n 20        # 印出下一批還沒檢查的字（條目＋相似候選）
  python scripts/dict_batch.py apply out/batch.json         # 驗證後寫回 packs/dict/levelN.json 與 similar/levelN.json
  python scripts/dict_batch.py check                        # 全部重新驗證
  python scripts/dict_batch.py pack                         # 把目前成果打包成 out/dict-result-<時間>.zip（給使用者下載）

apply 的輸入：
  { "level": 3,
    "words": [ 完整的單字物件（DictModels.kt 的 WordJson 格式），整筆取代原條目 ],
    "pairs": [ 相似字對，格式見 docs/similar-format.md ],
    "reviewed": [ 這批檢查完的字（含沒改動的） ] }
有錯誤就整批不寫入；只有警告會照寫並印出來。
"""
import argparse, glob, json, os, re, sys, time

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT = os.path.join(ROOT, "packs", "dict")
SIM_DIR = os.path.join(DICT, "similar")
CAND = os.path.join(DICT, "similar-candidates.json")
PROGRESS_DIR = os.path.join(DICT, "review")  # 每級一個檔，各級可以平行處理不互相覆蓋

SIMPLIFIED = set("们这个时说对会为来还发经过进关应问题见观现让认设语话请车东门长开间实际网络视频质软没么样动学习给头买卖钱电脑书写读")
POS = {"n.", "v.", "adj.", "adv.", "prep.", "conj.", "pron.", "int.", "aux.", "art.", "det.", "num.", "phr."}
KINDS = {"visual", "semantic", "both"}


def level_path(n):
    return os.path.join(DICT, f"level{n}.json")


def load_level(n):
    return json.load(open(level_path(n), encoding="utf-8"))


def save(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")
    os.replace(tmp, path)


def all_words():
    out = {}
    for n in range(1, 7):
        for w in load_level(n)["words"]:
            out[w["word"].strip().lower()] = n
    return out


def progress_path(n):
    return os.path.join(PROGRESS_DIR, f"level{n}.json")


def load_progress(n=None):
    out = {"reviewed": {}}
    for k in ([n] if n else range(1, 7)):
        if os.path.exists(progress_path(k)):
            out["reviewed"].update(json.load(open(progress_path(k), encoding="utf-8"))["reviewed"])
    return out


def load_pairs():
    pairs = {}
    for f in sorted(glob.glob(os.path.join(SIM_DIR, "level*.json"))):
        for p in json.load(open(f, encoding="utf-8"))["pairs"]:
            pairs[(p["a"], p["b"])] = p
    return pairs


def zh_of(entry):
    return "；".join(f"{m.get('pos', '')}{m.get('zh', '')}" for m in entry.get("meanings", []))


def simp(s):
    return sorted({c for c in s if c in SIMPLIFIED})


def texts(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from texts(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from texts(v)


def check_word(w, errors, warns):
    word = w.get("word", "").strip()
    tag = f"[{word}]"
    if not word:
        errors.append("有條目沒有 word")
        return
    ms = w.get("meanings", [])
    if not ms:
        errors.append(f"{tag} 沒有 meanings")
    for i, m in enumerate(ms):
        if not m.get("zh", "").strip():
            errors.append(f"{tag} 字義 {i} 沒有中文")
        for p in re.split(r"[/,\s]+", m.get("pos", "")):
            if p and p not in POS:
                warns.append(f"{tag} 字義 {i} 詞性「{m.get('pos')}」不在常用清單")
        exs = m.get("examples", [])
        if not exs:
            warns.append(f"{tag} 字義 {i} 沒有例句")
        for e in exs:
            if not e.get("en", "").strip() or not e.get("zh", "").strip():
                errors.append(f"{tag} 字義 {i} 有例句缺英文或中文")
    syn = [s.get("word", "").strip().lower() for s in w.get("synonyms", [])]
    # 第一個放目標字本身當對照（docs/codex-dict-prompt.md 第 26 條），其他位置不能再出現
    if word.lower() in syn[1:]:
        errors.append(f"{tag} 同義字清單第一個以外又出現自己")
    if syn and syn[0] != word.lower():
        warns.append(f"{tag} 同義字第一個應該是目標字本身")
    if len(syn) != len(set(syn)):
        errors.append(f"{tag} 同義字重複")
    bad = simp("".join(texts(w)))
    if bad:
        errors.append(f"{tag} 有簡體字：{''.join(bad)}")


def form_hit(word, sentence):
    s = sentence.lower()
    w = word.lower()
    return w in s or w[: max(3, len(w) - 2)] in s


def check_pair(p, words, errors, warns):
    a, b = p.get("a", "").lower(), p.get("b", "").lower()
    tag = f"[{a}/{b}]"
    if not a or not b or a == b:
        errors.append(f"{tag} a、b 不能空白或相同")
        return
    if a > b:
        errors.append(f"{tag} a 要依字母順序排在 b 前面")
    for x in (a, b):
        if x not in words:
            errors.append(f"{tag} {x} 不在字典裡")
    if p.get("kind") not in KINDS:
        errors.append(f"{tag} kind 要是 visual／semantic／both")
    for k in ("diff", "tip", "aZh", "bZh"):
        if not str(p.get(k, "")).strip():
            errors.append(f"{tag} 缺 {k}")
    pts = p.get("points", [])
    if not (1 <= len(pts) <= 4):
        warns.append(f"{tag} points 建議 2–4 點")
    for k, x in (("exA", a), ("exB", b)):
        ex = p.get(k) or {}
        if not ex.get("en") or not ex.get("zh"):
            errors.append(f"{tag} {k} 缺英文或中文")
        elif not form_hit(x, ex["en"]):
            warns.append(f"{tag} {k} 例句裡找不到 {x}")
    bad = simp("".join(texts(p)))
    if bad:
        errors.append(f"{tag} 有簡體字：{''.join(bad)}")


def cmd_status(_):
    prog = load_progress()["reviewed"]
    pairs = load_pairs()
    total = 0
    for n in range(1, 7):
        ws = [w["word"].lower() for w in load_level(n)["words"]]
        done = sum(1 for w in ws if w in prog)
        total += done
        print(f"Level {n}: {done}/{len(ws)}")
    print(f"合計已檢查 {total} 字，相似字對 {len(pairs)} 組")


def trim(key, rows):
    """義近候選檔每字都湊滿 15 個以上，低分的多半是雜訊（borrow → book、that）：顯示時只留分數 ≥ 0.35 的前 10 個，
    再加最多 5 個「只靠中文重疊」的。形近、同族照原樣。"""
    if key != "semantic":
        return rows
    main = [x for x in rows if not x.get("zhOnly") and x["s"] >= 0.35][:10]
    return main + [x for x in rows if x.get("zhOnly")][:5]


def cmd_show(a):
    prog = load_progress()["reviewed"]
    cand = json.load(open(CAND, encoding="utf-8"))["words"] if os.path.exists(CAND) else {}
    words_by = {}
    for n in range(1, 7):
        for w in load_level(n)["words"]:
            words_by[w["word"].lower()] = w
    pairs = load_pairs()
    todo = [w for w in load_level(a.level)["words"] if w["word"].lower() not in prog]
    if a.start:
        todo = [w for w in todo if w["word"].lower() >= a.start.lower()]
    batch = todo[: a.n]
    if not batch:
        print("這一級已經全部檢查完")
        return
    for w in batch:
        k = w["word"].lower()
        print("=" * 60)
        print(json.dumps(w, ensure_ascii=False))
        c = cand.get(k, {})
        done_with = {p["b"] if p["a"] == k else p["a"] for p in pairs.values() if k in (p["a"], p["b"])}
        for label, key in (("形近候選", "visual"), ("同族（只在真的常搞混時才收）", "family"), ("義近候選", "semantic")):
            rows = []
            for x in trim(key, c.get(key, [])):
                o = words_by.get(x["w"])
                mark = "（已有字對）" if x["w"] in done_with else ""
                extra = f" 共同中文:{'/'.join(x['zh'])}" if x.get("zh") else ""
                if x.get("sound"):
                    extra += " 音近"
                if x.get("sig", {}).get("rule"):
                    extra += " 拼字規則"
                if x.get("ant"):
                    extra += " 字典標為反義"
                if x.get("zhOnly"):
                    extra += " 只靠中文重疊"
                rows.append(f"  {x['w']} {x['s']}{mark} L{o.get('level', '?') if o else '?'} {zh_of(o) if o else ''}{extra}")
            if rows:
                print(f"-- {label}")
                print("\n".join(rows))
    print("=" * 60)
    print(f"本批 {len(batch)} 字：{', '.join(w['word'] for w in batch)}；這一級還剩 {len(todo) - len(batch)} 字")


def cmd_apply(a):
    data = json.load(open(a.file, encoding="utf-8"))
    n = int(data["level"])
    words = all_words()
    errors, warns = [], []
    for w in data.get("words", []):
        check_word(w, errors, warns)
        if words.get(w.get("word", "").strip().lower()) != n:
            errors.append(f"[{w.get('word')}] 不是 Level {n} 的字（不能新增或改字）")
    for p in data.get("pairs", []):
        check_pair(p, words, errors, warns)
    for x in warns:
        print("警告", x)
    if a.dry_run:
        print(f"試跑：錯誤 {len(errors)}、警告 {len(warns)}，沒有寫入")
        for x in errors:
            print("錯誤", x)
        sys.exit(1 if errors else 0)
    if errors:
        for x in errors:
            print("錯誤", x)
        print(f"有 {len(errors)} 個錯誤，整批沒有寫入")
        sys.exit(1)
    lv = load_level(n)
    idx = {w["word"].strip().lower(): i for i, w in enumerate(lv["words"])}
    for w in data.get("words", []):
        k = w["word"].strip().lower()
        w.setdefault("level", n)
        lv["words"][idx[k]] = w
    save(level_path(n), lv)
    os.makedirs(SIM_DIR, exist_ok=True)
    sp = os.path.join(SIM_DIR, f"level{n}.json")
    sim = json.load(open(sp, encoding="utf-8")) if os.path.exists(sp) else {"version": 1, "pairs": []}
    existing = load_pairs()
    added = 0
    for p in data.get("pairs", []):
        key = (p["a"].lower(), p["b"].lower())
        if key in existing:
            # 同一組已經寫過：只在新版本 kind 更完整時更新 kind
            old = existing[key]
            if old.get("kind") != p["kind"] and "both" not in (old.get("kind"),):
                old["kind"] = "both"
            continue
        sim["pairs"].append(p)
        existing[key] = p
        added += 1
    save(sp, sim)
    prog = load_progress(n)
    today = time.strftime("%Y-%m-%d")
    for w in data.get("reviewed", []) + [w["word"] for w in data.get("words", [])]:
        prog["reviewed"][w.strip().lower()] = today
    os.makedirs(PROGRESS_DIR, exist_ok=True)
    save(progress_path(n), prog)
    print(f"Level {n}：更新 {len(data.get('words', []))} 字、新增 {added} 組相似字、標記檢查完 {len(set(data.get('reviewed', [])))} 字")


def cmd_check(_):
    words = all_words()
    errors, warns = [], []
    for n in range(1, 7):
        for w in load_level(n)["words"]:
            check_word(w, errors, warns)
    for p in load_pairs().values():
        check_pair(p, words, errors, warns)
    print(f"錯誤 {len(errors)}、警告 {len(warns)}")
    for x in errors[: a_limit]:
        print("錯誤", x)
    from collections import Counter
    for k, v in Counter(re.sub(r"^\[[^\]]*\] ", "", re.sub(r"字義 \d+", "字義 N", x)) for x in warns).most_common(10):
        print(f"警告 ×{v}", k)


a_limit = 80


def cmd_pack(_):
    """成果打包：六級字典、相似字對、進度、報告。使用者下載後交給本機合併回 packs/dict/。"""
    import zipfile
    out = os.path.join(ROOT, "out")
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, f"dict-result-{time.strftime('%Y%m%d-%H%M')}.zip")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for n in range(1, 7):
            z.write(level_path(n), f"packs/dict/level{n}.json")
        for d in (SIM_DIR, PROGRESS_DIR):
            for f in sorted(glob.glob(os.path.join(d, "*.json"))):
                z.write(f, os.path.relpath(f, ROOT).replace(os.sep, "/"))
        rep_ = os.path.join(ROOT, "REPORT.md")
        if os.path.exists(rep_):
            z.write(rep_, "REPORT.md")
    cmd_status(None)
    print(f"已打包：{path}（{os.path.getsize(path) / 1e6:.1f} MB）")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    s = sub.add_parser("show")
    s.add_argument("--level", type=int, required=True)
    s.add_argument("--n", type=int, default=20)
    s.add_argument("--start", default="")
    s2 = sub.add_parser("apply")
    s2.add_argument("file")
    s2.add_argument("--dry-run", action="store_true", help="只驗證不寫入")
    sub.add_parser("check")
    sub.add_parser("pack")
    args = ap.parse_args()
    {"status": cmd_status, "show": cmd_show, "apply": cmd_apply, "check": cmd_check, "pack": cmd_pack}[args.cmd](args)
