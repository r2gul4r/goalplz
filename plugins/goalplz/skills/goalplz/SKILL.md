---
name: goalplz
description: Convert rough user requests into strong Codex Goal mode objectives and run them when appropriate. Use only when the user explicitly invokes /goalplz, $goalplz, or asks for goalplz by name to turn an unclear multi-step coding, debugging, optimization, migration, testing, research, or audit request into an evidence-checked completion contract.
---

# Goalplz

Use this skill to decide whether Goal mode is warranted, rewrite the request into an auditable goal, and start or hand off that goal safely.

## Workflow

1. Classify the request.
   - Use Goal mode when the work has a durable objective, evidence-based finish line, and uncertain multi-step path.
   - Do not use Goal mode for a one-line edit, simple explanation, short review, or a request that should produce one answer and stop.
   - If the user explicitly asks for Goal mode but the finish line is vague, tighten the completion criteria before starting.

2. Extract the goal contract.
   - Outcome: final state that should be true.
   - Verification surface: tests, lint, build, benchmark, report, artifact, screenshot, data, logs, or source evidence that proves completion.
   - Constraints: APIs, schemas, behavior, security, data, UX, dependencies, and tests that must not regress.
   - Boundaries: files, directories, tools, external systems, and data that are allowed or off-limits.
   - Iteration policy: how to choose the next attempt after each result.
   - Blocked stop condition: when to stop and report missing input, repeated failure, approval needs, or no defensible path.

3. Handle missing detail.
   - If a safe assumption is obvious and reversible, state it briefly and proceed.
   - If verification, scope, or safety materially changes the work, ask the minimum necessary question before creating the goal.
   - Never invent success metrics or permission for risky external actions.

4. Produce the goal.
   - Keep the goal specific enough to audit and broad enough to let Codex choose the next useful action.
   - Include blocked behavior explicitly.
   - Use the compact template in `references/goal-patterns.md` when useful.

5. Start or hand off the goal.
   - If a goal-management tool is available, create the goal with the rewritten objective unless the user asked for conversion only.
   - If no goal-management tool is available, give the user a ready-to-paste `/goal ...` command.
   - If another goal is already active, do not clear or replace it without explicit user approval.

6. Work against evidence.
   - Inspect current state before editing.
   - Reproduce failures or establish a baseline when feasible.
   - Change one hypothesis at a time.
   - After each attempt, check evidence and decide whether to continue, complete, or report blocked.
   - Mark complete only when the objective has been verified against concrete evidence.

## Safety Gates

Require explicit user approval before paid API calls, deploys, production writes, dependency installs, broad config changes, destructive filesystem or git actions, permission changes, mass messaging, or other persistent external mutations.

If proxy evidence is used, label it as proxy support. If exact proof is impossible, preserve uncertainty in the final result instead of flattening it into success.

## Output Style

When converting before execution, use this concise shape:

```text
Goal fit: <yes/no/needs tightening>
Goal:
<rewritten goal text>

Assumptions:
- <only material assumptions>
```

When execution finishes, report the outcome, changed files, verification run, skipped or failed checks, and remaining risk.

## Reference

Read `references/goal-patterns.md` for reusable templates, examples, and anti-patterns.
