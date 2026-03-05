---
name: resume-impact-tailor
description: Rewrite resume content from task lists into employer value statements. Use when improving HR screening conversion, converting technical bullets into problem-solution-impact language, reordering sections for a target role, or tailoring resume wording to a specific JD (including Chinese requests like "根据JD改简历" and "突出业务价值").
---

# Resume Impact Tailor

## Goal

Turn each resume line into a hiring-relevant claim:
1. Explain what problem was solved.
2. Explain what changed for the team or business.
3. Explain why the employer should pay for this capability.

## Inputs

- Current resume source files (for this repo, usually `cv/summary.tex`, `cv/experience.tex`, `cv/projects.tex`)
- Optional JD text file
- Optional role constraints (industry, level, location, visa, language)

## Workflow

### Step 1: Build an evidence inventory

For each bullet, extract:
- Situation/problem
- Action/decision
- Operational effect
- Business/people value

Drop bullets that only list tools without a result.

### Step 2: Rewrite with value translation

Apply the chain `动作 -> 作用 -> 可被购买能力`:
- 动作 (what you did)
- 作用 (what changed)
- 可被购买能力 (what future employer can rely on)

Prefer patterns like:
- `Solved [problem] by [approach], enabling [team/business outcome].`
- `Standardized [chaotic process] into [repeatable workflow], reducing [rework/risk/delay].`
- `Integrated [tool/system] into [existing process], turning [uncontrolled step] into [measurable step].`

### Step 3: Optimize for HR-first readability

- Put impact near the beginning of each line (first 8-12 words).
- Keep terms understandable for non-technical screeners.
- Keep one concise stack line per role; avoid repeated tool laundry lists.
- Keep strongest evidence first in each role.

### Step 4: Tailor to JD when provided

1. Extract top priorities from JD (responsibilities, must-haves, pain points).
2. Map existing evidence to each priority.
3. Rewrite and reorder bullets so top 3-5 JD priorities are visible quickly.
4. Preserve truthfulness; never invent metrics or ownership.

Run the built-in report script before editing:

```bash
.venv/bin/python skills/resume-impact-tailor/scripts/resume_signal_report.py \
  --resume cv/summary.tex \
  --resume cv/experience.tex \
  --jd /path/to/jd.txt \
  --out /tmp/resume-jd-report.md
```

If no JD is available, run without `--jd` to identify weak "task-only" bullets:

```bash
.venv/bin/python skills/resume-impact-tailor/scripts/resume_signal_report.py \
  --resume cv/summary.tex \
  --resume cv/experience.tex
```

### Step 5: Apply repo-specific edits

- Update LaTeX partials in `cv/`.
- Keep formatting compatible with `\item { ... }`.
- Rebuild resume PDF after edits:

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error -output-directory=out resume.tex
```

## Quality bar

- Use concrete outcomes (reliability, speed, risk, cost, delivery confidence, user impact).
- Keep claims defensible in interviews.
- Favor fewer strong bullets over many generic bullets.
- Use plain language first, technical detail second.

## Resources

- Rewrite guidance and examples: `references/rewrite-framework.md`
- Signal/JD analysis tool: `scripts/resume_signal_report.py`

### scripts/
- Use `resume_signal_report.py` to detect weak bullets and JD coverage gaps.

### references/
- Read `rewrite-framework.md` for transformation rules and rewrite templates.
