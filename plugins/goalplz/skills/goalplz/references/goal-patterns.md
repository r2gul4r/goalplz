# Goal Patterns

Use these patterns after the `goalplz` workflow has triggered. Keep the final goal compact; do not paste every pattern unless it is useful.

## Compiler Contract v0.2

Goalplz is a goal prompt compiler. Its internal output should be stricter than the rendered `/goal` prompt. Use the internal contract to prevent invention, route unsafe work away from Goal mode, and verify that the final prompt is executable.

```json
{
  "schema_version": "0.2",
  "decision": {
    "status": "READY_GOAL | PLAN_FIRST | NEEDS_TIGHTENING | NOT_GOAL | REFUSE",
    "route": "render_goal | render_plan_first | ask_tightening_questions | render_normal_prompt | refuse",
    "confidence": "low | medium | high",
    "reasons": [],
    "blocking_gaps": [],
    "approval_gates": []
  },
  "context": {
    "raw_user_request": "",
    "user_supplied_context": [],
    "repo_context": {
      "target_paths": [],
      "mentioned_files": [],
      "issue_refs": [],
      "error_logs": [],
      "docs_to_read_first": []
    },
    "source_of_truth": [],
    "prompt_injection_notes": []
  },
  "provenance": {
    "outcome": "user | inferred_safe | policy_default | adapter_default | repo_discovered | needs_user",
    "verification": "user | inferred_safe | policy_default | adapter_default | repo_discovered | needs_user",
    "constraints": "user | inferred_safe | policy_default | adapter_default | repo_discovered | needs_user",
    "scope": "user | inferred_safe | policy_default | adapter_default | repo_discovered | needs_user",
    "risk": "user | inferred_safe | policy_default | adapter_default | repo_discovered | needs_user"
  },
  "task": {
    "outcome": "",
    "domains": {
      "primary": "debugging | performance | migration | research | ui | security | refactor | docs | unknown",
      "secondary": [],
      "adapters": {}
    }
  },
  "scope": {
    "allowed_changes": [],
    "non_goals": [],
    "off_limits": [],
    "change_budget": {
      "prefer_minimal_diff": true,
      "max_behavior_change": "none | minimal | moderate | broad | unknown"
    }
  },
  "verification": {
    "baseline": {
      "required": true,
      "commands": [],
      "expected_initial_state": ""
    },
    "fast_checks": [],
    "full_checks": [],
    "success_criteria": [],
    "manual_checks": []
  },
  "risk": {
    "level": "low | medium | high | blocked",
    "reasons": [],
    "external_effects": {
      "network": "none | read_only | write | unknown",
      "production_data": "none | read_only | write | unknown",
      "cost": "none | bounded | unbounded | unknown",
      "deployment": "none | staging | production | unknown"
    },
    "approval_required_before": [],
    "autonomy": "local_only | approval_gated | plan_only"
  },
  "constraints": {
    "must_preserve": [],
    "forbidden": [],
    "requires_approval": []
  },
  "execution": {
    "preflight": [],
    "iteration_rules": [],
    "pause_triggers": [],
    "rollback": {
      "strategy": "git_branch | worktree | patch_only | manual_backup | not_applicable",
      "must_keep_reversible": true
    },
    "evidence_log": {
      "progress_log_path": ".goalplz/progress.md",
      "must_record": []
    }
  },
  "assumptions": [
    {
      "text": "",
      "source": "user | inferred_safe | policy_default | adapter_default",
      "safety": "reversible | low_risk | approval_needed | unsafe",
      "confidence": "low | medium | high",
      "requires_user_confirmation": false
    }
  ],
  "completion_conditions": {
    "required": [],
    "artifacts": [],
    "remaining_risks": []
  },
  "renderer": {
    "target": "codex_goal",
    "format": "compact_markdown | contract_file",
    "max_chars": 4000,
    "overflow_strategy": "write_contract_file"
  }
}
```

## Route Policy

Use exactly one status and one route.

- `READY_GOAL` / `render_goal`: the work has one durable objective, bounded scope, safe autonomy boundaries, evidence-based completion, and enough context or safe local discovery.
- `PLAN_FIRST` / `render_plan_first`: the work may become a goal, but discovery, design, benchmark selection, architecture choices, migration planning, or source review must happen first.
- `NEEDS_TIGHTENING` / `ask_tightening_questions`: blocking information is missing and inventing it would change success, scope, acceptance, permissions, cost, data, external systems, or security posture.
- `NOT_GOAL` / `render_normal_prompt`: the request is a one-shot answer, simple explanation, small edit, or short review.
- `REFUSE` / `refuse`: the request is unsafe, unauthorized, destructive, credential-seeking, or disallowed.

