# Zefan Wu — Personal Site

This repository hosts three things in one place:

1. LaTeX sources and fonts for my resume.
2. An online resume page (with an embedded PDF and message board powered by Giscus).
3. A lightweight Jekyll blog built from Markdown posts.

Latest resume PDF: [`out/resume.pdf`](out/resume.pdf)  
Live site: <https://chappiewuzefan.github.io/zefan-site/>

---

## Project Layout

| Path | Purpose |
| --- | --- |
| `resume.tex`, `cv/` | LaTeX resume source files |
| `fonts/` | Custom fonts referenced by the resume |
| `out/` | LaTeX build artifacts (PDF, synctex, etc.) |
| `_layouts/`, `_posts/`, `_config.yml` | Jekyll templates and configuration |
| `resume.html` | Online resume page (PDF viewer + message board) |
| `index.md`, `blog/` | Blog index page and supporting files |
| `Gemfile` | Bundler dependencies for local Jekyll preview |

---

## Resume Workflow (VS Code)

- The LaTeX Workshop extension is configured to run `latexmk` automatically whenever `.tex` files are saved.
- Artifacts are written to the `out/` directory.
- Optional formatting via `latexindent` (install its Perl dependencies if needed).

This means updating the resume is as simple as editing the `.tex` files and hitting save; the PDF refreshes instantly.

---

## Writing Blog Posts

Jekyll consumes Markdown files in `_posts/` using the standard naming convention. Create a new post like this:

```markdown
---
title: "Post Title"
tags: [tag-one, tag-two]
---

Content begins here. Markdown is fully supported.
```

Commit and push the post and GitHub Pages will rebuild the site automatically. The blog index lists posts chronologically.

---

## Local Preview (optional)

If you want to preview everything locally, install the Ruby dependencies into `vendor/bundle` and run Jekyll:

```bash
bundle config set --local path 'vendor/bundle'
bundle install
bundle exec jekyll serve
```

Then browse to <http://127.0.0.1:4000/zefan-site/>.

---

## GitHub Pages Deployment

1. In **Settings → Pages**, set the source to `Deploy from a branch`, branch `main`, folder `/ (root)`.
2. Every push triggers a new Jekyll build. The production site is served from <https://chappiewuzefan.github.io/zefan-site/>.

`resume.html` embeds the compiled PDF, shows a running site uptime label, and exposes a “Resume Message Board”. Messages are stored as GitHub Discussions under the repository. Visitor statistics are collected via [Busuanzi](https://busuanzi.ibruce.info/) and displayed in the footer.

---

## Message Board / Discussions

Giscus uses Discussions to store comments. The embed on `resume.html` is configured with `data-term="Resume Message Board"`; adjust that value if you ever rename the section.

---

## Contributing / Forking

Feel free to fork the project, adapt the LaTeX template, or use the Jekyll setup as a starting point for your own personal site. Pull requests and suggestions are welcome.
