# Update Goalplz

Use this flow when the repository has changed and you want Codex to pick up the latest plugin files.

## Update the Repository

```bash
git pull
```

## Refresh Local Installation

Run the installer again:

```bash
python scripts/install.py
python scripts/verify.py --installed
```

If the Codex CLI is unavailable, skip marketplace refresh and verify installed files:

```bash
python scripts/install.py --skip-marketplace
python scripts/verify.py --installed --skip-marketplace
```

The installer overwrites only the Goalplz prompt alias at:

```text
${CODEX_HOME:-~/.codex}/prompts/goalplz.md
```

It also refreshes the compatibility skill at:

```text
${CODEX_HOME:-~/.codex}/skills/goalplz
```

It does not edit unrelated prompts, skills, repositories, or user instructions.

## Refresh Codex

Restart Codex or start a new thread after updating. If Codex keeps an older plugin snapshot, refresh the marketplace from Codex or run:

```bash
codex plugin marketplace upgrade goalplz-local
```

If your Codex installation uses a different marketplace name, inspect it first:

```bash
codex plugin marketplace list
```

## Verify Behavior

Check that `/goalplz` or `/prompts:goalplz` appears in your slash command list, then try:

```text
/goalplz convert this test failure into a goal but do not edit files
```

Expected behavior: Codex should use the Goalplz workflow to decide whether Goal mode is appropriate and produce or start a clear goal contract.
