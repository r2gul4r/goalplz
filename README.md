<p align="right">
  English | <a href="./README.ko.md">한국어</a>
</p>

# Goalplz

Goalplz is a Codex plugin that compiles rough requests into safe, scoped, verifiable Codex Goal mode prompts.

It packages a reusable `$goalplz` skill and an optional `/goalplz` custom prompt alias.

## Why

Codex Goal mode works best when the objective has a concrete outcome, verification surface, constraints, boundaries, iteration policy, and blocked stop condition. Goalplz does not merely fill a template: it first routes the request, builds a contract, then renders a Codex-ready `/goal`, `/plan`, tightening questions, normal prompt, or refusal.

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

- Decides whether Goal mode is the right tool and routes to `READY_GOAL`, `PLAN_FIRST`, `NEEDS_TIGHTENING`, `NOT_GOAL`, or `REFUSE`.
- Extracts outcome, context, provenance, scope, verification, risk, constraints, rollback, pause triggers, and completion conditions from rough input.
- Infers only safe, reversible gaps and never invents success criteria, permissions, external-system access, security posture, cost, or production impact.
- Renders `READY_GOAL` as a compact Markdown `/goal` contract.
- Routes unready requests to `/plan`, up to three blocking questions, a normal prompt, or refusal.
- Starts a goal when the current Codex surface supports goal-management tools, and falls back to a ready-to-paste command when direct goal creation is unavailable.

## Rough Prompt Conversion Test

On 2026-06-06, local mock fixtures were created under `test-fixtures/goalplz-realistic/` and dry-run converted against the current `prompts/goalplz.md` and `$goalplz` skill rules.

This test does not execute code changes or Goal mode. It checks what `/goal` prompt Goalplz renders when the user gives a rough request plus attached or targeted context.

Goalplz internally builds a contract with context, provenance, scope, verification, risk, pause triggers, and completion conditions. The final output does not have to be a fixed `Context:`, `Scope:`, `Verification:` template every time. If a compact prompt is enough, Goalplz renders a compact `/goal`; if the goal is too large, it can reference a separate contract file.

Goalplz keeps its internal schema, route/status values, and diagnostic wrapper keys in English, but renders user-facing prose in the dominant language of the request. An English request should produce English prose; a Korean request should produce Korean prose. Code, commands, paths, API names, and user-provided identifiers are preserved as written.

Fixtures:

- `test-fixtures/goalplz-realistic/checkout-failure.log`
- `test-fixtures/goalplz-realistic/checkout-performance-note.md`
- `test-fixtures/goalplz-realistic/mock-paper.md`
- `test-fixtures/goalplz-realistic/src/checkout/OrderSummary.tsx`
- `test-fixtures/goalplz-realistic/src/components/ProductCard.tsx`
- `test-fixtures/goalplz-realistic/assets/product-card-mobile-reference.svg`

### Test 1: Attached Failure Log

Input:

```text
/goalplz fix the broken test from the attached failure log

Attachment:
test-fixtures/goalplz-realistic/checkout-failure.log
```

Converted `/goal` prompt:

```text
/goal Use test-fixtures/goalplz-realistic/checkout-failure.log as the source of truth, reproduce the checkout test failure, identify the root cause, and make the smallest safe change so the failure passes. Do not delete, skip, or weaken tests. Run `npm test -- src/checkout/__tests__/applyCoupon.test.ts` before changes to record the baseline, then rerun the same test and related checkout checks after the fix. Pause and report if the failure cannot be reproduced or the only viable path weakens the test expectation.
```

### Test 2: Attached Performance Note

Input:

```text
/goalplz make checkout faster based on the attached performance note

Attachment:
test-fixtures/goalplz-realistic/checkout-performance-note.md
```

Converted `/goal` prompt:

```text
/goal Use test-fixtures/goalplz-realistic/checkout-performance-note.md as the source of truth to reduce checkout createOrder p95 from 410ms to <=250ms while preserving payment authorization behavior and order total calculation. Do not invent benchmark thresholds or change payment/order-total policy. Compare baseline and result with `npm run bench -- checkout`, then run `npm test -- src/checkout` and `npm run typecheck`. Pause and report if the benchmark cannot run, p95 cannot be compared, or meeting the target requires payment/order-total behavior changes.
```

### Test 3: Attached Paper

Input:

```text
/goalplz reproduce the attached paper, focusing on Table 2 first

Attachment:
test-fixtures/goalplz-realistic/mock-paper.md
```

