# My Resume

该仓库现在同时承载三块内容：LaTeX 简历源文件、在线简历页面（含留言板）、以及基于 Jekyll 的博客。

最新版本的 PDF 保存在 `out/resume.pdf`，并通过 GitHub Pages 在线展示。

- [下载 / 预览我的简历](out/resume.pdf)
- 在线浏览网址：`https://chappiewuzefan.github.io/MyResume/`

仓库结构说明：

- `resume.tex` 及 `cv/`：LaTeX 简历源文件；
- `fonts/`：简历字体；
- `out/`：LaTeX 编译产物（PDF、synctex 等）；
- `_layouts/`、`_posts/`、`_config.yml`：Jekyll 站点结构；
- `resume.html`：在线简历页（包含 PDF 预览与留言板）；
- `index.md`：博客首页，自动列出 `_posts` 下所有文章。

如果你希望复现编译：

```bash
latexmk -xelatex -synctex=1 -interaction=nonstopmode resume.tex
```

欢迎提出改进建议或直接 fork 使用模板。

## 本地编辑与自动编译

VS Code 安装了 LaTeX Workshop 插件，并配置为：

- 保存 `.tex` 文件时自动调用 `latexmk` 进行编译；
- 编译产物（PDF、synctex 等）输出到 `out/` 目录；
- 可选地调用 `latexindent` 进行格式化（需要满足依赖）。

因此只要修改任意 `*.tex` 文件并保存，VS Code 会立即出新 PDF。

## 撰写博客文章

Jekyll 会自动把 `_posts` 目录下的 Markdown 渲染成博客文章。新建文件时遵循 `YYYY-MM-DD-title.md` 命名，并写入以下模板：

```markdown
---
title: "文章标题"
tags: [标签1, 标签2]
---

正文内容，支持 Markdown 语法。
```

保存后 `git add`、`git commit`、`git push`，GitHub Pages 会自动重新构建；博客首页会显示最新文章。

## GitHub Pages 配置

1. 在仓库的 **Settings → Pages** 中，将 **Source** 设置为 `Deploy from a branch`，选择 `main` 分支、`/ (root)` 文件夹。
2. 保存后等待几分钟，GitHub 会自动构建静态站点，最终访问 `https://<你的用户名>.github.io/MyResume/` 即可在线查看简历。

> `resume.html` 会嵌入 `out/resume.pdf` 并展示留言板（Giscus）。只要同步更新 PDF 并推送，页面就会保持最新内容。留言会同步到仓库的 Discussions。
