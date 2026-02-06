#!/usr/bin/env python3
"""Lightweight spec-checker for repository.

Checks presence of key spec files and that skill interfaces mentioned
in the READMEs or specs exist as simple text signatures in code files.

Exits with code 0 on success, 1 on any failure.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

checks = []


def file_exists(p: Path):
    return p.exists()


def contains_text(p: Path, text: str):
    if not p.exists():
        return False
    try:
        data = p.read_text(encoding="utf-8")
    except Exception:
        return False
    return text in data


def main():
    failures = []

    # 1) Specs file present
    specs = ROOT / "specs" / "technical.md"
    checks.append((specs, "specs/technical.md exists", file_exists(specs)))

    # 2) Skills READMEs exist
    for skill in ["content_generator", "publisher", "trend_fetcher"]:
        r = ROOT / "skills" / skill / "README.md"
        checks.append((r, f"skills/{skill}/README.md exists", file_exists(r)))

    # 3) Trend fetcher implements fetch_trends signature (text search)
    tf_skill = ROOT / "skills" / "trend_fetcher" / "skill.py"
    checks.append((tf_skill, "trend_fetcher skill.py exists", file_exists(tf_skill)))
    checks.append((tf_skill, "trend_fetcher defines fetch_trends()",
                   contains_text(tf_skill, "def fetch_trends(")))

    # 4) Content generator README mentions `skill_content_generator`
    cg_readme = ROOT / "skills" / "content_generator" / "README.md"
    checks.append((cg_readme, "content_generator README documents skill_content_generator",
                   contains_text(cg_readme, "skill_content_generator")))

    # 5) Publisher README mentions `skill_publisher`
    pub_readme = ROOT / "skills" / "publisher" / "README.md"
    checks.append((pub_readme, "publisher README documents skill_publisher",
                   contains_text(pub_readme, "skill_publisher")))

    # Report
    print("Spec-check results:")
    for p, msg, ok in checks:
        status = "OK" if ok else "MISSING"
        print(f" - {msg}: {status}")
        if not ok:
            failures.append((p, msg))

    if failures:
        print("\nSpec check failed. Fix the missing items above.")
        sys.exit(1)
    else:
        print("\nAll spec checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
