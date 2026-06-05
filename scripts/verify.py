#!/usr/bin/env python3
"""Verify Goalplz repository and optional local installation."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


REQUIRED_REPO_FILES = [
    ".agents/plugins/marketplace.json",
    "plugins/goalplz/.codex-plugin/plugin.json",
    "plugins/goalplz/skills/goalplz/SKILL.md",
    "plugins/goalplz/skills/goalplz/agents/openai.yaml",
    "plugins/goalplz/skills/goalplz/references/goal-patterns.md",
    "prompts/goalplz.md",
]

PLUGIN_SELECTOR = "goalplz@goalplz-local"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()


def find_codex_cli(codex_home: Path) -> str | None:
    env_path = os.environ.get("CODEX_CLI_PATH")
    if env_path and Path(env_path).is_file():
        return env_path

    config = codex_home / "config.toml"
    if config.is_file():
        match = re.search(
            r"(?m)^\s*CODEX_CLI_PATH\s*=\s*['\"]([^'\"]+)['\"]",
            config.read_text(encoding="utf-8", errors="ignore"),
        )
        if match and Path(match.group(1)).is_file():
            return match.group(1)

    return shutil.which("codex")


def ok(message: str) -> None:
    print(f"[OK] {message}")


def warn(message: str) -> None:
    print(f"[WARN] {message}")


def fail(message: str) -> None:
    print(f"[FAIL] {message}")


def verify_json(path: Path, expected_name: str | None = None) -> bool:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{path} is not valid JSON: {exc}")
        return False

    if expected_name and data.get("name") != expected_name:
        fail(f"{path} name is {data.get('name')!r}, expected {expected_name!r}")
        return False

    ok(f"Valid JSON: {path.relative_to(repo_root())}")
    return True


def verify_repo(root: Path) -> bool:
    success = True
    for rel in REQUIRED_REPO_FILES:
        path = root / rel
        if path.is_file():
            ok(f"Found {rel}")
        else:
            fail(f"Missing {rel}")
            success = False

    success = verify_json(root / ".agents/plugins/marketplace.json", "goalplz-local") and success
    success = verify_json(root / "plugins/goalplz/.codex-plugin/plugin.json", "goalplz") and success

    skill = (root / "plugins/goalplz/skills/goalplz/SKILL.md").read_text(encoding="utf-8")
    if "name: goalplz" not in skill or "/goalplz" not in skill:
        fail("SKILL.md does not advertise goalplz and /goalplz")
        success = False
    else:
        ok("SKILL.md advertises goalplz and /goalplz")

    prompt = (root / "prompts/goalplz.md").read_text(encoding="utf-8")
    if "$ARGUMENTS" not in prompt:
        fail("prompts/goalplz.md does not include slash command arguments")
        success = False
    else:
        ok("Prompt alias includes slash command arguments")

    if "$goalplz" in prompt:
        fail("prompts/goalplz.md still depends on $goalplz skill routing")
        success = False
    elif "Goalplz: active" not in prompt or "Goal fit:" not in prompt:
        fail("prompts/goalplz.md does not contain the self-contained goalplz workflow")
        success = False
    else:
        ok("Prompt alias is self-contained and does not route to $goalplz")

    return success


def verify_installed(root: Path, codex_home: Path, check_marketplace: bool, require_marketplace: bool) -> bool:
    success = True
    installed_skill = codex_home / "skills" / "goalplz" / "SKILL.md"
    if installed_skill.is_file():
        ok(f"Installed compatibility skill found: {installed_skill}")
        source = (root / "plugins/goalplz/skills/goalplz/SKILL.md").read_text(encoding="utf-8")
        installed = installed_skill.read_text(encoding="utf-8")
        if source == installed:
            ok("Installed compatibility skill matches repository skill")
        else:
            fail("Installed compatibility skill differs from repository skill")
            success = False
    else:
        fail(f"Installed compatibility skill missing: {installed_skill}")
        success = False

    installed_prompt = codex_home / "prompts" / "goalplz.md"
    if installed_prompt.is_file():
        ok(f"Installed prompt alias found: {installed_prompt}")
        source = (root / "prompts/goalplz.md").read_text(encoding="utf-8")
        installed = installed_prompt.read_text(encoding="utf-8")
        if source == installed:
            ok("Installed prompt alias matches repository prompt")
        else:
            fail("Installed prompt alias differs from repository prompt")
            success = False
    else:
        fail(f"Installed prompt alias missing: {installed_prompt}")
        success = False

    if not check_marketplace:
        ok("Skipped Codex plugin list check")
        return success

    codex = find_codex_cli(codex_home)
    if codex is None:
        message = "Codex CLI not found on PATH; cannot verify plugin installation"
        if require_marketplace:
            fail(message)
            return False
        warn(message)
        return success

    try:
        result = subprocess.run(
            [codex, "plugin", "list"],
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
    except OSError as exc:
        message = f"Could not run Codex CLI plugin list: {exc}"
        if require_marketplace:
            fail(message)
            return False
        warn(message)
        return success
    output = result.stdout or ""
    if result.returncode != 0:
        message = "codex plugin list failed"
        if require_marketplace:
            fail(message)
        else:
            warn(message)
        if output.strip():
            print(output.rstrip())
        return False if require_marketplace else success

    matched_line = next(
        (line for line in output.splitlines() if PLUGIN_SELECTOR in line),
        "",
    )
    if not matched_line:
        fail(f"Codex plugin list did not mention {PLUGIN_SELECTOR}")
        print(output.rstrip())
        return False

    normalized = " ".join(matched_line.lower().split())
    if "installed, enabled" in normalized:
        ok(f"Codex plugin installed and enabled: {PLUGIN_SELECTOR}")
    else:
        fail(f"Codex plugin is not installed and enabled: {matched_line.strip()}")
        success = False

    return success


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Goalplz.")
    parser.add_argument("--installed", action="store_true", help="Also verify local Codex installation.")
    parser.add_argument("--skip-marketplace", action="store_true", help="Skip Codex CLI plugin installation check.")
    parser.add_argument("--require-marketplace", action="store_true", help="Fail if Codex plugin verification cannot run.")
    parser.add_argument("--codex-home", type=Path, default=default_codex_home())
    args = parser.parse_args()

    root = repo_root()
    success = verify_repo(root)
    if args.installed:
        success = verify_installed(
            root,
            args.codex_home.expanduser(),
            not args.skip_marketplace,
            args.require_marketplace,
        ) and success

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
