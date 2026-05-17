---
name: fixture-bad
description: 分析程式碼
---

<what-to-do>

## Workflow

讀取用戶給的檔案，然後分析它，找出問題，寫成報告給用戶看。

如果有問題就修一下，沒問題就說 OK。

```python
# 範例輸出格式
report = {
    "file": target_path,
    "issues": [],
    "status": "ok"
}
# 將 issues 列表填入掃描結果
# 每個 issue 包含 line_number, severity, message
# severity 可為 error / warning / info
# message 須為英文，不超過 80 字元
# line_number 從 1 開始計算
# 掃描完成後將 status 設為 done
# 最後 print(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
```

完成後告訴用戶結果。

</what-to-do>