Converted `/goal` prompt:

```text
/goal Use test-fixtures/goalplz-realistic/mock-paper.md as the source of truth to reproduce or audit TinyCache Table 2 and record results in reports/tinycache_table2_repro.md. Use the Table 2 F1, VRAM, Tokens/s values plus the reproduction notes dataset, metric, and command as the target. Run `python experiments/tinycache_eval.py --subset longbench_qa_tiny` when possible, and record a result-vs-paper comparison table, execution log, and missing conditions. If dataset, script, checkpoint, or compute constraints prevent exact reproduction, label the result as proxy evidence instead of exact reproduction.
```

### Test 4: Targeted Code File

Input:

```text
/goalplz clean up src/checkout/OrderSummary.tsx; it is messy; do not change behavior

Target file:
test-fixtures/goalplz-realistic/src/checkout/OrderSummary.tsx
```

Converted `/goal` prompt:

```text
/goal Refactor test-fixtures/goalplz-realistic/src/checkout/OrderSummary.tsx for readability without behavior changes. Preserve `OrderSummaryProps`, rendering semantics, and price calculation policy; do not add features, change design, alter public APIs, or rewrite checkout architecture. Limit edits to the target file and directly required adjacent helpers, run relevant test/lint/typecheck when available, and report the diff summary. Pause and report if behavior-preserving cleanup requires broader structural changes.
```

### Test 5: UI File And Reference Image

Input:

```text
/goalplz make ProductCard.tsx prettier on mobile using the attached screenshot

Attachment/target:
test-fixtures/goalplz-realistic/assets/product-card-mobile-reference.svg
test-fixtures/goalplz-realistic/src/components/ProductCard.tsx
```

Converted `/goal` prompt:

```text
/goal Use test-fixtures/goalplz-realistic/assets/product-card-mobile-reference.svg and test-fixtures/goalplz-realistic/src/components/ProductCard.tsx to improve the mobile ProductCard layout while preserving desktop behavior and existing data flow. Do not change the product data model, cart behavior, or the full design system. Check the 390x844 mobile viewport against the reference, verify desktop still works, confirm Add to cart interaction, no text overlap, and no image alt/accessibility regression, then record visual evidence and remaining tradeoffs. Pause and report if the reference conflicts with the existing component contract.
```

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

Quick install:

```bash
python scripts/install.py
python scripts/verify.py --installed
```

If the Codex CLI is unavailable, the installer still installs the compatibility skill and prompt alias. Use `--require-marketplace --require-plugin` when you want Codex plugin registration or installation failure to stop the install.

By default, the installer avoids duplicate Goalplz skill entries. If the Codex plugin is installed and enabled, it removes the user-level compatibility skill fallback. If the plugin cannot be confirmed, it installs the fallback. Use `--with-compat-skill` only for Codex surfaces that do not load plugin skills directly.

If `goalplz-local` is already registered from another repository path, run:

```bash
python scripts/install.py --replace-marketplace
```

If the plugin cache is stale or locked, run:

```bash
python scripts/install.py --reinstall-plugin
```

On Windows, the installer prefers `CODEX_CLI_PATH` from Codex config before the WindowsApps `codex` alias, which avoids common app-alias permission failures.

From the repository root:

```bash
codex plugin marketplace add .
codex plugin add goalplz@goalplz-local
```

Then restart Codex. `goalplz` should appear as an installed plugin from the `Goalplz Local` marketplace.

For a manual local marketplace, Codex reads:

```text
.agents/plugins/marketplace.json
```

That marketplace points to:

```text
./plugins/goalplz
```

The installer mirrors the skill to `${CODEX_HOME:-~/.codex}/skills/goalplz` only when the Codex plugin is not confirmed installed, or when `--with-compat-skill` is passed. Installing both the plugin skill and compatibility skill can make Goalplz appear twice in the skill picker.

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

For the full install flow, see [INSTALL.md](./INSTALL.md).

## Maintenance

- [INSTALL.md](./INSTALL.md): install and verify Goalplz locally.
- [UPDATE.md](./UPDATE.md): refresh an existing installation.
- [UNINSTALL.md](./UNINSTALL.md): remove the prompt alias, compatibility skill, and marketplace entry.
- [CONTRIBUTING.md](./CONTRIBUTING.md): contribution scope and checks.
- [SECURITY.md](./SECURITY.md): vulnerability reporting and security expectations.

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
