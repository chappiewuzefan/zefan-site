#!/usr/bin/env python3
"""Generate a resume impact report and optional JD alignment report."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re
from typing import Iterable


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "this",
    "to",
    "using",
    "with",
    "within",
    "across",
    "through",
    "over",
    "under",
    "our",
    "your",
    "you",
    "we",
    "will",
    "can",
    "should",
    "must",
    "required",
    "requirement",
    "preferred",
    "experience",
    "years",
}

ACTION_VERBS = {
    "architected",
    "automated",
    "built",
    "collaborated",
    "configured",
    "created",
    "delivered",
    "designed",
    "developed",
    "documented",
    "enabled",
    "engineered",
    "implemented",
    "improved",
    "integrated",
    "led",
    "maintained",
    "managed",
    "migrated",
    "optimized",
    "planned",
    "partnered",
    "refactored",
    "resolved",
    "scaled",
    "served",
    "streamlined",
    "supported",
    "tested",
    "translated",
    "troubleshot",
    "worked",
    "upgraded",
    "introduced",
    "containerized",
    "conducted",
    "synthesized",
}

OUTCOME_TERMS = {
    "decrease",
    "decreased",
    "faster",
    "improve",
    "improved",
    "increase",
    "increased",
    "optimize",
    "optimized",
    "reduced",
    "reliable",
    "reliability",
    "saved",
    "stability",
    "streamlined",
    "uptime",
}

VALUE_TERMS = {
    "accuracy",
    "cost",
    "customer",
    "delivery",
    "efficiency",
    "manual",
    "operations",
    "performance",
    "productivity",
    "quality",
    "risk",
    "scalable",
    "sla",
    "stakeholder",
    "team",
    "user",
    "workflow",
}

TECH_SHORT_TOKENS = {"api", "aws", "ci", "cd", "gcp", "gpu", "iot", "ml", "nlp", "sql"}

JD_PRIORITY_PATTERN = re.compile(
    r"\b(must|required|requirements?|responsibilit(?:y|ies)|need|expect|ability|proficient|preferred)\b",
    re.IGNORECASE,
)


@dataclass
class BulletAnalysis:
    source: str
    text: str
    score: int
    missing: list[str]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def tex_items(text: str) -> list[str]:
    items: list[str] = []
    i = 0
    token = r"\item"
    while True:
        idx = text.find(token, i)
        if idx == -1:
            break
        j = idx + len(token)
        while j < len(text) and text[j].isspace():
            j += 1
        if j >= len(text) or text[j] != "{":
            i = j
            continue
        j += 1
        depth = 1
        start = j
        while j < len(text) and depth > 0:
            ch = text[j]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            j += 1
        if depth == 0:
            item = text[start : j - 1].strip()
            if item:
                items.append(item)
        i = j
    return items


def strip_tex_comments(text: str) -> str:
    cleaned_lines: list[str] = []
    for line in text.splitlines():
        if line.lstrip().startswith("%"):
            continue
        chars: list[str] = []
        i = 0
        while i < len(line):
            ch = line[i]
            if ch == "%" and (i == 0 or line[i - 1] != "\\"):
                break
            chars.append(ch)
            i += 1
        cleaned_lines.append("".join(chars))
    return "\n".join(cleaned_lines)


def plain_statements(text: str) -> list[str]:
    raw = re.split(r"[\n.;]", text)
    statements = []
    for line in raw:
        stripped = line.strip()
        if not stripped or stripped.startswith("%"):
            continue
        cleaned = latex_to_text(line).strip()
        if re.fullmatch(r"[-_]{6,}", cleaned):
            continue
        if not re.search(r"[A-Za-z]", cleaned):
            continue
        if len(cleaned) >= 35:
            statements.append(cleaned)
    return statements


def latex_to_text(text: str) -> str:
    output = text
    for _ in range(5):
        previous = output
        output = re.sub(r"\\textbf\{([^{}]*)\}", r"\1", output)
        output = re.sub(r"\\emph\{([^{}]*)\}", r"\1", output)
        output = re.sub(r"\\url\{([^{}]*)\}", r"\1", output)
        if output == previous:
            break
    output = output.replace(r"\&", " and ")
    output = output.replace(r"\%", "%")
    output = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", " ", output)
    output = re.sub(r"[{}]", " ", output)
    output = re.sub(r"\s+", " ", output)
    return output.strip()


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z][a-zA-Z0-9+#./-]*", text.lower())


def analyze_statement(source: str, statement: str) -> BulletAnalysis:
    text = latex_to_text(statement)
    text_lower = text.lower()
    tokens = set(tokenize(text))

    has_action = bool(tokens & ACTION_VERBS)
    has_outcome = bool(tokens & OUTCOME_TERMS) or bool(re.search(r"\d|%", text_lower))
    has_value = bool(tokens & VALUE_TERMS)

    score = int(has_action) + int(has_outcome) + int(has_value)
    missing: list[str] = []
    if not has_action:
        missing.append("clear action")
    if not has_outcome:
        missing.append("observable outcome")
    if not has_value:
        missing.append("employer value")

    # Tool-list lines are usually weak for HR screening unless attached to impact.
    if "technical skills:" in text_lower and score > 1:
        score = 1
        missing = ["business context", "outcome"]

    return BulletAnalysis(source=source, text=text, score=score, missing=missing)


def extract_jd_keywords(jd_text: str, top_n: int) -> list[tuple[str, int]]:
    counts: Counter[str] = Counter()
    tokens = re.findall(r"[A-Za-z][A-Za-z0-9+#/-]{1,}", jd_text)
    for raw in tokens:
        token = raw.lower().strip(".,:;()[]{}")
        if token in STOPWORDS:
            continue
        if len(token) >= 4 or token in TECH_SHORT_TOKENS:
            counts[token] += 1
    return counts.most_common(top_n)


def extract_priority_lines(jd_text: str, limit: int = 8) -> list[str]:
    lines = [line.strip() for line in jd_text.splitlines() if line.strip()]
    selected = [line for line in lines if JD_PRIORITY_PATTERN.search(line)]
    return selected[:limit]


def escape_pipe(text: str) -> str:
    return text.replace("|", "\\|")


def truncate(text: str, length: int = 120) -> str:
    if len(text) <= length:
        return text
    return text[: length - 3] + "..."


def build_report(
    resume_paths: Iterable[Path], analyses: list[BulletAnalysis], jd_text: str | None, top_n: int
) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    weak = [item for item in analyses if item.score <= 1]
    moderate = [item for item in analyses if item.score == 2]
    strong = [item for item in analyses if item.score == 3]

    lines: list[str] = []
    lines.append("# Resume Signal Report")
    lines.append("")
    lines.append(f"- Generated: {now}")
    lines.append(f"- Resume files: {', '.join(str(path) for path in resume_paths)}")
    lines.append(f"- Statements analyzed: {len(analyses)}")
    lines.append(f"- Strength split: strong={len(strong)}, moderate={len(moderate)}, weak={len(weak)}")
    lines.append("")

    lines.append("## Weak or generic statements")
    if not weak:
        lines.append("")
        lines.append("- None detected.")
    else:
        lines.append("")
        lines.append("| # | Source | Score | Missing | Statement |")
        lines.append("|---|---|---:|---|---|")
        for idx, item in enumerate(weak[:15], start=1):
            missing = ", ".join(item.missing) if item.missing else "-"
            lines.append(
                f"| {idx} | {escape_pipe(item.source)} | {item.score} | "
                f"{escape_pipe(missing)} | {escape_pipe(truncate(item.text))} |"
            )

    lines.append("")
    lines.append("## Rewrite patterns to apply")
    lines.append("")
    lines.append("- Solve [problem] by [approach], enabling [team/business outcome].")
    lines.append("- Turn [manual or chaotic step] into [repeatable workflow], reducing [risk/rework/delay].")
    lines.append("- Integrate [tool/system] into [existing process] so [stakeholder] can [result].")

    if jd_text:
        resume_text = "\n".join(item.text for item in analyses).lower()
        keywords = extract_jd_keywords(jd_text, top_n)
        missing_keywords = [word for word, _count in keywords if word not in resume_text]

        lines.append("")
        lines.append("## JD alignment")
        lines.append("")
        lines.append("| JD keyword | Frequency | Covered in resume |")
        lines.append("|---|---:|---|")
        for word, count in keywords[: min(top_n, 20)]:
            covered = "yes" if word in resume_text else "no"
            lines.append(f"| {word} | {count} | {covered} |")

        lines.append("")
        lines.append("### Missing high-priority JD signals")
        lines.append("")
        if missing_keywords:
            for word in missing_keywords[:12]:
                lines.append(f"- {word}")
        else:
            lines.append("- No obvious keyword gaps detected.")

        priority_lines = extract_priority_lines(jd_text)
        lines.append("")
        lines.append("### Priority JD lines to map against your evidence")
        lines.append("")
        if priority_lines:
            for line in priority_lines:
                lines.append(f"- {line}")
        else:
            lines.append("- No explicit requirement lines matched the priority pattern.")

    lines.append("")
    lines.append("## Next editing move")
    lines.append("")
    lines.append(
        "- Rewrite weak statements first, then reorder each role so the strongest role-relevant evidence appears in the first 2-3 bullets."
    )
    return "\n".join(lines) + "\n"


def collect_statements(path: Path) -> list[str]:
    text = read_text(path)
    if path.suffix.lower() == ".tex":
        items = tex_items(strip_tex_comments(text))
        if items:
            return items
    return plain_statements(strip_tex_comments(text))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze resume signals and optional JD alignment from resume source files."
    )
    parser.add_argument(
        "--resume",
        action="append",
        required=True,
        help="Resume source file path. Repeat this flag for multiple files.",
    )
    parser.add_argument("--jd", help="Optional JD text file for keyword alignment.")
    parser.add_argument("--top", type=int, default=20, help="Number of JD keywords to inspect.")
    parser.add_argument("--out", help="Optional output markdown path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    resume_paths = [Path(path).resolve() for path in args.resume]

    analyses: list[BulletAnalysis] = []
    for path in resume_paths:
        if not path.exists():
            raise FileNotFoundError(f"Resume file not found: {path}")
        for statement in collect_statements(path):
            analyses.append(analyze_statement(path.name, statement))

    jd_text: str | None = None
    if args.jd:
        jd_path = Path(args.jd).resolve()
        if not jd_path.exists():
            raise FileNotFoundError(f"JD file not found: {jd_path}")
        jd_text = read_text(jd_path)

    report = build_report(resume_paths=resume_paths, analyses=analyses, jd_text=jd_text, top_n=args.top)

    if args.out:
        out_path = Path(args.out).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8")
        print(f"Wrote report to {out_path}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
