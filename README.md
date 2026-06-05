<p align="right">
  English | <a href="./README.ko.md">한국어</a>
</p>

# Goalplz

Goalplz is a Codex plugin that turns rough requests into auditable Goal mode objectives.

It packages a reusable `$goalplz` skill and an optional `/goalplz` custom prompt alias.

## Why

Codex Goal mode works best when the objective has a concrete outcome, verification surface, constraints, boundaries, iteration policy, and blocked stop condition. Goalplz rewrites vague multi-step requests into that shape before Codex starts working.

## User-facing command

Preferred usage after installing the optional prompt alias:

```text
/goalplz fix the failing checkout tests and keep going until verified
```

Depending on your Codex surface, custom prompts may appear as:

```text
/prompts:goalplz fix the failing checkout tests and keep going until verified
```

Direct skill invocation also works:

```text
Use $goalplz to turn this request into a clear Codex goal and run it when appropriate: fix the failing checkout tests
```

## What it does

- Decides whether Goal mode is the right tool.
- Converts a rough request into an auditable completion contract.
- Captures outcome, verification surface, constraints, boundaries, iteration policy, and blocked stop condition.
- Starts a goal when the current Codex surface supports goal-management tools.
- Falls back to a ready-to-paste `/goal ...` command when direct goal creation is unavailable.

## Repository layout

```text
.agents/
  plugins/
    marketplace.json
plugins/
  goalplz/
    .codex-plugin/plugin.json
    skills/
      goalplz/
        SKILL.md
        agents/openai.yaml
        references/goal-patterns.md
prompts/
  goalplz.md
```

The plugin root is `plugins/goalplz`. The repository root is a local marketplace root for Codex.

## Install the plugin locally

From the repository root:

```bash
codex plugin marketplace add .
```

Then restart Codex and install `goalplz` from the `Goalplz Local` marketplace.

For a manual local marketplace, Codex reads:

```text
.agents/plugins/marketplace.json
```

That marketplace points to:

```text
./plugins/goalplz
```

## Install the `/goalplz` alias

Codex plugin manifests package skills, but custom prompt aliases are installed separately.

PowerShell:

```powershell
$promptDir = Join-Path $env:USERPROFILE ".codex\prompts"
New-Item -ItemType Directory -Force -Path $promptDir | Out-Null
Copy-Item -Force ".\prompts\goalplz.md" (Join-Path $promptDir "goalplz.md")
```

Bash:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/prompts"
cp ./prompts/goalplz.md "${CODEX_HOME:-$HOME/.codex}/prompts/goalplz.md"
```

Restart Codex or start a new thread if your surface does not pick up new prompts immediately.

## Validate

If you have the Codex skill-creator and plugin-creator utilities available, run:

```bash
python path/to/skill-creator/scripts/quick_validate.py ./plugins/goalplz/skills/goalplz
python path/to/plugin-creator/scripts/validate_plugin.py ./plugins/goalplz
```

## Source basis

The workflow follows public Codex guidance for Goal mode: use goals for persistent objectives with a clear evidence-based finish line, measurable completion criteria, constraints, boundaries, iteration behavior, and blocked stop conditions.

- OpenAI Developers Cookbook: https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex
- Codex manual, Goal mode: https://developers.openai.com/codex/codex-manual.md

## License

MIT
