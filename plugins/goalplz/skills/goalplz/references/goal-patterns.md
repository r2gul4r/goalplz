# Goal Patterns

Use these patterns after the `goalplz` workflow has triggered. Keep the final goal compact; do not paste every pattern unless it is useful.

## Core Template

```text
<Desired final state>.

Verification:
- <Command, artifact, report, benchmark, UI check, log, or source evidence>
- <Specific success threshold when available>

Constraints:
- <Behavior, API, schema, security, data, UX, dependency, or test constraints>
- <Actions that require approval or are forbidden>

Boundaries:
- Allowed writes: <paths>
- Off-limits: <paths, external systems, data>
- Allowed tools/data: <sources>

Iteration policy:
- Inspect current state and establish a baseline first.
- Change one hypothesis at a time.
- Record the change, evidence, and next action after each attempt.
- Run the fastest relevant check first, then expand verification.

Completion/blocked:
- Complete only when all verification evidence supports the objective.
- Stop as blocked when the same blocker repeats, required input is missing, approval is needed, or no defensible path remains.
```

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

Goal:

```text
Reproduce the failing tests on the current branch, identify the root cause, and make the smallest defensible change so the reproduced tests pass.

Verification:
- Run the failing test command before and after the fix.
- Run related tests or lint when the changed area makes that relevant.

Constraints:
- Do not delete, skip, or weaken tests to make the suite pass.
- Preserve public API behavior unless evidence shows the API is the bug.

Boundaries:
- Allowed writes: files directly related to the failing behavior.
- Off-limits: generated artifacts, lockfiles, and broad config unless evidence shows they are required.

Iteration policy:
- Use the failure output to form one hypothesis at a time.
- After each change, rerun the narrowest relevant test.

Completion/blocked:
- Complete only when the reproduced failures pass.
- Stop blocked if the same failure persists after three distinct grounded attempts or required dependencies/credentials are missing.
```

## Example: Performance

Raw request:

```text
Make checkout faster.
```

Goal:

```text
Reduce checkout p95 latency below <threshold> on <benchmark or endpoint metric> while keeping checkout correctness checks green.

Verification:
- Establish the current p95 baseline with <benchmark command or metric query>.
- Rerun the same benchmark after each candidate fix.
- Run checkout correctness tests before completion.

Constraints:
- Preserve checkout API behavior, validation, auth, pricing, and order creation semantics.
- Do not add caching that can serve stale price, inventory, or authorization data.

Boundaries:
- Allowed writes: checkout service, benchmark fixtures, and directly related tests.
- Off-limits: payment provider config, production data, and unrelated services without approval.

Iteration policy:
- Inspect the hot path, choose one bottleneck hypothesis, patch narrowly, and measure.
- Keep benchmark outputs or summaries for comparison.

Completion/blocked:
- Complete only when latency and correctness evidence both pass.
- Stop blocked if the benchmark cannot run, the target is unreachable under current constraints, or external service access is required.
```

## Example: Research Audit

Raw request:

```text
Reproduce this paper as much as possible.
```

Goal:

```text
Produce the strongest evidence-backed reproduction audit of <paper/topic> using available materials and local resources.

Verification:
- Build a claim inventory from the source material.
- Map each claim to exact reproduction, approximate reconstruction, proxy support, or blocked status.
- Generate a final report with evidence paths, commands run, artifacts produced, and remaining uncertainty.

Constraints:
- Do not describe approximate or proxy results as exact reproduction.
- Separate confirmed findings from unsupported or blocked claims.

Boundaries:
- Allowed inputs: provided paper, repo, local data, and approved public sources.
- Off-limits: paid datasets, private systems, or unverifiable claims without approval.

Iteration policy:
- Start with claim extraction, then implement or verify the most central claims first.
- Preserve commands, parameters, outputs, and artifacts needed for review.

Completion/blocked:
- Complete when the report clearly labels evidence strength for each material claim.
- Stop blocked for claims that require unavailable seeds, checkpoints, private data, credentials, or original experiment state.
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
