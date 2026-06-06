#!/usr/bin/env python3
"""Install Goalplz local marketplace, plugin, skill fallback, and prompt alias."""

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
MARKETPLACE_NAME = "goalplz-local"


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
            encoding="utf-8",
            errors="replace",
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


def run_codex_marketplace_remove(codex_home: Path) -> int:
    codex = find_codex_cli(codex_home)
    if codex is None:
        print("[WARN] Codex CLI not found on PATH; skipped marketplace removal.")
        return 1

    try:
        result = subprocess.run(
            [codex, "plugin", "marketplace", "remove", MARKETPLACE_NAME],
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
    except OSError as exc:
        print(f"[WARN] Could not run Codex CLI marketplace removal: {exc}")
        return 1
    if result.stdout.strip():
        print(result.stdout.rstrip())
    if result.returncode != 0:
        print("[WARN] Codex marketplace removal did not complete.")
    else:
        print("[OK] Removed existing Codex marketplace entry.")
    return result.returncode


def run_codex_plugin_add(codex_home: Path) -> int:
    codex = find_codex_cli(codex_home)
    if codex is None:
        print("[WARN] Codex CLI not found on PATH; skipped plugin installation.")
        print(f"[INFO] Run manually: codex plugin add {PLUGIN_SELECTOR}")
        return 0

    try:
        result = subprocess.run(
            [codex, "plugin", "add", PLUGIN_SELECTOR],
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
    except OSError as exc:
        print(f"[WARN] Could not run Codex plugin installation: {exc}")
        print(f"[INFO] Run manually if needed: codex plugin add {PLUGIN_SELECTOR}")
        return 1
    if result.stdout.strip():
        print(result.stdout.rstrip())
    if result.returncode != 0:
        print("[FAIL] Codex plugin installation failed.")
    else:
        print("[OK] Codex plugin installation command completed.")
    return result.returncode


def run_codex_plugin_remove(codex_home: Path) -> int:
    codex = find_codex_cli(codex_home)
    if codex is None:
        print("[WARN] Codex CLI not found on PATH; skipped plugin removal.")
        return 1

    try:
        result = subprocess.run(
            [codex, "plugin", "remove", PLUGIN_SELECTOR],
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
    except OSError as exc:
        print(f"[WARN] Could not run Codex plugin removal: {exc}")
        return 1
    if result.stdout.strip():
        print(result.stdout.rstrip())
    if result.returncode != 0:
        print("[WARN] Codex plugin removal did not complete.")
    else:
        print("[OK] Removed existing Codex plugin installation.")
    return result.returncode


def codex_plugin_enabled(codex_home: Path) -> bool | None:
    codex = find_codex_cli(codex_home)
    if codex is None:
        return None

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
    except OSError:
        return None
    if result.returncode != 0:
        return None

    matched_line = next(
        (line for line in (result.stdout or "").splitlines() if PLUGIN_SELECTOR in line),
        "",
    )
    if not matched_line:
        return False

    return "installed, enabled" in " ".join(matched_line.lower().split())


def normalized_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore").replace("\r\n", "\n")


def plugin_cache_current(root: Path, codex_home: Path) -> bool:
    plugin_json = root / "plugins" / "goalplz" / ".codex-plugin" / "plugin.json"
    try:
        version = json.loads(plugin_json.read_text(encoding="utf-8")).get("version")
    except Exception:
        return False
    if not version:
        return False

    cache_root = codex_home / "plugins" / "cache" / MARKETPLACE_NAME / "goalplz" / version
    cache_skill = cache_root / "skills" / "goalplz" / "SKILL.md"
    cache_manifest = cache_root / ".codex-plugin" / "plugin.json"
    source_skill = root / "plugins" / "goalplz" / "skills" / "goalplz" / "SKILL.md"
    if not cache_skill.is_file() or not cache_manifest.is_file():
        return False

    return (
        normalized_text(source_skill) == normalized_text(cache_skill)
        and normalized_text(plugin_json) == normalized_text(cache_manifest)
    )


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


def remove_compat_skill_if_owned(root: Path, codex_home: Path) -> None:
    target = codex_home / "skills" / "goalplz"
    if not target.exists() and not target.is_symlink():
        print("[OK] Compatibility skill is not installed; no duplicate skill entry.")
        return

    skill_file = target / "SKILL.md"
    source_file = root / "plugins" / "goalplz" / "skills" / "goalplz" / "SKILL.md"
    owned = False
    if skill_file.is_file():
        installed = skill_file.read_text(encoding="utf-8", errors="ignore")
        source = source_file.read_text(encoding="utf-8", errors="ignore")
        owned = installed == source or (
            "name: goalplz" in installed
            and "Goalplz" in installed
            and "/goalplz" in installed
        )

    if not owned:
        print(f"[WARN] Existing compatibility skill was not recognized as Goalplz; left unchanged: {target}")
        return

    if target.is_dir() and not target.is_symlink():
        shutil.rmtree(target)
    else:
        target.unlink()
    print(f"[OK] Removed compatibility skill to avoid duplicate Goalplz skill entries: {target}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Install Goalplz for Codex.")
    parser.add_argument("--codex-home", type=Path, default=default_codex_home())
    parser.add_argument("--skip-marketplace", action="store_true")
    parser.add_argument("--require-marketplace", action="store_true")
    parser.add_argument("--replace-marketplace", action="store_true")
    parser.add_argument("--skip-plugin", action="store_true")
    parser.add_argument("--require-plugin", action="store_true")
    parser.add_argument("--reinstall-plugin", action="store_true")
    parser.add_argument("--skip-compat-skill", action="store_true")
    parser.add_argument("--with-compat-skill", action="store_true")
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
        if args.replace_marketplace:
            run_codex_marketplace_remove(args.codex_home.expanduser())
        code = run_codex_marketplace_add(root, args.codex_home.expanduser())
        if code != 0 and args.require_marketplace:
            return code
        if code != 0:
            print("[WARN] Continuing with compatibility skill and prompt alias install.")

    if not args.skip_plugin:
        codex_home = args.codex_home.expanduser()
        if args.reinstall_plugin:
            run_codex_plugin_remove(codex_home)
        if codex_plugin_enabled(codex_home) is True and plugin_cache_current(root, codex_home):
            code = 0
            print("[OK] Codex plugin already installed and cache matches repository.")
        else:
            code = run_codex_plugin_add(codex_home)
        if code != 0 and (args.require_plugin or args.require_marketplace):
            return code
        if code != 0:
            print("[WARN] Continuing with compatibility skill and prompt alias install.")

    if not args.skip_compat_skill:
        plugin_enabled = codex_plugin_enabled(args.codex_home.expanduser())
        if args.with_compat_skill:
            install_compat_skill(root, args.codex_home.expanduser())
        elif plugin_enabled is True:
            remove_compat_skill_if_owned(root, args.codex_home.expanduser())
        else:
            print("[WARN] Codex plugin is not confirmed installed and enabled; installing compatibility skill fallback.")
            install_compat_skill(root, args.codex_home.expanduser())

    if not args.skip_prompt:
        install_prompt(root, args.codex_home.expanduser())

    print("[OK] Install flow completed. Restart Codex or start a new thread.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
