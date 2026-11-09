# -*- coding: utf-8 -*-
"""
Palace1689 宫廷折扇网站（多语言版）

运行网站（本地预览）：
    python app.py
然后在浏览器打开 http://127.0.0.1:5000
    首页（大折扇）http://127.0.0.1:5000/
    品牌故事      http://127.0.0.1:5000/story/
    宫廷折扇      http://127.0.0.1:5000/fans/
    手艺传承      http://127.0.0.1:5000/craft/
    资讯·动态     http://127.0.0.1:5000/news/
    往期主题      http://127.0.0.1:5000/themes/
    联系我们      http://127.0.0.1:5000/contact/
    所有大师      http://127.0.0.1:5000/masters/
    所有扇子类型  http://127.0.0.1:5000/collections/
其他语言在前面加语言代码，例如英文首页 /en/、英文宫廷折扇页 /en/fans/
（语言代码：zh-hant、en、ja、ko、es、fr）

导出成静态网页（上传到 Netlify 等主机）：
    python app.py build
导出的文件在 dist/ 文件夹里。
"""
import importlib
import math
import shutil
import sys
from pathlib import Path

from flask import Flask, abort, render_template

import content

BASE = Path(__file__).parent
app = Flask(__name__)

# 每种语言用的字体（Google Fonts）：都是宋体/明朝体一类有顿笔的衬线字体。
#   网址参数, 字体名（含备用字体）
FONTS = {
    "zh-Hans": ("Noto+Serif+SC:wght@400;500;600;700;900",
                '"Noto Serif SC","Songti SC","STSong","SimSun",serif'),
    "zh-Hant": ("Noto+Serif+TC:wght@400;500;600;700;900",
                '"Noto Serif TC","Songti TC","PMingLiU",serif'),
    "ja":      ("Noto+Serif+JP:wght@400;500;600;700;900",
                '"Noto Serif JP","Hiragino Mincho ProN","Yu Mincho",serif'),
    "ko":      ("Noto+Serif+KR:wght@400;500;600;700;900",
                '"Noto Serif KR","AppleMyungjo","Batang",serif'),
}
# 英、西、法文：EB Garamond，笔画粗细变化明显的古典衬线体
LATIN_FONTS = ("EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400",
               '"EB Garamond","Garamond","Times New Roman",serif')

LANG_BY_CODE = {l["code"]: l for l in content.LANGUAGES}
LANG_BY_PATH = {l["path"]: l for l in content.LANGUAGES}
# 除首页外的页面：页面名 → 网址里的文件夹名
# 首页的六片扇叶各对应一个页面（顺序见 content.NAV）；另有两个列表页
PAGES = {"story": "story", "fans": "fans", "craft": "craft", "news": "news", "themes": "themes",
         "contact": "contact", "masters": "masters", "collections": "collections"}
# 每个页面在顶部菜单里高亮哪一项
ACTIVE = {**{s: s for s in ["story", "fans", "craft", "news", "themes", "contact"]},
          "masters": "fans", "collections": "fans"}


def fan_label(text_, vertical, mid, pt, rc, room):
    """扇叶上的文字。中文、日文：一个字一个字竖排；其他语言：沿扇叶方向横排。
    字号按文字长短自动缩小，保证放得进扇叶。"""
    if vertical:
        chars = list(text_)
        step = 1.1
        fs = min(40.0, room / (len(chars) * step))
        out = []
        for k, ch in enumerate(chars):
            x, y = pt(rc - (k - (len(chars) - 1) / 2) * fs * step, mid)
            rot = mid + (90 if ch in "ー—…" else 0)       # 长音符号竖排时要转 90°
            out.append({"ch": ch, "x": round(x, 1), "y": round(y, 1), "rot": round(rot, 2)})
        return {"chars": out, "fs": round(fs, 1)}
    # 横排：估算文字宽度（拉丁字母约 0.5 个字宽，韩文约 0.95，空格约 0.3）
    width = sum(0.3 if c == " " else 0.95 if ord(c) > 0x2E80 else 0.52 for c in text_)
    fs = min(38.0, room / max(width, 1))
    x, y = pt(rc, mid)
    rot = mid + 90 if mid < 0 else mid - 90                 # 左半边由外往里读，右半边由里往外读，文字都不倒
    return {"x": round(x, 1), "y": round(y, 1), "rot": round(rot, 2), "fs": round(fs, 1)}


