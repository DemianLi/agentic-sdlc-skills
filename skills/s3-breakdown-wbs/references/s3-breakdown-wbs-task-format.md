# s3-breakdown-wbs — Task Format Template

For each Atomic Task, write:

```markdown
### TASK-<N>: <Short, Verb-Noun Title>

**Input**: <exact files, data, or state this task starts from>
**Output**: <exact files created/modified, or observable state change>
**Acceptance Criterion**: <binary: pass or fail — use the AC-N.M from REQ in /s2-struct-req>
**Estimated Complexity**: <2 min | 3 min | 5 min> (code only)
**Blocked by**: TASK-<M>, TASK-<K> (or "none")
**File Scope**: <list exact file paths to touch>
```