Missing information has three classes:

- `soft missing`: safe to discover locally before editing, such as the relevant test command or project conventions.
- `hard missing`: success, acceptance, scope, or compatibility would be invented; ask at most three precise questions or route to `/plan`.
- `unsafe missing`: production writes, credentials, data deletion, auth/security posture, paid API use, deploys, external writes, or irreversible migrations are involved; require approval or refuse.

## Inference Rules

Infer only when all of these are true:

- The assumption is reversible.
- The work stays local or read-only.
- Existing behavior, security posture, data integrity, and tests are preserved.
- A check can prove the assumption wrong.
- The default matches repo or domain convention.
- A wrong assumption has low blast radius.

Never invent:

- success criteria, performance metrics, benchmark thresholds, or allowed tradeoffs
- research sources, datasets, target scores, compute budgets, or citation support
- production permissions, deployment approval, external writes, auth/security changes, paid API use, or destructive actions
- user-facing UI acceptance criteria without a reference surface

## Domain Adapters

Debugging:

- Reproduce before fixing.
- Record the baseline failure.
- Prefer the smallest root-cause-oriented change.
- Do not delete, skip, or weaken tests.
- Add regression coverage when reasonable.

Performance:

- Require metric, baseline, benchmark command or benchmark discovery, correctness checks, and allowed tradeoffs.
- If metric, target, benchmark, or correctness preservation is missing, use `PLAN_FIRST` or `NEEDS_TIGHTENING`.
- Record benchmark noise policy when measurements are unstable.

Migration:

- Require source stack, target stack, parity requirements, compatibility checks, rollout/legacy policy, and rollback or preservation strategy.
- Treat data migrations, auth changes, production writes, and irreversible steps as approval-gated.

Research/audit:

- Require source documents, claim inventory, evidence levels, unsupported-claim handling, and source limits.
- Require dataset, metric, target score, and compute budget when exact reproduction is requested.
- Do not describe proxy support as exact reproduction.

UI/prototype:

- Require reference surface, viewport matrix, visual evidence, interaction checks, and accessibility checks when relevant.
- Without a screenshot, Figma frame, route, mockup, or concrete source, use `NEEDS_TIGHTENING` or `PLAN_FIRST`.

Security:

- Require authorized scope, non-destructive validation, no exploit escalation, no secret exposure, and approval before auth, permission, network, or production-impacting changes.

Refactor/docs:

- Preserve behavior and public APIs.
- Keep diffs reviewable.
- Record non-goals.
- Require relevant tests, lint, typecheck, docs checks, or source evidence.

## Compact Goal Renderer Template

For `READY_GOAL`, render a compact Markdown contract rather than raw JSON. Translate labels to the user's language when appropriate, but preserve the structure.

```text
/goal <One durable objective>.

Context:
- <Source of truth and what to inspect first>

Scope:
- Allowed changes: <paths or areas>
- Non-goals: <explicitly out of scope>
- Off-limits: <paths, data, systems>

Constraints:
- Preserve <APIs, behavior, security, data, UX, tests>
- Do not <forbidden actions>
- Approval required before <gated actions>

Verification:
- Baseline: <what to establish before changes>
- Fast checks: <narrow checks>
- Full checks: <completion checks>
- Manual checks: <only when they complement executable checks>

Iteration:
- <Small checkpoint and one-hypothesis-at-a-time policy>
- <Evidence log requirement>

Pause if:
- <Approval, missing input, repeated blocker, risky scope expansion, or no defensible path>

Done when:
- <All required evidence supports the objective>
- <Artifacts and remaining risks are recorded>
```

If the rendered objective would be too long, use `renderer.format = contract_file` and a short `/goal` that references `.goalplz/goal-contract.md`.

## Fit Check

Good goal candidates:

- Debugging where the root cause is unknown.
- Performance work with benchmark or metric evidence.
- Flaky test reproduction and repair.
- Migration or refactor with compatibility constraints.
- Research, audit, or reproduction work where claims must be mapped to evidence.
- Multi-step implementation that needs tests or generated artifacts to prove completion.

Poor goal candidates:

