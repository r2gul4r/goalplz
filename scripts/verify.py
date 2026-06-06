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

COMPILER_CONTRACT_MARKERS = [
    "Goal Prompt Compiler",
    "READY_GOAL",
    "PLAN_FIRST",
    "NEEDS_TIGHTENING",
    "NOT_GOAL",
    "REFUSE",
    "route",
    "context",
    "provenance",
    "risk",
    "rollback",
    "pause_triggers",
    "evidence_log",
    "renderer",
    "approval",
    "non_goals",
]

READY_GOAL_RENDER_MARKERS = [
    "/goal",
    "Context:",
    "Scope:",
    "Constraints:",
    "Verification:",
    "Pause if:",
    "Done when:",
]

NON_READY_RENDER_MARKERS = [
    "REASON:",
    "BLOCKERS:",
    "PLAN_OR_QUESTIONS:",
    "QUALITY_CHECK:",
]

COMPILER_SCHEMA_KEYS = [
    "schema_version",
    "decision",
    "context",
    "provenance",
    "task",
    "scope",
    "verification",
    "risk",
    "constraints",
    "execution",
    "assumptions",
    "completion_conditions",
    "renderer",
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


def verify_markers(label: str, text: str, markers: list[str]) -> bool:
    normalized = text.lower()
    missing = [marker for marker in markers if marker.lower() not in normalized]
    if missing:
        fail(f"{label} is missing required template markers: {', '.join(missing)}")
        return False

    ok(f"{label} contains the compiler contract markers")
    return True


def verify_compiled_blocks(label: str, text: str) -> bool:
    blocks = re.findall(r"(?ms)^Compiled:\s*\n\s*```text\s*\n(.*?)\n```", text)
    if not blocks:
        fail(f"{label} does not contain any example Compiled blocks")
        return False

    success = True
    for index, block in enumerate(blocks, start=1):
        normalized = block.lower()
        missing = []
        if "status:" not in normalized:
            missing.append("STATUS:")
        if "route:" not in normalized:
            missing.append("ROUTE:")
        if "status: ready_goal" in normalized:
            missing.extend(
                marker
                for marker in READY_GOAL_RENDER_MARKERS
                if marker.lower() not in normalized
            )
        elif "status: plan_first" in normalized or "status: needs_tightening" in normalized:
            missing.extend(
                marker
                for marker in NON_READY_RENDER_MARKERS
                if marker.lower() not in normalized
            )
        if missing:
            fail(f"{label} Compiled block {index} is missing markers: {', '.join(missing)}")
            success = False

    if success:
        ok(f"{label} example Compiled blocks follow the compiler routes")

    return success


def verify_compiler_schema(label: str, text: str) -> bool:
    match = re.search(r"(?ms)^```json\s*\n(.*?)\n```", text)
    if not match:
        fail(f"{label} does not contain a compiler JSON schema block")
        return False

    try:
        schema = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        fail(f"{label} compiler JSON schema is invalid JSON: {exc}")
        return False

    missing = [key for key in COMPILER_SCHEMA_KEYS if key not in schema]
    if missing:
        fail(f"{label} compiler JSON schema is missing keys: {', '.join(missing)}")
        return False

    renderer = schema.get("renderer", {})
    if renderer.get("max_chars") != 4000 or renderer.get("overflow_strategy") != "write_contract_file":
        fail(f"{label} compiler JSON schema does not declare the expected renderer limit strategy")
        return False

    ok(f"{label} compiler JSON schema is valid")
    return True


def normalized_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore").replace("\r\n", "\n")


def verify_plugin_cache(root: Path, codex_home: Path) -> bool:
    plugin_json = root / "plugins/goalplz/.codex-plugin/plugin.json"
    try:
        version = json.loads(plugin_json.read_text(encoding="utf-8")).get("version")
    except Exception as exc:
        fail(f"Could not read plugin version from {plugin_json}: {exc}")
        return False
    if not version:
        fail(f"Plugin version missing from {plugin_json}")
        return False

    cache_root = codex_home / "plugins" / "cache" / "goalplz-local" / "goalplz" / version
    cache_skill = cache_root / "skills" / "goalplz" / "SKILL.md"
    cache_manifest = cache_root / ".codex-plugin" / "plugin.json"
    source_skill = root / "plugins" / "goalplz" / "skills" / "goalplz" / "SKILL.md"

    if not cache_skill.is_file() or not cache_manifest.is_file():
        fail(f"Installed plugin cache missing for {PLUGIN_SELECTOR} version {version}: {cache_root}")
        return False

    success = True
    if normalized_text(source_skill) == normalized_text(cache_skill):
        ok("Installed plugin cache skill matches repository skill")
    else:
        fail("Installed plugin cache skill differs from repository skill")
        success = False

    if normalized_text(plugin_json) == normalized_text(cache_manifest):
        ok("Installed plugin cache manifest matches repository manifest")
    else:
        fail("Installed plugin cache manifest differs from repository manifest")
        success = False

    return success


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
    elif "Goalplz: active" not in prompt or "STATUS:" not in prompt:
        fail("prompts/goalplz.md does not contain the self-contained goalplz workflow")
        success = False
    else:
        ok("Prompt alias is self-contained and does not route to $goalplz")

    patterns = (root / "plugins/goalplz/skills/goalplz/references/goal-patterns.md").read_text(encoding="utf-8")
    for label, text in [
        ("SKILL.md", skill),
        ("prompts/goalplz.md", prompt),
        ("goal-patterns.md", patterns),
    ]:
        success = verify_markers(label, text, COMPILER_CONTRACT_MARKERS) and success
    success = verify_compiler_schema("goal-patterns.md", patterns) and success
    success = verify_compiled_blocks("goal-patterns.md", patterns) and success

    return success


def verify_installed(
    root: Path,
    codex_home: Path,
    check_marketplace: bool,
    require_marketplace: bool,
    require_compat_skill: bool,
) -> bool:
    success = True
    plugin_enabled: bool | None = None

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
    else:
        codex = find_codex_cli(codex_home)
        if codex is None:
            message = "Codex CLI not found on PATH; cannot verify plugin installation"
            if require_marketplace:
                fail(message)
                return False
            warn(message)
        else:
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
            else:
                output = result.stdout or ""
                if result.returncode != 0:
                    message = "codex plugin list failed"
                    if require_marketplace:
                        fail(message)
                    else:
                        warn(message)
                    if output.strip():
                        print(output.rstrip())
                    if require_marketplace:
                        return False
                else:
                    matched_line = next(
                        (line for line in output.splitlines() if PLUGIN_SELECTOR in line),
                        "",
                    )
                    if not matched_line:
                        fail(f"Codex plugin list did not mention {PLUGIN_SELECTOR}")
                        print(output.rstrip())
                        success = False
                        plugin_enabled = False
                    else:
                        normalized = " ".join(matched_line.lower().split())
                        if "installed, enabled" in normalized:
                            ok(f"Codex plugin installed and enabled: {PLUGIN_SELECTOR}")
                            plugin_enabled = True
                            success = verify_plugin_cache(root, codex_home) and success
                        else:
                            fail(f"Codex plugin is not installed and enabled: {matched_line.strip()}")
                            success = False
                            plugin_enabled = False

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
        if plugin_enabled is True:
            warn("Compatibility skill is installed while the plugin is enabled; Codex may show duplicate Goalplz skill entries.")
    elif require_compat_skill or plugin_enabled is not True:
        fail(f"Installed compatibility skill missing: {installed_skill}")
        success = False
    else:
        ok("Compatibility skill is not installed; plugin provides the Goalplz skill without duplicate fallback.")

    return success


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Goalplz.")
    parser.add_argument("--installed", action="store_true", help="Also verify local Codex installation.")
    parser.add_argument("--skip-marketplace", action="store_true", help="Skip Codex CLI plugin installation check.")
    parser.add_argument("--require-marketplace", action="store_true", help="Fail if Codex plugin verification cannot run.")
    parser.add_argument("--require-compat-skill", action="store_true", help="Require the user-level compatibility skill fallback.")
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
            args.require_compat_skill,
        ) and success

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
