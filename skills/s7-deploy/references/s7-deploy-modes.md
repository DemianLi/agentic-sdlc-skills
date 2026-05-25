# s7-deploy — Deploy Modes

| Mode | When | deploy_mode field |
|---|---|---|
| `live` | Real target available (k8s, fly.io, Docker registry, PyPI) | `"live"` |
| `dry-run` | No real target (trial, CI preview, local validation) | `"dry-run"` |
| `gitops` | Team uses ArgoCD/Flux; deploy = PR merge to main, CD auto-triggers | `"gitops"` |

**GitOps**: "deploy" = merge PR to `main`. No manual `kubectl apply` or `fly deploy`. Wait for ArgoCD sync / Flux reconcile before smoke tests.
