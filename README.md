# My Resume

最新版本的 PDF 保存在仓库的 `out/resume.pdf`，并通过 GitHub Pages 在线展示。

- [下载 / 预览我的简历](out/resume.pdf)
- 在线浏览网址：`https://chappiewuzefan.github.io/MyResume/`

仓库结构说明：

- `resume.tex` 及 `cv/` 子目录包含 LaTeX 源文件；
- `fonts/` 存放使用的字体；
- `out/` 目录用于存放编译产物（PDF、synctex 等）。

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

## GitHub Pages 配置

1. 在仓库的 **Settings → Pages** 中，将 **Source** 设置为 `Deploy from a branch`，选择 `main` 分支、`/ (root)` 文件夹。
2. 保存后等待几分钟，GitHub 会自动构建静态站点，最终访问 `https://<你的用户名>.github.io/MyResume/` 即可在线查看简历。

> `index.html` 会自动嵌入 `out/resume.pdf`。只要同步更新 PDF 并推送，页面也会展示最新版本。
> 页面底部还集成了基于 GitHub Discussions 的留言板（Giscus）。访客可使用自己的 GitHub 账号留言，内容会同步到仓库的 Discussions。
