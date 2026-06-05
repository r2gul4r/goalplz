# Install Goalplz

This guide installs the local Codex plugin marketplace entry, the Goalplz plugin, and the optional `/goalplz` prompt alias.

## Requirements

- Codex CLI on `PATH` for plugin marketplace registration and plugin installation. Without it, Goalplz can still install the compatibility skill and prompt alias.
- Python 3.9+ for the helper scripts.
- A local clone of this repository.

## Quick Install

From the repository root:

```bash
python scripts/install.py
python scripts/verify.py --installed
```

The installer:

- Verifies the repository contains the expected plugin and prompt files.
- Runs `codex plugin marketplace add <repo-root>` when the Codex CLI is available.
- Runs `codex plugin add goalplz@goalplz-local` so the Goalplz skill appears in Codex's official skill list.
- Uses `CODEX_CLI_PATH` from the environment or `${CODEX_HOME:-~/.codex}/config.toml` before falling back to the `codex` command on `PATH`.
- Mirrors the skill into `${CODEX_HOME:-~/.codex}/skills/goalplz` as a compatibility fallback.
- Copies `prompts/goalplz.md` to `${CODEX_HOME:-~/.codex}/prompts/goalplz.md`.

Restart Codex or start a new thread after installation.

## Manual Install

Register this repository as a local plugin marketplace:

```bash
codex plugin marketplace add .
```

Then install the plugin from the `Goalplz Local` marketplace:

```bash
codex plugin add goalplz@goalplz-local
```

For compatibility with Codex environments that load user skills directly, copy the skill:

```bash
skill_dir="${CODEX_HOME:-$HOME/.codex}/skills/goalplz"
rm -rf "$skill_dir"
mkdir -p "$(dirname "$skill_dir")"
cp -R ./plugins/goalplz/skills/goalplz "$skill_dir"
```

PowerShell:

```powershell
$skillDest = Join-Path $env:USERPROFILE ".codex\skills\goalplz"
if (Test-Path $skillDest) {
    Remove-Item -Recurse -Force -LiteralPath $skillDest
}
New-Item -ItemType Directory -Force -Path (Split-Path $skillDest) | Out-Null
Copy-Item -Recurse -Force ".\plugins\goalplz\skills\goalplz" $skillDest
```

Install the optional `/goalplz` prompt alias:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/prompts"
cp ./prompts/goalplz.md "${CODEX_HOME:-$HOME/.codex}/prompts/goalplz.md"
```

PowerShell:

```powershell
$promptDir = Join-Path $env:USERPROFILE ".codex\prompts"
New-Item -ItemType Directory -Force -Path $promptDir | Out-Null
Copy-Item -Force ".\prompts\goalplz.md" (Join-Path $promptDir "goalplz.md")
```

## Verify

Validate repository structure:

```bash
python scripts/verify.py
```

Validate the installed compatibility skill, prompt alias, and Codex plugin status when available:

```bash
python scripts/verify.py --installed
```

If the Codex CLI is unavailable but you still want to verify the prompt alias and compatibility skill files:

```bash
python scripts/verify.py --installed --skip-marketplace
```

For strict plugin validation, require the Codex CLI checks:

```bash
python scripts/install.py --require-marketplace --require-plugin
python scripts/verify.py --installed --require-marketplace
```

Validate Codex skill/plugin schemas when the creator utilities are available:

```bash
python path/to/skill-creator/scripts/quick_validate.py ./plugins/goalplz/skills/goalplz
python path/to/plugin-creator/scripts/validate_plugin.py ./plugins/goalplz
```

## Use

After prompt alias installation:

```text
/goalplz fix the failing checkout tests and keep going until verified
```

Depending on the Codex surface, the prompt may appear as:

```text
/prompts:goalplz fix the failing checkout tests and keep going until verified
```

Direct skill invocation:

```text
Use $goalplz to turn this request into a clear Codex goal and run it when appropriate: fix the failing checkout tests
```
