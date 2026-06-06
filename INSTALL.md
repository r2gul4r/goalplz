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
- Mirrors the skill into `${CODEX_HOME:-~/.codex}/skills/goalplz` only when the Codex plugin is not confirmed installed and enabled.
- Removes the compatibility skill when the plugin is installed and enabled, preventing duplicate Goalplz skill entries.
- Copies `prompts/goalplz.md` to `${CODEX_HOME:-~/.codex}/prompts/goalplz.md`.

Restart Codex or start a new thread after installation.

If `goalplz-local` is already registered from another clone or Codex worktree, refresh the marketplace path:

```bash
python scripts/install.py --replace-marketplace
```

If the plugin cache is stale or locked, force a remove/add cycle:

```bash
python scripts/install.py --reinstall-plugin
```

If your Codex surface cannot load plugin skills directly and needs a user-level fallback, force that fallback:

```bash
python scripts/install.py --with-compat-skill
```

## Manual Install

Register this repository as a local plugin marketplace:

```bash
codex plugin marketplace add .
```

Then install the plugin from the `Goalplz Local` marketplace:

```bash
codex plugin add goalplz@goalplz-local
```

For compatibility with Codex environments that load user skills directly, copy the skill. Do this only when the plugin skill is not available; installing both can show duplicate Goalplz skill entries.

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

Validate the prompt alias, Codex plugin status, and compatibility fallback when needed:

```bash
python scripts/verify.py --installed
```

If the Codex CLI is unavailable but you still want to verify the prompt alias and compatibility skill files:

```bash
python scripts/verify.py --installed --skip-marketplace
```

If you intentionally installed the user-level fallback, require it during verification:

```bash
python scripts/verify.py --installed --require-compat-skill
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
