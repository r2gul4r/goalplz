# Uninstall Goalplz

Use this flow to remove the optional prompt alias and detach the local marketplace entry.

## Remove the Prompt Alias

Bash:

```bash
rm -f "${CODEX_HOME:-$HOME/.codex}/prompts/goalplz.md"
```

PowerShell:

```powershell
$prompt = Join-Path $env:USERPROFILE ".codex\prompts\goalplz.md"
if (Test-Path $prompt) {
    Remove-Item -LiteralPath $prompt
}
```

This removes only the Goalplz prompt alias.

## Remove the Compatibility Skill

Bash:

```bash
rm -rf "${CODEX_HOME:-$HOME/.codex}/skills/goalplz"
```

PowerShell:

```powershell
$skill = Join-Path $env:USERPROFILE ".codex\skills\goalplz"
if (Test-Path $skill) {
    Remove-Item -Recurse -Force -LiteralPath $skill
}
```

This removes only the Goalplz compatibility skill directory.

## Remove the Marketplace Entry

Inspect configured marketplaces:

```bash
codex plugin marketplace list
```

Remove the Goalplz marketplace if it is listed as `goalplz-local`:

```bash
codex plugin marketplace remove goalplz-local
```

If your Codex installation recorded a different marketplace name, remove that name instead.

## Remove Installed Plugin

If the plugin is installed in the Codex app, remove it from the Plugins UI after removing or disabling the marketplace.

## Verify Removal

Restart Codex or start a new thread, then confirm `/goalplz`, `/prompts:goalplz`, and `$goalplz` are no longer available unless another installation source provides them.
