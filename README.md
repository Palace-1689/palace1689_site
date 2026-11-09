# Palace1689 宫廷折扇网站（多语言版）

Palace1689 品牌官网：高端定制宫廷折扇，七种语言（简体中文、繁體中文、English、日本語、한국어、Español、Français）。

- 网站地址：https://palace1689.netlify.app（绑定域名后为 https://palace1689.com）
- 技术：Python + Flask 写页面，导出成纯静态网页，放在 Netlify 上

这份说明是写给接手维护网站的人的。从头读一遍，就能自己改文字、换图片、上线。

---

## 一、网站是怎么上线的（最重要）

```
你在电脑上改代码 ──推送──▶ GitHub 仓库 ──自动──▶ Netlify 生成网站并上线 ──▶ palace1689.com
```

- **代码** 存在 GitHub 组织的仓库里。
- **Netlify** 连着这个仓库。仓库一有新的提交，Netlify 就会自动运行 `python app.py build` 生成网站，一两分钟后上线。设置写在 `netlify.toml` 里，一般不用动。
- **域名** palace1689.com 绑定在 Netlify 上。

所以日常维护只需要：**改代码 → 本地预览确认 → 提交并推送到 GitHub**。不需要再手动把 `dist` 文件夹拖进 Netlify。

上线出问题时：在 Netlify 打开这个项目的 **Deploys** 页面，能看到每次上线的记录和报错；点之前任何一次成功的记录，再点 **Publish deploy**，就能立刻退回那个版本。

### 账号

网站相关账号都属于品牌，不属于个人：

| 账号 | 用途 |
| --- | --- |
| GitHub 组织 | 存代码。维护人员要被加进组织才能改代码 |
| Netlify（品牌邮箱注册） | 生成网站、上线、域名、HTTPS 证书 |
| 域名 palace1689.com | 在品牌的 Netlify 账号里购买，每年自动续费，扣绑定的卡 |

**交接时**：把新维护人加进 GitHub 组织并设为管理员，再把旧维护人移出；品牌邮箱的登录方式交给新的负责人。网站不用停。

**每年记得**：确认 Netlify 绑定的付款卡没过期。域名续费失败会导致网站打不开。

---

## 二、第一次在自己电脑上设置

