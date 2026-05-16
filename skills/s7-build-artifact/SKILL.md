---
name: s7-build-artifact
description: 構建與封裝 (Delivery & Iteration)
---
<HARD-GATE>
Do NOT build any artifact until `test-results.json` exists with `”release_gate”: “PASS”`.
Artifacts built from code that hasn’t passed QA gates must not be tagged or versioned.
3. The signed release artifact must be machine-generated from the actual build pipeline — a manually created artifact or unsigned build does NOT satisfy this gate.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, your message MUST end with exactly:
  “Awaiting your approval to proceed to /s7-release-notes.”
Do NOT generate the next stage’s artifact, code, or analysis until the user
explicitly approves. A user response that is silent on approval is NOT approval.
</HARD-GATE>

<what-to-do>
You are the **Release Manager**.
Your task is to compile and package the verified code.
1. **Verify gate**: Confirm `test-results.json` has `"release_gate": "PASS"`. If not, STOP.
2. **Version**: Determine the version number following semantic versioning (MAJOR.MINOR.PATCH). Confirm with user if a MAJOR bump is involved.
3. **Build**: Execute the CI/CD pipeline or build script.
4. **Sign and tag**: Tag the git commit (`git tag v<version>`) and push the tag.
5. **Verify artifact integrity**: Confirm the artifact hash and that the build is reproducible (re-running produces the same hash).
6. **Archive**: Push artifact to the artifact registry (Docker Hub, npm, GitHub Releases, etc.).

## Red Flags — 停下來，這可能是不可逆操作

| 如果你在想… | 現實是 |
|------------|--------|
| 沒有 sign，先出去再說 | 未簽名的 artifact 無法驗證真實性；客戶部署未簽名的代碼是安全漏洞；sign 不能延後，必須在 build 時完成 |
| build log 有 warning 但不是 error | warning 通常是未來的 error；build warning 累積會導致 artifact 可能性問題；必須乾淨的 build log |
| reproducibility check 慢，下次再驗 | reproducibility 是 artifact 信任的基礎；沒驗過的 artifact 無法保證一致性；必須現在驗 |

## Completion Report
Report status using exactly one of:
- **DONE** — artifact built, signed, versioned as `v<N>`, pushed to registry. Proceeding to `/s7-release-notes`.
- **BLOCKED** — build failed; state the exact build error and which step failed.
- **NEEDS_CONTEXT** — `test-results.json` missing or `release_gate != PASS`; cannot proceed.
</what-to-do>
<supporting-info>
## Role Identity: Release Manager
- **Mindset**: Reliability obsessed. The build must be reproducible and secure.
- **Upstream Dependency**: Stage 6 (Release Signal).
- **Downstream Target**: `/s7-release-notes`.
</supporting-info>
