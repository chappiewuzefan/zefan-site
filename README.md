# Zefan Wu — Personal Site

This repository powers <https://zefanwu.com/>. It bundles together:

1. **LaTeX resume** – all sources, fonts, class files, and build configuration.
2. **Interactive resume page** – embeds the PDF, shows site uptime, and includes a Giscus comment board.
3. **Jekyll blog + home page** – Markdown-driven content with custom layouts and styling.

Latest resume PDF: [`out/resume.pdf`](out/resume.pdf)

---

## Repository layout

### LaTeX resume

| Path / Item | Description |
| --- | --- |
| `resume.tex` | Primary LaTeX document that imports section partials from `cv/` and compiles to `out/resume.pdf`. |
| `cv/` | Individual section files (summary, experience, education, etc.) to keep edits modular. |
| `fonts/` | Font files bundled with the project so the PDF renders consistently. |
| `russell.cls` | Resume class defining typography, spacing, and section styling. |
| `latexmkrc` | Build configuration consumed by LaTeX Workshop (`latexmk -xelatex`, output to `out/`). |
| `out/` | Generated artifacts (`resume.pdf`, `.xdv`, `.synctex.gz`). The PDF is checked in for the web viewer. |

### Jekyll site

| Path / Item | Description |
| --- | --- |
| `_config.yml` | Site metadata, base URL, plugins (`jekyll-feed`, `jekyll-seo-tag`), permalink rules. |
| `_layouts/` | Layout templates: `default` (global shell + styles + icons), `page`, `post`, `blog`, `resume`. |
| `_posts/` | Markdown posts named `YYYY-MM-DD-title.md`. |
| `blog/index.md` | Blog landing page using the `blog` layout to list recent posts. |
| `index.md` | Landing page with a short intro and social links. |
| `resume.html` | Resume route that embeds `out/resume.pdf`, displays uptime, and mounts the Giscus message board. |
| `CNAME` | Custom domain mapping for GitHub Pages (`zefanwu.com`). |

### Tooling & automation

| Path / Item | Description |
| --- | --- |
| `Gemfile` | Ruby dependencies for local preview (`bundle exec jekyll serve`). |
| `package.json` | Node scripts and dev deps (`prettier`, `markdownlint-cli`). |
| `package-lock.json` | Locked versions of Node dependencies. |
| `.markdownlint.jsonc` / `.markdownlintignore` | Markdown lint rules & ignore list. |
| `.prettierrc.json` / `.prettierignore` | Prettier configuration & ignore list. |
| `.vscode/settings.json` | Workspace defaults: LaTeX output directory, format-on-save with Prettier for Markdown/JSON/YAML. |
| `.gitignore` | Keeps build artifacts (e.g., `node_modules/`, `_site/`, `out/`) and logs out of version control. |
| `profile.png` | Optional avatar referenced by the LaTeX class. |

---

## Resume workflow (VS Code)

- LaTeX Workshop runs `latexmk` automatically on save and writes artifacts to `out/`.
- Formatting is handled by `latexindent` (install its Perl dependencies to enable the integrated formatter).
- Edit the relevant `cv/*.tex` partials, save, and the PDF refreshes instantly.

To remove build artifacts, either use LaTeX Workshop’s “Clean up” command or run `latexmk -c` manually.

---

## Blog authoring

Create posts in `_posts/` with the standard Jekyll naming pattern:

```markdown
---
title: "Post Title"
tags: [tag-one, tag-two]
---

Content begins here. Markdown is fully supported.
```

Commit and push; GitHub Pages rebuilds automatically and the blog index is updated chronologically.

---

## Local preview

```bash
bundle config set --local path 'vendor/bundle'
bundle install
bundle exec jekyll serve
```

Visit <http://127.0.0.1:4000/> to preview the site locally (the PDF will render from `out/resume.pdf`).

---

## Linting & formatting

Install Node dev dependencies once:

```bash
npm install
```

Available scripts:

- `npm run lint:md` – run markdownlint (respects `.markdownlintignore`).
- `npm run format` – run Prettier on Markdown / JSON / YAML using `.prettierrc.json`.
- `npm run format:check` – verify formatting without writing changes (useful in CI).

VS Code’s workspace settings (see `.vscode/settings.json`) enable format-on-save for Markdown/JSON/YAML via Prettier—just hit save and formatting is applied automatically. LaTeX files continue to use LaTeX Workshop’s formatter.

---

## Deployment (GitHub Pages + Cloudflare)

1. GitHub Pages builds from `main` with the root folder (`/(root)`).
2. `CNAME` and `_config.yml` point the site to `https://zefanwu.com/`.
3. Cloudflare proxies the domain, providing HTTPS, caching, and Web Analytics (the beacon script lives in `_layouts/default.html`).

`resume.html` embeds the compiled PDF, displays an uptime counter, and mounts a Giscus message board (`data-term="Resume Message Board"`). Adjust the script if you change repository IDs or discussion categories.

---

## Message board

All comments are stored as GitHub Discussions through Giscus. Moderate them directly in the repository’s **Discussions** tab. Update the embed configuration in `resume.html` if you rename the discussion category or term.

---

## Contributing / Forking

Feel free to fork and adapt the LaTeX resume, Jekyll layouts, or automation setup. Pull requests and suggestions are welcome.
