# String Stats API — Requirements v1.0

**Topic**: string-stats-api
**Date**: 2026-05-16
**Status**: APPROVED

---

## REQ-1: Word Count

The `/analyze` endpoint must return `word_count` = number of space-separated tokens in `text`.

### Acceptance Criteria

- AC-1.1: `word_count("hello world")` returns 2
- AC-1.2: `word_count("")` returns 0
- AC-1.3: `word_count("  leading  trailing  ")` returns 2
- AC-1.4: API returns `word_count` field in JSON response for any text input

---

## REQ-2: Character Count

The `/analyze` endpoint must return `char_count` = number of non-whitespace characters in `text`.

### Acceptance Criteria

- AC-2.1: `char_count("hello world")` returns 10
- AC-2.2: `char_count("")` returns 0
- AC-2.3: `char_count("   ")` returns 0 (whitespace only)

---

## REQ-3: Sentence Count

The `/analyze` endpoint must return `sentence_count` = number of sentence boundaries (`.`, `!`, `?`).

### Acceptance Criteria

- AC-3.1: `sentence_count("Hello. World.")` returns 2
- AC-3.2: `sentence_count("")` returns 0
- AC-3.3: `sentence_count("no ending")` returns 0
- AC-3.4: `sentence_count("Wait... really?")` returns 2 (consecutive punctuation = one boundary)

---

## REQ-4: Paragraph Count

The `/analyze` endpoint must return `paragraph_count` = number of paragraphs separated by `\n\n`.

### Acceptance Criteria

- AC-4.1: `paragraph_count("para1\n\npara2")` returns 2
- AC-4.2: `paragraph_count("")` returns 0
- AC-4.3: `paragraph_count("single paragraph")` returns 1

---

## REQ-5: API Performance

The `/analyze` endpoint must meet performance SLOs.

### Acceptance Criteria

- AC-5.1: P99 response time < 50ms for text up to 10,000 characters (ASGI transport)
- AC-5.2: Error rate = 0% under 100 sequential requests
- AC-5.3: word_count P99 < 1ms for 10,000 character text
- AC-5.4: No memory leak detected over 1,000 sequential requests
