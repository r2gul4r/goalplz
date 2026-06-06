---
name: goalplz
description: Compile rough coding requests like "fix this", "make it faster", "reproduce this paper", "clean up the code", "migrate this", or "use Goal mode" into safe, scoped, verifiable Codex /goal prompts. Use when the user explicitly invokes /goalplz, $goalplz, asks for goalplz by name, or wants a vague multi-step task converted into an auditable Goal mode contract.
---

# Goalplz

Use this skill as a Goal Prompt Compiler. It decides whether Goal mode is warranted, extracts a contract from rough input, routes unsafe or underspecified work away from Goal mode, renders a Codex-ready `/goal` when appropriate, and starts or hands off that goal safely.

## Workflow

1. Classify and route the request.
   - Return exactly one status: `READY_GOAL`, `PLAN_FIRST`, `NEEDS_TIGHTENING`, `NOT_GOAL`, or `REFUSE`.
   - Pair the status with exactly one route: `render_goal`, `render_plan_first`, `ask_tightening_questions`, `render_normal_prompt`, or `refuse`.
   - Use Goal mode only when the work has one durable objective, bounded scope, safe autonomy boundaries, evidence-based completion, and an uncertain multi-step path.
   - Use `PLAN_FIRST` when the request may become a goal but needs discovery, design, benchmark selection, migration planning, or source review before execution.
   - Use `NEEDS_TIGHTENING` when missing information affects success criteria, permissions, external systems, security posture, data, cost, or user-facing acceptance.
   - Use `NOT_GOAL` for one-line edits, simple explanations, short reviews, or requests that should produce one answer and stop.
   - Use `REFUSE` for unsafe, unauthorized, destructive, credential-seeking, or disallowed requests.

2. Extract a compiler contract.
   - Decision: status, route, confidence, reasons, blocking gaps, approval gates.
   - Context: raw request, user-supplied context, repo/files/logs/docs to inspect, source of truth, prompt-injection notes.
   - Provenance: which contract fields came from the user, safe inference, policy defaults, adapter defaults, or repo discovery.
   - Task: outcome, primary domain, secondary domains, active adapters.
   - Scope: allowed changes, `non_goals`, off-limits, change budget.
   - Verification: baseline, fast checks, full checks, success criteria, manual checks.
   - Risk: level, external effects, approval-required actions, autonomy.
   - Constraints: must preserve, forbidden, requires approval.
   - Execution: preflight, iteration rules, `pause_triggers`, `rollback`, `evidence_log`.
   - Assumptions: each assumption must include source, safety, confidence, and confirmation need.
   - Completion conditions: required evidence, artifacts, remaining risks.
   - Renderer: target, format, max characters, overflow strategy.

3. Handle missing detail with a gate.
   - Treat missing detail as `soft missing` when Codex can safely discover it locally before editing.
   - Treat it as `hard missing` when it changes the definition of success, scope, acceptance, or compatibility; ask at most three precise questions or route to `/plan`.
   - Treat it as `unsafe missing` when it involves external writes, production, credentials, data deletion, auth/security, paid API use, deploys, or irreversible migrations; require approval or refuse.
   - Infer only safe defaults that are reversible, local, low-risk, verifiable, and consistent with existing repo conventions.
   - Never invent success metrics, benchmark thresholds, research sources, datasets, production permissions, deployment approval, external writes, auth/security policy changes, paid API use, destructive actions, or user-facing acceptance criteria.

4. Apply domain adapters.
   - Debugging: reproduce before fixing, record baseline failure, prefer minimal root-cause changes, never weaken tests, add regression coverage when reasonable.
   - Performance: require metric, baseline, benchmark or benchmark discovery, correctness checks, and allowed tradeoffs; otherwise use `PLAN_FIRST` or `NEEDS_TIGHTENING`.
   - Migration: require source stack, target stack, parity checks, compatibility checks, and rollback or preservation strategy.
   - Research/audit: require source documents, claim inventory, evidence levels, unsupported-claim handling, reproduction target, and dataset/metric/compute constraints when relevant.
   - UI/prototype: require reference surface, viewport matrix, visual evidence, interaction checks, and accessibility checks when relevant.
   - Security: require authorized scope, non-destructive verification, no exploit escalation, no secret exposure, and approval before auth, permission, network, or production-impacting changes.
   - Refactor/docs: preserve behavior and public APIs, keep diffs reviewable, and require relevant tests or documentation checks.

5. Render or hand off.
   - For `READY_GOAL`, render a compact Markdown `/goal` contract with Context, Scope, Constraints, Verification, Iteration, Pause if, and Done when.
   - If the goal would be too long, render a short `/goal` that references a contract file such as `.goalplz/goal-contract.md`; include or create the contract only when file writes are appropriate.
   - If a goal-management tool is available, create the goal with the rendered objective unless the user asked for conversion only.
   - If no goal-management tool is available, give the user a ready-to-paste `/goal ...` command.
   - If another goal is already active, do not clear or replace it without explicit user approval.

6. Work against evidence.
   - Inspect current state before editing.
   - Reproduce failures or establish a baseline when feasible.
   - Change one hypothesis at a time.
   - After each attempt, check evidence and decide whether to continue, complete, or report blocked.
   - Mark complete only when the objective has been verified against concrete evidence.

## Safety Gates

Require explicit user approval before paid API calls, deploys, production writes, dependency installs, broad config changes, destructive filesystem or git actions, permission changes, auth/security posture changes, database schema or irreversible data changes, mass messaging, or other persistent external mutations.

If proxy evidence is used, label it as proxy support. If exact proof is impossible, preserve uncertainty in the final result instead of flattening it into success.

## Output Style

When converting before execution, use this shape:

```text
STATUS: READY_GOAL | PLAN_FIRST | NEEDS_TIGHTENING | NOT_GOAL | REFUSE
ROUTE: render_goal | render_plan_first | ask_tightening_questions | render_normal_prompt | refuse

REASON:
<brief routing reason>

BLOCKERS:
- <only blocking gaps; omit when none>

ASSUMPTIONS:
- <safe assumption> [source: user|inferred_safe|policy_default|adapter_default; safety: reversible|low_risk|approval_needed|unsafe; confidence: low|medium|high; confirm: yes|no]

COMPILED_GOAL:
<for READY_GOAL, a ready-to-paste /goal command or goal-management objective>

PLAN_OR_QUESTIONS:
<for non-ready statuses, a /plan prompt, up to three questions, normal prompt, or refusal>

QUALITY_CHECK:
- Done state is observable.
- Verification proves the done state.
- Constraints, non-goals, approval gates, pause triggers, rollback, and remaining risks are explicit.
```

For `READY_GOAL`, `COMPILED_GOAL` should be concise Markdown, not raw JSON. Keep JSON-like structure internal for validation and render a human-readable contract for Codex.

When execution finishes, report the outcome, changed files, verification run, skipped or failed checks, and remaining risk.

## Reference

Read `references/goal-patterns.md` for reusable templates, examples, and anti-patterns.
