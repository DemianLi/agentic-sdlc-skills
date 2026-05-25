# s7-deploy — Per-Target Commands & Smoke Tests

## Deploy Commands

### Live Mode
- **PyPI**: `twine upload dist/*`
- **Docker**: `flyctl deploy --image <name>:<version>`
- **k8s**: `kubectl set image deployment/<name> <container>=<image>:<version>` && `kubectl rollout status`
- **npm**: `npm publish`

### Dry-Run Mode
- **Wheel**: `pip install dist/<name>-<version>-*.whl` (local, safe)
- **Docker**: `docker build -t <name>:<version> . --no-cache`

## Smoke Tests

- **Python library**: `python -c "import <module>; print(<module>.__version__)"`
- **API service**: `curl -s http://localhost:<port>/health | jq .status`
- **Key function**: `python -c "from module import func; print(func('test'))"`
