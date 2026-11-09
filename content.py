# -*- coding: utf-8 -*-
"""
所有语言共用的设置：图片、联系方式、网址、语言列表。
这里改一次，七种语言的网站都会跟着变。

网站上的文字（标题、介绍、按钮……）不在这里，
而是在 locales/ 文件夹里，每种语言一个文件：
    locales/zh_hans.py   简体中文（默认语言）
    locales/zh_hant.py   繁體中文
    locales/en.py        English
    locales/ja.py        日本語
    locales/ko.py        한국어
    locales/es.py        Español
    locales/fr.py        Français
"""

# ---------- 网站正式网址 ----------
# 用来告诉搜索引擎各语言版本的对应关系。换成自己的域名后改这里，结尾不要加 /
SITE_URL = "https://palace1689.netlify.app"

# ---------- 语言 ----------
# path：这个语言版本的网址后缀。默认语言留空 ""，网址就是首页本身。
#       例如 English 的 path 是 "en"，网址就是 https://palace1689.netlify.app/en/
# module：locales/ 文件夹里对应的文件名（不含 .py）
# label：语言按钮菜单里显示的名字（用该语言自己的写法）
LANGUAGES = [
    {"code": "zh-Hans", "path": "",        "module": "zh_hans", "label": "简体中文"},
    {"code": "zh-Hant", "path": "zh-hant", "module": "zh_hant", "label": "繁體中文"},
    {"code": "en",      "path": "en",      "module": "en",      "label": "English"},
    {"code": "ja",      "path": "ja",      "module": "ja",      "label": "日本語"},
    {"code": "ko",      "path": "ko",      "module": "ko",      "label": "한국어"},
    {"code": "es",      "path": "es",      "module": "es",      "label": "Español"},
    {"code": "fr",      "path": "fr",      "module": "fr",      "label": "Français"},
]
DEFAULT_LANGUAGE = "zh-Hans"   # 缺翻译时用这个语言的文字补上

# ---------- 栏目 ----------
# 六个栏目，每个都是单独的一页。这个顺序同时决定：
#   · 首页大折扇上六片扇叶从左到右的顺序（首页没有菜单栏）
#   · 其他页面顶部菜单从左到右的顺序
# 栏目名称在各语言文件的 MENU 里。"fans"（宫廷折扇）在菜单里还会展开 FANS_MENU 的子菜单。
NAV = ["story", "fans", "craft", "news", "themes", "contact"]

# “宫廷折扇”页面从上到下的区块，也是它的下拉子菜单
FANS_MENU = ["history", "masters", "categories", "showcase"]

# ---------- 每个区块的背景图 ----------
# 现在所有区块共用宫廷紫底色加暗金云纹。想给某个区块单独换背景图，
# 把图片放进 static/images/，在这里填文件名，例如 "story.jpg"。
BACKGROUNDS = {
    "intro": "",
    "story": "",
    "craft": "",
    "news": "",
    "themes": "",
    "contact": "",
    "history": "",
    "masters": "",
    "categories": "",
}

# ---------- 往期主题 ----------
# 首页“往期主题”的卡片，从左到右按这里的顺序显示。
# id：对应各语言文件里 THEMES 的名称和介绍。photo：配图（建议 3:2），link：“查看主题”打开的网址。
THEMES = [
    {"id": "theme1", "photo": "", "link": ""},
    {"id": "theme2", "photo": "", "link": ""},
    {"id": "theme3", "photo": "", "link": ""},
    {"id": "theme4", "photo": "", "link": ""},
]

# ---------- 折扇展示 ----------
# “宫廷折扇”页面最下方的大图轮播，按这里的顺序播放，每 5 秒换下一把。
# image：图片在 static/images/ 里的位置。
# master：这把扇子的大师，填 MASTERS 里的 id（例如 "master3"），留空显示“待填写”。
# price：定制价格，直接写要显示的文字，例如 "¥ 28,000 起"，留空显示“待填写”。
# 扇名和简介在各语言文件的 SHOWCASE 里（键名就是这里的 id）。
SHOWCASE = [
    {"id": "fan01", "image": "showcase/fan-01.jpg", "master": "", "price": ""},
    {"id": "fan02", "image": "showcase/fan-02.jpg", "master": "", "price": ""},
    {"id": "fan03", "image": "showcase/fan-03.jpg", "master": "", "price": ""},
    {"id": "fan04", "image": "showcase/fan-04.jpg", "master": "", "price": ""},
    {"id": "fan05", "image": "showcase/fan-05.jpg", "master": "", "price": ""},
    {"id": "fan06", "image": "showcase/fan-06.jpg", "master": "", "price": ""},
    {"id": "fan07", "image": "showcase/fan-07.jpg", "master": "", "price": ""},
    {"id": "fan08", "image": "showcase/fan-08.jpg", "master": "", "price": ""},
    {"id": "fan09", "image": "showcase/fan-09.jpg", "master": "", "price": ""},
    {"id": "fan10", "image": "showcase/fan-10.jpg", "master": "", "price": ""},
    {"id": "fan11", "image": "showcase/fan-11.jpg", "master": "", "price": ""},
    {"id": "fan12", "image": "showcase/fan-12.jpg", "master": "", "price": ""},
    {"id": "fan13", "image": "showcase/fan-13.jpg", "master": "", "price": ""},
    {"id": "fan14", "image": "showcase/fan-14.jpg", "master": "", "price": ""},
]
SHOWCASE_SECONDS = 5   # 自动切换的间隔（秒）

