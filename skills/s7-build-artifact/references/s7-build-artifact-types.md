# s7-build-artifact — Artifact Types

| Project type | Artifact | Command |
|---|---|---|
| Python library | `.whl` + `.tar.gz` | `python -m build` |
| Python service | Docker image | `docker build -t <name>:<version> .` |
| Node library | `.tgz` | `npm pack` |
| Node service | Docker image | `docker build -t <name>:<version> .` |
| Go binary | Binary | `go build -o dist/<name> .` |

If `Dockerfile` present, prefer Docker for services.
