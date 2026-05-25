# s0-skill-budget — D/I/S Axis Checks

## D-Axis: Description Budget {#d-axis}

| Code | Check | Standard |
|------|-------|----------|
| D1 | Length | tokens ≤ 40 |
| D2 | Trigger | starts "Use when" + task keyword |
| D3 | Output | contains "Outputs:" or artifact name |
| D4 | Exclusion | contains "NOT" + scenario |
| D5 | No workflow words | no "Step" / "->" / "Workflow" |

## I-Axis: Index Coverage {#i-axis}

| Code | Check | Standard |
|------|-------|----------|
| I1 | Listed | skill name in index values |
| I2 | Keywords | ≥ 2 keywords point to skill |
| I3 | No conflicts | no keyword shared with adjacent stages |

## S-Axis: Size Budget {#s-axis}

| Code | Check | Standard |
|------|-------|----------|
| S1 | File size | ≤ 10 KB |
| S2 | Section length | no `###` section > 50 lines |
| S3 | External refs | all `Reads:` files exist |
