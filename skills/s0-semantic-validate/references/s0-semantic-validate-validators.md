# s0-semantic-validate — Validator Types

| Type | Content | Protects Against |
|:---|:---|:---|
| `json_query` | JSON field assertion (jq syntax) | empty JSON, failed reports |
| `regex_match` | file content regex match | empty test files, stubs |
| `file_hash` | mtime vs sentinel timestamp | old report copies |
