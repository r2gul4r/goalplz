# Contributing

Thanks for improving Goalplz.

## Scope

Goalplz is intentionally narrow:

- Keep the core workflow focused on Codex Goal mode.
- Keep `SKILL.md` concise.
- Put long templates and examples in `references/goal-patterns.md`.
- Do not add multi-agent or non-Codex host support unless it has a clear maintenance plan.

## Development Checks

Run repository verification:

```bash
python scripts/verify.py
```

Run Codex schema checks when the creator utilities are available:

```bash
python path/to/skill-creator/scripts/quick_validate.py ./plugins/goalplz/skills/goalplz
python path/to/plugin-creator/scripts/validate_plugin.py ./plugins/goalplz
```

## Pull Requests

Prefer small PRs with:

- What changed.
- Why it changed.
- How it was verified.
- Any compatibility or installation risk.

Do not include secrets, tokens, private repository paths, or local machine-specific state in examples or fixtures.
