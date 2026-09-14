# 刘新宇 · 个人主页

> 长期个人档案：研究经历、完整论文列表、开源项目与随笔。
> **不是求职简历** —— 页面里没有会过期的措辞（比如「正在寻找 2027 校招机会」）。

技术栈：**Astro 5 + TypeScript**，纯静态输出，默认零客户端 JS。
选型依据见 `../demos/COMPARISON.md`（与 Hugo 的实测对比）。

## 快速开始

```bash
pnpm install
pnpm dev       # 开发服务器 → http://localhost:4321
pnpm build     # 构建到 dist/
pnpm preview   # 预览构建产物
```

> ⚠️ 本机运行需要 `ASTRO_TELEMETRY_DISABLED=1`（否则 Astro 会尝试写
> `~/Library/Preferences/astro`）。`pnpm build` 已在此环境下验证通过。

## 目录结构

```
site/
├── src/
│   ├── data/site.yaml          ★ 站点唯一数据源（论文/动态/项目/经历都在这）
│   ├── lib/site.ts             Zod schema —— 字段写错会在构建时报错
│   ├── content/writing/*.md    随笔（Markdown + frontmatter）
│   ├── layouts/Base.astro      HTML 骨架
│   ├── pages/
│   │   ├── index.astro         首页（Hero→News→Research→Publications→Projects→Writing→About）
│   │   └── writing/            随笔列表 + 详情
│   └── styles/style.css        亮色学术极简样式（6 个 token）
├── public/
│   ├── cv.pdf                  简历（下载入口）
│   ├── portrait.jpg            肖像照（已备好，当前未在页面使用）
│   └── favicon.svg
├── astro.config.mjs            ⚠️ 部署前改 site 为真实域名
├── verify.py                   内容/交互/链接的自动化验证 + 截图
└── .npmrc                      钉住 npm 官方源（本机默认镜像不可用）
```

## 改内容

**绝大多数改动只需要动一个文件：`src/data/site.yaml`。**

| 想改什么 | 改哪里 |
|---|---|
| 加一篇论文 | `publications` 加一条（`role` 只能是 `first-author` / `co-author`，`status` 只能是 `published` / `review`） |
| 加一条动态 | `news` |
| 加一个开源项目 | `projects`（`lang` / `stars` 目前取自 GitHub API，改时记得同步） |
| 改经历 | `timeline` |
| 改研究主线 | `research` |
| 改主页简介 | `author.bio`（支持内联 HTML，如 `<strong>`） |
| 加一篇随笔 | 新建 `src/content/writing/xxx.md`，需带 `title` / `date` / `excerpt` 三个 frontmatter 字段 |

写错字段名或漏字段，`pnpm build` 会直接报错并指出位置 —— 不会安静地渲染成空标签。

论文作者串里**自己的名字会自动加粗**（`src/lib/site.ts` 的 `highlightSelf`），
换名字只需要改 `author.name_en`。

## 部署（GitHub Pages）

仓库里已经有 `.github/workflows/deploy.yml` —— 推到 `main` 就会自动构建并发布。

**两种仓库模式，配置不同：**

| 模式 | 仓库名 | `astro.config.mjs` |
|---|---|---|
| **用户主页（推荐）** | `helldog-star.github.io` | `site: 'https://helldog-star.github.io'`，**不用**设 base |
| 项目主页 | 任意，如 `homepage` | `site: 'https://helldog-star.github.io/homepage'` **且** `base: '/homepage'` |

**步骤：**

1. 按上表改 `astro.config.mjs` 的 `site`（项目主页模式还要加 `base`）。
2. 在 GitHub 建一个**空**仓库（不要勾选 "Add a README"）。
3. 本地关联并推送：

   ```bash
   cd site
   git remote add origin git@github.com:helldog-star/<仓库名>.git
   git push -u origin main
   ```

4. 仓库 **Settings → Pages → Source** 选 **GitHub Actions**。
5. 之后每次 `git push` 都会自动重新构建部署。

**自定义域名**：Settings → Pages 里填 Custom domain，
并把 `astro.config.mjs` 的 `site` 改成那个域名。

**其他平台**：Vercel / Cloudflare Pages 直接连仓库，构建命令 `pnpm build`，输出目录 `dist`。

> 注意：`cv-project` 本身的 git remote 指向 `liantze/AltaCV`（模板仓库），
> 所以本目录已单独 `git init`，是独立仓库，不要从上层目录推。

## 验证

```bash
# 起本地服务后运行
python3 verify.py
```

会检查：论文条数与作者加粗、项目卡片、CV/favicon/图片可达性、
筛选交互（全部 8 / 一作 4 / 合作 4 / 在投 1），并截图到 `_shots/`。

## ⚠️ 待你确认的内容

| 项 | 说明 |
|---|---|
| **3 篇随笔** | `src/content/writing/` 下三篇是**我基于你的论文代写的草稿**，不是你的原话。请改写或替换，否则别直接部署。 |
| **肖像照** | `public/portrait.jpg` 已放好但未启用。想放照片告诉我，我加到 Hero 区。 |
| **域名** | `astro.config.mjs` 里还是占位 `xinyuliu.example`。 |
| **CV** | 用的是 `resume_lxy_v8.pdf`。更新简历后需重新拷到 `public/cv.pdf`。 |
| **OPRD 项目** | 你的 GitHub 上有这个 repo，但它关联的论文（arXiv:2606.06021）作者列表里**没有你**，所以只作为项目展示、未列入 Publications。 |
| **News 日期** | 用的是 arXiv 编号可推出的月份与 GitHub 仓库推送时间，非会议接收通知的确切日期。 |