def fan_leaves(items, vertical=True, cx=500.0, cy=560.0, R=480.0, r0=168.0, span=160.0):
    """首页大折扇：每个栏目一片扇叶。返回每片扇叶的形状、文字位置和角度（SVG 坐标）。"""
    n = len(items)
    step = span / n
    gap = 0.5                                   # 扇叶之间留一点缝，露出扇骨
    pt = lambda r, deg: (cx + r * math.sin(math.radians(deg)), cy - r * math.cos(math.radians(deg)))
    leaves = []
    for i, item in enumerate(items):
        a1 = -span / 2 + i * step + gap
        a2 = -span / 2 + (i + 1) * step - gap
        mid = (a1 + a2) / 2
        (x1, y1), (x2, y2) = pt(R, a1), pt(R, a2)
        (x3, y3), (x4, y4) = pt(r0, a2), pt(r0, a1)
        d = (f"M{x1:.1f} {y1:.1f} A{R} {R} 0 0 1 {x2:.1f} {y2:.1f} "
             f"L{x3:.1f} {y3:.1f} A{r0} {r0} 0 0 0 {x4:.1f} {y4:.1f}Z")
        text_ = fan_label(item["label"], vertical, mid, pt, (R + r0) / 2 - 4, R - r0 - 104)
        dx, dy = pt(14, mid)                    # 鼠标移上去时，扇叶沿中线向外挪一点
        ox, oy = pt(R - 28, mid)                # 扇叶顶端的小金点
        leaves.append({**item, "d": d, "text": text_, "mid": round(mid, 2), "delay": round((i + 0.5) / n * 300),
                       "dx": round(dx - cx, 1), "dy": round(dy - cy, 1), "ox": round(ox, 1), "oy": round(oy, 1),
                       "shade": i % 2})
    ribs = []
    for k in range(n + 1):                      # 扇骨：每两片扇叶之间一根，两端是较粗的大骨
        a = -span / 2 + k * step
        guard = k in (0, n)
        x, y = pt(R + (6 if guard else -6), a)
        ribs.append({"x": round(x, 1), "y": round(y, 1), "w": 9 if guard else 3.5,
                     "deg": round(a, 2), "delay": round(k / n * 300)})   # 打开动画：扇骨的角度和起步时间
    return {"leaves": leaves, "ribs": ribs, "cx": cx, "cy": cy, "R": R, "r0": r0}


def load_locale(lang):
    return importlib.import_module("locales." + lang["module"])


def text(locale, default, name):
    """取某个语言文件里的一项；没有就用默认语言补上。"""
    return getattr(locale, name, getattr(default, name))


def by_id(items, locale, default, name, lang_code, warn):
    """把共用设置（照片、链接）和语言文件里的文字按 id 合并。"""
    words = getattr(locale, name, {})
    fallback = getattr(default, name, {})
    merged = []
    for item in items:
        t = words.get(item["id"])
        if t is None:
            t = fallback.get(item["id"], {})
            if warn:
                print(f"⚠ {lang_code}：{name} 里缺少 “{item['id']}” 的翻译，暂时显示默认语言的文字")
        merged.append({**item, **t})
    return merged


def sort_key(item):
    return item.get("sort_name", item["id"]).casefold()