需要装好 [Python 3](https://www.python.org/downloads/)（3.10 或更新）和 [GitHub Desktop](https://desktop.github.com/)。

1. 在 GitHub Desktop 里 **File → Clone repository**，选这个仓库，下载到电脑上。
2. 打开终端（Mac：应用程序 → 实用工具 → 终端），进入项目文件夹，运行：

```
python3 -m venv .venv                 # 建一个独立的 Python 环境（只需做一次）
source .venv/bin/activate             # 进入环境（Windows 用 .venv\Scripts\activate）
pip install -r requirements.txt       # 安装 Flask（只需做一次）
```

## 三、日常修改的流程

1. **进入环境并启动预览：**

```
source .venv/bin/activate
python app.py
```

2. 浏览器打开 http://127.0.0.1:5000 。改了文件后保存，刷新浏览器就能看到变化。终端里如果出现 “⚠ 缺少翻译” 的提示，说明某种语言少了对应的文字，暂时会显示简体中文。
3. 确认没问题后，在终端按 `Ctrl + C` 停止预览。
4. 打开 GitHub Desktop：左下角写一句改了什么（例如“更新英文品牌故事”），点 **Commit to main**，再点右上角 **Push origin**。
5. 一两分钟后，网站自动更新。

### 各页面地址（本地预览时）

其他语言在前面加语言代码，例如英文首页 `/en/`、英文宫廷折扇页 `/en/fans/`。语言代码：`zh-hant`、`en`、`ja`、`ko`、`es`、`fr`。

| 页面 | 地址 |
| --- | --- |
| 首页：一把大折扇，六片扇叶分别通向六个栏目（首页没有菜单栏） | http://127.0.0.1:5000/ |
| 品牌故事 | http://127.0.0.1:5000/story/ |
| 宫廷折扇：折扇介绍、签约大师、我们扇子的类别、折扇展示 | http://127.0.0.1:5000/fans/ |
| 手艺传承 | http://127.0.0.1:5000/craft/ |
| 资讯·动态 | http://127.0.0.1:5000/news/ |
| 往期主题 | http://127.0.0.1:5000/themes/ |
| 联系我们 | http://127.0.0.1:5000/contact/ |
| 所有大师 | http://127.0.0.1:5000/masters/ |
| 所有扇子类型 | http://127.0.0.1:5000/collections/ |

---

## 四、文件夹里有什么

| 文件 | 用途 |
| --- | --- |
| `content.py` | **所有语言共用**的设置：菜单顺序、照片、价格、日期、联系方式、网址 |
| `locales/zh_hans.py` 等 | **每种语言的文字**：菜单、标题、正文、按钮……一种语言一个文件 |
| `app.py` | 启动网站预览（`python app.py`）、导出网站（`python app.py build`） |
| `templates/index.html` | 网页结构 |
| `static/css/style.css` | 颜色、字体、大小、手机适配 |
| `static/js/main.js` | 折扇展开动画、下拉菜单、折扇展示的轮播和放大镜 |
| `static/images/` | 图片。`showcase/` 里是折扇展示的图，`pattern-cloud.svg` 是背景的暗金云纹 |
| `netlify.toml` | Netlify 自动生成网站的设置（生成命令、Python 版本） |
| `requirements.txt` | 网站需要的 Python 套件（只有 Flask） |
| `.gitignore` | 不上传到 GitHub 的文件（`dist/`、`.venv/` 等） |

`dist/` 和 `.venv/` 是在你电脑上自动生成的，不会上传到 GitHub，删了也没关系。

---

## 五、常见修改

**改文字**

- **改某种语言的文字：** 打开 `locales/` 里对应的文件，例如英文在 `locales/en.py`。每一项都是 `"名字": "文字"`，只改引号里面的文字，引号、逗号不要删。
- **改中文时别忘了其他六种语言：** 每种语言是单独的文件，改了简体中文，其他语言不会自动跟着变。
- **折扇介绍、品牌故事的正文：** 在各语言文件的 `HISTORY`（折扇介绍）和 `STORY`（品牌故事）里。`headline` 是正文最上面居中的标题，`motto` 是标题下的一句，`paragraphs` 是一段一段的正文，`pillars` 是结尾居中的几句短句，`coda` 是最后一段，`closing` 是结尾居中的一句。不需要的项删掉即可。
- **占位提示：** `HISTORY`、`CRAFT`、`STORY` 里的 `"placeholder"` 是 `True` 时，页面会显示“占位文字”提示；正文写好后改成 `False`。
- **首页扇叶上的字：** 就是各语言文件 `MENU` 里的菜单名。中文、日文竖排，其他语言沿扇叶方向排；字多时会自动缩小。

**改顺序、加内容**

- **菜单顺序：** `content.py` 的 `NAV`（首页扇叶从左到右的顺序，也是其他页面顶部菜单的顺序）、`FANS_MENU`（宫廷折扇页的区块和下拉菜单）。
- **折扇展示：**
  - 图片、大师、价格在 `content.py` 的 `SHOWCASE` 里。`master` 填大师的 id（例如 `"master3"`），会自动显示那位大师的名字；`price` 直接写要显示的文字，例如 `"¥ 28,000 起"`。
  - 扇名和简介在各语言文件的 `SHOWCASE` 里。
  - 加一把扇子：图片放进 `static/images/showcase/`，在 `content.py` 的 `SHOWCASE` 加一行，再到每个语言文件的 `SHOWCASE` 加上同一个 id。
  - 自动切换间隔：`content.py` 的 `SHOWCASE_SECONDS`。
- **大师和扇子类别：** 按 `content.py` 里的 `sort_name` 字母顺序自动排列。宫廷折扇页显示前 4 个，“所有大师”“所有扇子类型”页面显示全部。
- **资讯·动态：** 日期、配图、链接在 `content.py` 的 `NEWS` 里；标题和摘要在各语言文件的 `NEWS` 里。按日期从新到旧排列。
- **往期主题：** 配图、链接在 `content.py` 的 `THEMES` 里；名称和介绍在各语言文件的 `THEMES` 里。
- **联系方式：** `content.py` 的 `CONTACTS`，填一次，七种语言都会显示。

**图片**

- 放进 `static/images/` 对应的文件夹，用 `.jpg` 或 `.png`。iPhone 拍的 `.heic` 网页显示不了，要先转成 `.jpg`。
- 图片太大会让网站变慢。单张最好在 1 MB 以内，宽度 2000 像素左右就够了。

**外观**

- **颜色：** `static/css/style.css` 最上面 `:root` 里：`--plum-*` 是紫色系（主色 `#3D1F40`），`--gold` 是暗金，`--ink` 是正文颜色。改这里，整个网站一起变。
- **网址：** `content.py` 的 `SITE_URL`，填网站正式网址（绑定域名后改成 `https://palace1689.com`），用于告诉搜索引擎各语言版本的地址。

---

## 六、导出网站（一般不需要）

Netlify 会自动生成网站。只有想在自己电脑上检查导出结果时才需要：

```
python app.py build
```

生成的 `dist/` 里，首页是简体中文，其他语言在 `dist/en/`、`dist/ja/` 等子文件夹里。直接双击 `dist/index.html` 时页面之间的链接会打不开（电脑本地文件的限制），用 `python app.py` 预览或上线后一切正常。

---

## 七、尚未实现

- “定制”“详细信息”“前往定制”按钮还没有跳转目标；“查看全文”“查看主题”在 `content.py` 里填了 `link` 就能打开。
- logo 还是占位图，定稿后替换，并按 logo 调整颜色。
