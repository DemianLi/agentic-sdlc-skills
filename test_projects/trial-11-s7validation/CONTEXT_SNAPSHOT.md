# CONTEXT_SNAPSHOT.md — String Stats API

## Project Purpose
HTTP API for text analysis. Consumers are developers calling GET /analyze to get statistics about a piece of text.

## Main User Flows

### Flow 1: Analyze Standard Text
User sends a multi-sentence paragraph and receives all 4 metrics.
- Input: GET /analyze?text=<standard_paragraph>
- Expected: 200 OK with word_count, char_count, sentence_count, paragraph_count all > 0

### Flow 2: Analyze Empty Text
User sends empty string; API returns zeros for all metrics without error.
- Input: GET /analyze?text=
- Expected: 200 OK with all metrics = 0

### Flow 3: Analyze Multi-Paragraph Text
User sends text with multiple paragraphs separated by double newlines.
- Input: GET /analyze?text=<multi_para_text>
- Expected: 200 OK with paragraph_count >= 2

### Flow 4: Analyze Text with No Sentence Endings
User sends text with no . ! ? punctuation.
- Input: GET /analyze?text=<text_without_punctuation>
- Expected: 200 OK with sentence_count = 0

## Secondary Flows

### Flow S1: Analyze Very Long Text (10,000 chars)
User sends text at the performance boundary.
- Expected: 200 OK within SLO limits

### Flow S2: Analyze Whitespace-Only Text
User sends only spaces/newlines.
- Expected: 200 OK with word_count=0, char_count=0

## AC Traceability
- Flow 1 → REQ-1 (word_count), REQ-2 (char_count), REQ-3 (sentence_count), REQ-4 (paragraph_count)
- Flow 2 → AC-1.2, AC-2.2, AC-3.2, AC-4.2 (empty string edge cases)
- Flow 3 → AC-4.1 (multi-paragraph detection)
- Flow 4 → AC-3.3 (no ending punctuation)
