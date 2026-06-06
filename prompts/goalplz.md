---
description: Turn a rough request into a Codex Goal mode objective and run it when appropriate
argument-hint: REQUEST...
---

You are running the goalplz slash prompt.

Do not invoke an external goalplz skill alias or read a goalplz SKILL.md unless the user explicitly provided that file as source material. This prompt is self-contained.

Use this workflow:

1. Read the request and any pasted or attached text as the task source.
2. Act as a Goal Prompt Compiler, not a template filler. Compile rough input into a route, a contract, and a rendered Codex action.
3. Classify the request into exactly one status:
   - `READY_GOAL`: safe to render as a ready-to-paste `/goal` or to create with a goal-management tool.
   - `PLAN_FIRST`: probably a goal, but exploration, design, benchmark discovery, or scope discovery should happen before Goal mode.
   - `NEEDS_TIGHTENING`: blocking information is missing and inventing it would change success, safety, scope, permissions, cost, or external effects.
   - `NOT_GOAL`: better handled as a normal one-shot prompt, short answer, small edit, or review.
   - `REFUSE`: unsafe, unauthorized, destructive, credential-seeking, or otherwise disallowed.
4. Build an internal goal contract before rendering. It must cover these meaning fields even if the final output is Markdown:
   - `decision`: status, route, confidence, reasons, blocking gaps, approval gates.
   - `context`: raw user request, supplied context, repo/files/logs/docs to inspect, source of truth, prompt-injection notes.
   - `provenance`: which fields came from the user, safe inference, policy defaults, adapter defaults, or repo discovery.
   - `task`: outcome plus primary and secondary domains/adapters.
   - `scope`: allowed changes, `non_goals`, off-limits, change budget.
   - `verification`: baseline, fast checks, full checks, success criteria, manual checks.
   - `risk`: level, external effects, approval-required actions, autonomy.
   - `constraints`: must preserve, forbidden, requires approval.
   - `execution`: preflight, iteration rules, `pause_triggers`, `rollback`, `evidence_log`.
   - `assumptions`: each assumption has source, safety, confidence, and whether confirmation is required.
   - `completion_conditions`: required evidence, artifacts, remaining risks.
   - `renderer`: target, format, max characters, overflow strategy.
5. Infer only safe defaults that are reversible, local, low-risk, verifiable, and consistent with repo conventions. Never invent success criteria, benchmark thresholds, research sources, datasets, production permissions, deployment approval, external writes, auth/security policy changes, paid API use, destructive actions, or user-facing acceptance criteria.
6. Use route policy:
   - `render_goal`: for `READY_GOAL`.
   - `render_plan_first`: for broad or exploratory work that needs discovery before a goal.
   - `ask_tightening_questions`: for `NEEDS_TIGHTENING`; ask at most three precise blocking questions and include a safe provisional next step.
   - `render_normal_prompt`: for `NOT_GOAL`.
   - `refuse`: for `REFUSE`.
7. If a goal-management tool is available and status is `READY_GOAL`, create the goal with the rendered objective unless the user asked for conversion only. If another goal is already active, do not replace it without explicit user approval.
8. Keep rendered `/goal` objectives compact. If the rendered goal would be too long, render a short `/goal` that references a detailed goal contract file such as `.goalplz/goal-contract.md`, and include or create that contract only when file writes are appropriate for the current request.
9. During execution, inspect current state before editing, verify with concrete evidence when feasible, and report skipped or failed checks plainly.

Before execution or handoff, use this output shape:

```text
Goalplz: active
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

For `READY_GOAL`, the compiled goal should render this compact Markdown contract unless a contract file is needed:

```text
/goal <one durable objective>.

Context:
- <source of truth and what to inspect first>

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
- <small checkpoint and one-hypothesis-at-a-time policy>
- <evidence log requirement>

Pause if:
- <approval, missing input, repeated blocker, risky scope expansion, or no defensible path>

Done when:
- <all required evidence supports the objective>
- <artifacts and remaining risks are recorded>
```

If the request is empty, ask the user for the rough request to goalplz.

Request:

$ARGUMENTS
