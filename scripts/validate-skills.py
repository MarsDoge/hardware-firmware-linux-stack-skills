#!/usr/bin/env python3
"""Validate the hardware-firmware-linux-stack-skills collection.

This intentionally avoids importing Hermes internals so the repository can be
validated in GitHub Actions and on machines that only have Python + PyYAML.
"""

from __future__ import annotations

import re
import stat
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_SKILL_CONTENT_CHARS = 100_000
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
FM_CLOSE_RE = re.compile(r"\n---\s*\n")
REQUIRED_HEADINGS = [
    "## Overview",
    "## When to Use",
    "## Verification Checklist",
]
PITFALL_HEADINGS = ("## Common Pitfalls", "## Pitfalls")
ALLOWED_SUPPORT_DIRS = {"references", "templates", "scripts", "assets"}


def fail(errors: list[str], path: Path, msg: str) -> None:
    errors.append(f"{path.relative_to(ROOT)}: {msg}")


def parse_frontmatter(path: Path, errors: list[str]) -> tuple[dict, str] | None:
    text = path.read_text(encoding="utf-8")
    if len(text) > MAX_SKILL_CONTENT_CHARS:
        fail(errors, path, f"file too large: {len(text)} > {MAX_SKILL_CONTENT_CHARS}")
    if not text.startswith("---"):
        fail(errors, path, "frontmatter must start at byte 0")
        return None
    match = FM_CLOSE_RE.search(text[3:])
    if not match:
        fail(errors, path, "missing closing frontmatter marker")
        return None
    raw_fm = text[3 : match.start() + 3]
    body = text[3:][match.end() :]
    try:
        fm = yaml.safe_load(raw_fm)
    except Exception as exc:  # pragma: no cover - diagnostic path
        fail(errors, path, f"frontmatter YAML parse failed: {exc}")
        return None
    if not isinstance(fm, dict):
        fail(errors, path, "frontmatter must be a mapping")
        return None
    return fm, body


def validate_skill(path: Path, all_skill_names: set[str], errors: list[str]) -> None:
    parsed = parse_frontmatter(path, errors)
    if not parsed:
        return
    fm, body = parsed
    skill_dir = path.parent
    expected_name = skill_dir.name

    name = fm.get("name")
    desc = fm.get("description")
    if not name:
        fail(errors, path, "missing name")
    elif name != expected_name:
        fail(errors, path, f"name {name!r} must match directory {expected_name!r}")
    elif len(name) > MAX_NAME_LENGTH or not NAME_RE.fullmatch(name):
        fail(errors, path, f"invalid skill name {name!r}")

    if not desc:
        fail(errors, path, "missing description")
    elif len(str(desc)) > MAX_DESCRIPTION_LENGTH:
        fail(errors, path, f"description too long: {len(str(desc))} > {MAX_DESCRIPTION_LENGTH}")
    elif not str(desc).startswith("Use when"):
        fail(errors, path, "description should start with 'Use when'")

    for key in ("version", "author", "license"):
        if not fm.get(key):
            fail(errors, path, f"missing recommended field {key}")

    hermes = fm.get("metadata", {}).get("hermes", {}) if isinstance(fm.get("metadata"), dict) else {}
    if not hermes.get("tags"):
        fail(errors, path, "metadata.hermes.tags missing/empty")

    related = hermes.get("related_skills", []) or []
    for rel in related:
        # Allow known external/user-local skills referenced by the router.
        if rel in {"uefi-firmware", "uefi-development", "systematic-debugging", "test-driven-development", "linux-desktop-apps", "codebase-inspection"}:
            continue
        if rel not in all_skill_names:
            fail(errors, path, f"related skill {rel!r} is not in this collection or allowlist")

    if not body.strip():
        fail(errors, path, "body is empty")
    for heading in REQUIRED_HEADINGS:
        if heading not in body:
            fail(errors, path, f"missing heading {heading}")
    if not any(heading in body for heading in PITFALL_HEADINGS):
        fail(errors, path, "missing pitfalls heading: expected '## Common Pitfalls' or '## Pitfalls'")

    support_refs = [m.group(1) for m in re.finditer(r"`((?:references|templates|scripts|assets)/[^`]+)`", body)]
    for rel in support_refs:
        target = skill_dir / rel
        if not target.exists():
            fail(errors, path, f"referenced support file missing: {rel}")

    for child in skill_dir.iterdir():
        if child.name == "SKILL.md":
            continue
        if child.is_dir() and child.name not in ALLOWED_SUPPORT_DIRS:
            fail(errors, child, "unexpected support directory")

    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists():
        for script in scripts_dir.glob("*.sh"):
            mode = script.stat().st_mode
            if not (mode & stat.S_IXUSR):
                fail(errors, script, "shell script should be executable")


def main() -> int:
    errors: list[str] = []
    if not SKILLS.exists():
        print("skills/ directory missing", file=sys.stderr)
        return 1

    skill_files = sorted(SKILLS.glob("*/SKILL.md"))
    if not skill_files:
        print("no skills/*/SKILL.md files found", file=sys.stderr)
        return 1

    all_skill_names = {p.parent.name for p in skill_files}
    for path in skill_files:
        validate_skill(path, all_skill_names, errors)

    if errors:
        print("Skill validation failed:\n", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1

    for path in skill_files:
        print(f"OK {path.relative_to(ROOT)}")
    print(f"Validated {len(skill_files)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
