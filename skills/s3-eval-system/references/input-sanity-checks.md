# Impact Scan — Input Sanity Checks

After loading `CONTEXT_SNAPSHOT.md`, verify each item before starting the codebase scan.
If any check fails, stop and state exactly what is missing.

| Check | What to verify | If it fails |
|---|---|---|
| `## Iteration Goal` is specific | One concrete goal — not a vague phrase like "improve the feature" or "refactor the module" | Ask: "What specific behavior should change? Please rewrite the goal as one sentence with a subject and verb." |
| `## Must-Have Requirements` lists REQ-N IDs | At least one `REQ-1`, `REQ-2`, etc. referencing an actual requirements doc | Ask: "Which requirements from Stage 2 are in scope? Please list REQ-N IDs from the requirements doc." |
| `## In Scope` names concrete components | Lists specific files, routes, or user flows — not just "the checkout module" | Ask: "Which specific files, routes, or components are in scope? The impact scan cannot proceed without a concrete boundary." |
| `## Forbidden Actions` exists | Explicit list of what must NOT be changed this iteration | Ask: "What should I absolutely not touch during this iteration? This section is required." |
