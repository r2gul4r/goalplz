#!/usr/bin/env python3
"""Install Goalplz local marketplace, skill fallback, and prompt alias."""

from __future__ import annotations

import argparse
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


def check_repo(root: Path) -> list[str]:
    missing = []
    for rel in REQUIRED_REPO_FILES:
        if not (root / rel).is_file():
            missing.append(rel)
    return missing


def run_codex_marketplace_add(root: Path, codex_home: Path) -> int:
    codex = find_codex_cli(codex_home)
    if codex is None:
        print("[WARN] Codex CLI not found on PATH; skipped marketplace registration.")
        print(f"[INFO] Run manually: codex plugin marketplace add {root}")
        return 0

    try:
        result = subprocess.run(
            [codex, "plugin", "marketplace", "add", str(root)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
    except OSError as exc:
        print(f"[WARN] Could not run Codex CLI marketplace registration: {exc}")
        print(f"[INFO] Run manually if needed: codex plugin marketplace add {root}")
        return 1
    if result.stdout.strip():
        print(result.stdout.rstrip())
    if result.returncode != 0:
        print("[FAIL] Codex marketplace registration failed.")
    else:
        print("[OK] Codex marketplace registration command completed.")
    return result.returncode


def install_prompt(root: Path, codex_home: Path) -> None:
    source = root / "prompts" / "goalplz.md"
    target_dir = codex_home / "prompts"
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target_dir / "goalplz.md")
    print(f"[OK] Installed prompt alias: {target_dir / 'goalplz.md'}")


def install_compat_skill(root: Path, codex_home: Path) -> None:
    source = root / "plugins" / "goalplz" / "skills" / "goalplz"
    target = codex_home / "skills" / "goalplz"
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() or target.is_symlink():
        if target.is_dir() and not target.is_symlink():
            shutil.rmtree(target)
        else:
            target.unlink()
    shutil.copytree(source, target)
    print(f"[OK] Installed compatibility skill: {target}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Install Goalplz for Codex.")
    parser.add_argument("--codex-home", type=Path, default=default_codex_home())
    parser.add_argument("--skip-marketplace", action="store_true")
    parser.add_argument("--require-marketplace", action="store_true")
    parser.add_argument("--skip-compat-skill", action="store_true")
    parser.add_argument("--skip-prompt", action="store_true")
    args = parser.parse_args()

    root = repo_root()
    missing = check_repo(root)
    if missing:
        for rel in missing:
            print(f"[FAIL] Missing required file: {rel}")
        return 1

    print(f"[OK] Goalplz repository looks complete: {root}")

    if not args.skip_marketplace:
        code = run_codex_marketplace_add(root, args.codex_home.expanduser())
        if code != 0 and args.require_marketplace:
            return code
        if code != 0:
            print("[WARN] Continuing with compatibility skill and prompt alias install.")

    if not args.skip_compat_skill:
        install_compat_skill(root, args.codex_home.expanduser())

    if not args.skip_prompt:
        install_prompt(root, args.codex_home.expanduser())

    print("[OK] Install flow completed. Restart Codex or start a new thread.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