# ---------- 我们的资讯 ----------
# 网站按 date（日期）从新到旧排列：
#   “资讯·动态”页面显示全部。
# id：对应各语言文件里 NEWS 的标题和摘要。
# date：发布日期，格式 年-月-日，只用来排序，不显示在网页上。现在的日期是占位。
# photo：资讯配图（横向长方形，建议 3:2，例如 1200×800），放在 static/images/，留空显示占位。
# link：“查看全文”要打开的网址，暂时留空。
# 加一条资讯：在这里加一行（新的 id 和日期），再到每个语言文件的 NEWS 里加上同一个 id。
NEWS = [
    {"id": "news1",  "date": "2026-10-20", "photo": "", "link": ""},
    {"id": "news2",  "date": "2026-10-06", "photo": "", "link": ""},
    {"id": "news3",  "date": "2026-09-22", "photo": "", "link": ""},
    {"id": "news4",  "date": "2026-09-08", "photo": "", "link": ""},
    {"id": "news5",  "date": "2026-08-25", "photo": "", "link": ""},
    {"id": "news6",  "date": "2026-08-11", "photo": "", "link": ""},
    {"id": "news7",  "date": "2026-07-28", "photo": "", "link": ""},
    {"id": "news8",  "date": "2026-07-14", "photo": "", "link": ""},
    {"id": "news9",  "date": "2026-06-30", "photo": "", "link": ""},
    {"id": "news10", "date": "2026-06-16", "photo": "", "link": ""},
    {"id": "news11", "date": "2026-06-02", "photo": "", "link": ""},
    {"id": "news12", "date": "2026-05-19", "photo": "", "link": ""},
]

# ---------- 签约大师 ----------
# 网站会按 sort_name 的字母顺序排列大师：
#   首页“签约大师”显示排在最前面的 HOME_COUNT 位，“所有大师”页面显示全部。
# id：每位大师的编号，用来对应各语言文件里的名字和介绍，不要重复。
# sort_name：排序用的名字，填大师姓名的拼音，例如 "Wang Jianguo"。现在的 A～L 是占位。
# photo：照片文件名（放在 static/images/），留空显示占位圆圈。
# 加一位大师：在这里加一行（新的 id），再到每个语言文件的 MASTERS 里加上同一个 id。
MASTERS = [
    {"id": "master1",  "sort_name": "A", "photo": ""},
    {"id": "master2",  "sort_name": "B", "photo": ""},
    {"id": "master3",  "sort_name": "C", "photo": ""},
    {"id": "master4",  "sort_name": "D", "photo": ""},
    {"id": "master5",  "sort_name": "E", "photo": ""},
    {"id": "master6",  "sort_name": "F", "photo": ""},
    {"id": "master7",  "sort_name": "G", "photo": ""},
    {"id": "master8",  "sort_name": "H", "photo": ""},
    {"id": "master9",  "sort_name": "I", "photo": ""},
    {"id": "master10", "sort_name": "J", "photo": ""},
    {"id": "master11", "sort_name": "K", "photo": ""},
    {"id": "master12", "sort_name": "L", "photo": ""},
]

# ---------- 扇子类别 ----------
# 和大师一样：按 sort_name（中文名的拼音）字母顺序排列，
#   首页显示排在最前面的 HOME_COUNT 种，“所有扇子类型”页面显示全部。
# 七种语言用同一个顺序，所以每种语言的首页显示的都是同样的几种扇子。
CATEGORIES = [
    {"id": "embroidered",     "sort_name": "ci xiu shan mian zhe shan", "photo": ""},   # 刺绣扇面折扇
    {"id": "carved_ribs",     "sort_name": "diao gu zhe shan",          "photo": ""},   # 雕骨折扇
    {"id": "gongbi",          "sort_name": "gong bi hua niao zhe shan", "photo": ""},   # 工笔花鸟折扇
    {"id": "kesi",            "sort_name": "ke si shan mian zhe shan",  "photo": ""},   # 缂丝扇面折扇
    {"id": "mother_of_pearl", "sort_name": "luo dian gu zhe shan",      "photo": ""},   # 螺钿骨折扇
    {"id": "gold_painted",    "sort_name": "ni jin miao hua zhe shan",  "photo": ""},   # 泥金描画折扇
    {"id": "lacquer_gilt",    "sort_name": "qi gu miao jin zhe shan",   "photo": ""},   # 漆骨描金折扇
    {"id": "blue_green",      "sort_name": "qing lv shan shui zhe shan","photo": ""},   # 青绿山水折扇
    {"id": "gold_silk",       "sort_name": "sa jin juan mian zhe shan", "photo": ""},   # 洒金绢面折扇
    {"id": "sandalwood",      "sort_name": "tan xiang shan",            "photo": ""},   # 檀香扇
    {"id": "xiangfei_bamboo", "sort_name": "xiang fei zhu zhe shan",    "photo": ""},   # 湘妃竹折扇
    {"id": "zitan",           "sort_name": "zi tan gu zhe shan",        "photo": ""},   # 紫檀骨折扇
]

# “宫廷折扇”页面的“签约大师”“我们扇子的类别”各显示几个
HOME_COUNT = 4

# ---------- 联系方式 ----------
# value：显示出来的内容（电话号码、邮箱、账号名）。留空 "" 显示“待填写”。
# link：点击后打开的网址（例如 Instagram 主页），可以留空。
# 各语言里的名称（“电话”“Phone”……）在语言文件的 CONTACT_LABELS 里。
CONTACTS = [
    {"id": "phone",       "value": "", "link": ""},
    {"id": "email",       "value": "", "link": ""},
    {"id": "instagram",   "value": "", "link": ""},
    {"id": "tiktok",      "value": "", "link": ""},
    {"id": "whatsapp",    "value": "", "link": ""},
    {"id": "wechat",      "value": "", "link": ""},
    {"id": "xiaohongshu", "value": "", "link": ""},
    {"id": "youtube",     "value": "", "link": ""},
]