def page_context(lang, page="home", warn=False):
    default = load_locale(LANG_BY_CODE[content.DEFAULT_LANGUAGE])
    loc = load_locale(lang)
    slug = PAGES.get(page, "")
    depth = (1 if lang["path"] else 0) + (1 if slug else 0)
    up = "../" * depth                                      # 从当前页面回到网站根目录
    root = up + (lang["path"] + "/" if lang["path"] else "")  # 这个语言的首页
    home = root or "./"
    link = lambda s: (root + s + "/") if root else (s + "/")  # 这个语言的某个页面
    fans = link("fans")

    lang_links = []
    for l in content.LANGUAGES:
        rel = (l["path"] + "/" if l["path"] else "") + (slug + "/" if slug else "")
        lang_links.append({**l, "href": (up + rel) or "./", "current": l is lang,
                           "url": content.SITE_URL + "/" + rel})

    words = text(loc, default, "MENU")
    label = lambda s: words.get(s, default.MENU.get(s, s))
    fans_prefix = "" if page == "fans" else fans
    nav = []
    for s in content.NAV:
        item = {"id": s, "label": label(s), "href": link(s)}
        if s == "fans":
            item["children"] = [{"id": c, "label": label(c), "href": fans_prefix + "#" + c}
                                for c in content.FANS_MENU]
        nav.append(item)

    labels = text(loc, default, "CONTACT_LABELS")
    contacts = [{**c, "label": labels.get(c["id"], default.CONTACT_LABELS.get(c["id"], c["id"]))}
                for c in content.CONTACTS]

    masters = by_id(sorted(content.MASTERS, key=sort_key), loc, default, "MASTERS", lang["code"], warn)
    categories = by_id(sorted(content.CATEGORIES, key=sort_key), loc, default, "CATEGORIES", lang["code"], warn)
    news = by_id(sorted(content.NEWS, key=lambda x: x.get("date", ""), reverse=True), loc, default, "NEWS", lang["code"], warn)
    names = {m["id"]: m.get("name", "") for m in masters}
    showcase = [{**f, "master_name": names.get(f.get("master", ""), "")}
                for f in by_id(content.SHOWCASE, loc, default, "SHOWCASE", lang["code"], warn)]
    n = content.HOME_COUNT

    fonts = FONTS.get(lang["code"], LATIN_FONTS)
    return {
        "page": page,
        "active": ACTIVE.get(page, ""),
        "lang": lang,
        "lang_links": lang_links,
        "site_url": content.SITE_URL,
        "static": up + "static/",
        "home": home,
        "fans_href": fans,
        "masters_href": link("masters"),
        "collections_href": link("collections"),
        "fonts_query": fonts[0], "font_family": fonts[1],
        "meta": text(loc, default, "META"),
        "brand": text(loc, default, "BRAND"),
        "ui": text(loc, default, "UI"),
        "nav": nav,
        "fan": fan_leaves(nav, lang["code"] in ("zh-Hans", "zh-Hant", "ja")) if page == "home" else None,
        "fans_sections": content.FANS_MENU,
        "menu_labels": {s: label(s) for s in [*content.NAV, *content.FANS_MENU]},
        "backgrounds": content.BACKGROUNDS,
        "history": text(loc, default, "HISTORY"),
        "craft": text(loc, default, "CRAFT"),
        "story": text(loc, default, "STORY"),
        "news_section": text(loc, default, "NEWS_SECTION"),
        "news": news,
        "themes_section": text(loc, default, "THEMES_SECTION"),
        "themes": by_id(content.THEMES, loc, default, "THEMES", lang["code"], warn),
        "masters_section": text(loc, default, "MASTERS_SECTION"),
        "masters": masters if page == "masters" else masters[:n],
        "categories_section": text(loc, default, "CATEGORIES_SECTION"),
        "categories": categories if page == "collections" else categories[:n],
        "showcase_section": text(loc, default, "SHOWCASE_SECTION"),
        "showcase": showcase,
        "showcase_seconds": content.SHOWCASE_SECONDS,
        "contact_section": text(loc, default, "CONTACT_SECTION"),
        "contacts": contacts,
    }


def render(lang, page="home", warn=False):
    return render_template("index.html", **page_context(lang, page, warn))


@app.route("/")
def home():
    return render(LANG_BY_PATH[""])


@app.route("/<name>/")
def first_level(name):
    """/fans/、/masters/ 等是默认语言的页面；/en/ 等是其他语言的首页。"""
    if name in PAGES.values():
        return render(LANG_BY_PATH[""], name)
    lang = LANG_BY_PATH.get(name)
    if lang is None or name == "":
        abort(404)
    return render(lang)


@app.route("/<lang_path>/<name>/")
def second_level(lang_path, name):
    lang = LANG_BY_PATH.get(lang_path)
    if lang is None or lang_path == "" or name not in PAGES.values():
        abort(404)
    return render(lang, name)


def build(out_dir: Path = BASE / "dist"):
    """导出 dist/：首页是默认语言，其他语言在 dist/en/、dist/ja/ ……"""
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    with app.test_request_context("/"):
        for lang in content.LANGUAGES:
            for page in ["home", *PAGES]:
                parts = [p for p in (lang["path"], PAGES.get(page, "")) if p]
                target = out_dir.joinpath(*parts)
                target.mkdir(parents=True, exist_ok=True)
                (target / "index.html").write_text(render(lang, page, warn=(page == "home")), encoding="utf-8")
            print(f"✓ {lang['label']:<8} → dist/{lang['path'] + '/' if lang['path'] else ''}（首页和 {len(PAGES)} 个子页面）")
    shutil.copytree(BASE / "static", out_dir / "static")
    print(f"已导出到 {out_dir}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        build()
    else:
        # 启动时检查一遍各语言有没有缺翻译
        with app.test_request_context("/"):
            for lang in content.LANGUAGES:
                page_context(lang, warn=True)
        # debug=True：改了文件后自动重新加载
        app.run(debug=True)
