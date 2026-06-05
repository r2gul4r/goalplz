---
description: Turn a rough request into a Codex Goal mode objective and run it when appropriate
argument-hint: REQUEST...
---

You are running the goalplz slash prompt.

Do not invoke an external goalplz skill alias or read a goalplz SKILL.md unless the user explicitly provided that file as source material. This prompt is self-contained.

Use this workflow:

1. Read the request and any pasted or attached text as the task source.
2. Classify Goal fit:
   - `yes` when the work has a durable objective, evidence-based finish line, and uncertain multi-step path.
   - `no` for a one-line edit, simple explanation, short review, or a request that should produce one answer and stop.
   - `needs tightening` when the user wants Goal mode but the finish line, verification surface, or safety boundary is materially unclear.
3. For `yes` or explicit Goal-mode requests, rewrite the request into an auditable goal contract with:
   - outcome
   - completion criteria
   - verification surface
   - constraints and boundaries
   - iteration policy
   - blocked stop condition
4. If a goal-management tool is available, create the goal with the rewritten objective unless the user asked for conversion only. If another goal is already active, do not replace it without explicit user approval.
5. If no goal-management tool is available, provide a ready-to-paste `/goal ...` command.
6. If the request is not suitable for Goal mode, say so briefly and proceed normally unless the user explicitly asked to force Goal mode.
7. During execution, inspect current state before editing, verify with concrete evidence when feasible, and report skipped or failed checks plainly.

Before execution, use this compact shape:

```text
Goalplz: active
Goal fit: <yes/no/needs tightening>
Goal:
<rewritten goal text or brief reason no goal is needed>

Assumptions:
- <only material assumptions>
```

If the request is empty, ask the user for the rough request to goalplz.

Request:

$ARGUMENTS