- Simple explanation.
- One-line text or code edit.
- Short code review where findings are enough.
- Vague quality request such as "make it better" without success criteria.
- Human taste, product strategy, or business judgment as the main success condition.
- Risky external operation without explicit approval boundaries.

## Example: Failing Tests

Raw request:

```text
Fix the broken tests in this project.
```

Compiled:

```text
STATUS: READY_GOAL
ROUTE: render_goal

REASON:
The request has a durable debugging objective, safe local discovery path, and evidence-based completion.

ASSUMPTIONS:
- The relevant failing test command can be discovered from the repository. [source: inferred_safe; safety: reversible; confidence: medium; confirm: no]

COMPILED_GOAL:
/goal Reproduce the current failing test state, identify the root cause, and make the smallest defensible change so the reproduced failure passes.

Context:
- Inspect repository instructions, current git state, and the failing test output before editing.

Scope:
- Allowed changes: code and tests directly related to the reproduced failure.
- Non-goals: broad refactors, unrelated cleanup, dependency upgrades, or architecture changes.
- Off-limits: generated artifacts, lockfiles, and broad config unless evidence shows they are required.

Constraints:
- Preserve public API behavior unless evidence shows the API is the bug.
- Do not delete, skip, or weaken tests.
- Approval required before dependency installs, destructive git/filesystem actions, or external writes.

Verification:
- Baseline: run the narrowest relevant failing test before changes and record the failure.
- Fast checks: rerun that same test after each grounded fix.
- Full checks: run related tests or lint when the changed area makes that relevant.

Iteration:
- Use failure output to form one hypothesis at a time.
- Keep a short evidence log of commands, failures, fixes, and remaining risks.

Pause if:
- The failure cannot be reproduced, required dependencies or credentials are missing, or the only path is weakening validation.

Done when:
- The reproduced failure passes.
- Relevant follow-up checks pass or skipped checks are explained.
- Remaining risks are recorded.
```

## Example: Performance

Raw request:

```text
Make checkout faster.
```

Compiled:

```text
STATUS: PLAN_FIRST
ROUTE: render_plan_first

REASON:
The request is a plausible performance goal, but metric, threshold, benchmark, and allowed tradeoffs are missing.

BLOCKERS:
- Missing performance metric and target threshold.
- Missing benchmark or measurement source.
- Missing correctness checks and allowed tradeoffs.

PLAN_OR_QUESTIONS:
/plan Inspect the checkout performance path, identify measurable bottlenecks, propose a benchmark command or metric source, list correctness checks and tradeoffs that need approval, and draft a safe /goal. Do not change production behavior yet.

QUALITY_CHECK:
- The plan must produce a measurable metric, baseline, target, correctness checks, approval gates, and pause triggers before READY_GOAL.
```

## Example: Research Audit

Raw request:

```text
Reproduce this paper as much as possible.
```

Compiled:

```text
STATUS: NEEDS_TIGHTENING
ROUTE: ask_tightening_questions

REASON:
The request is a Goal mode candidate, but the source material and reproduction target are missing.

BLOCKERS:
- Missing paper, link, file, or source material.
- Missing reproduction target: code run, table/number reconstruction, model score, ablation, or audit report.
- Missing dataset, metric, compute budget, or accepted proxy level when exact reproduction is expected.

PLAN_OR_QUESTIONS:
1. Which paper, URL, file, or repository is the source of truth?
2. What counts as reproduction: code execution, result table reconstruction, model performance, ablation, or an evidence-backed audit?
3. What datasets, checkpoints, metrics, and compute budget are available?

QUALITY_CHECK:
- Do not render READY_GOAL until source documents, evidence levels, reproduction target, and blocked/proxy policy are explicit.
```

## Anti-Patterns

Weak:

```text
/goal Improve performance
```

Better:

```text
/goal Reduce p95 checkout latency below 120 ms on the checkout benchmark while keeping the checkout correctness suite green.
```

Weak:

```text
/goal Refactor this code
```

Better:

```text
/goal Extract the duplicated invoice formatting logic into a shared helper without changing generated invoice output, verified by the existing invoice snapshot tests and related unit tests.
```

Weak:

```text
/goal Do the backlog
```

Better:

Split into smaller goals, each with its own evidence surface, constraints, and blocked condition.

## Source Notes

This pattern is based on the public Codex guidance that Goal mode is best for persistent, evidence-checked objectives with clear completion criteria, constraints, boundaries, iteration policy, and blocked stop conditions.
