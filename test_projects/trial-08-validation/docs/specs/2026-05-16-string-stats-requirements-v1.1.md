# String Stats Library Requirements — v1.1

## Change Log
- **v1.1** (2026-05-16): ADDED REQ-4 paragraph_count

## Scope Contract
**IN SCOPE**: word_count, char_count, sentence_count, paragraph_count
**OUT OF SCOPE**: file I/O, async, encoding detection

## REQ-1: Word Count
**User Story**: As a developer, I want to count words in a string, so I can analyze text volume.
**Acceptance Criteria**:
- [ ] AC-1.1: Given "hello world", when word_count("hello world"), then returns 2
- [ ] AC-1.2: Given "", when word_count(""), then returns 0
- [ ] AC-1.3: Given "  spaces  ", when word_count("  spaces  "), then returns 1

## REQ-2: Character Count (no whitespace)
**User Story**: As a developer, I want character count excluding whitespace, so I can measure content density.
**Acceptance Criteria**:
- [ ] AC-2.1: Given "hello world", when char_count("hello world"), then returns 10
- [ ] AC-2.2: Given "", when char_count(""), then returns 0
- [ ] AC-2.3: Given "   ", when char_count("   "), then returns 0

## REQ-3: Sentence Count
**User Story**: As a developer, I want to count sentences, so I can analyze text structure.
**Acceptance Criteria**:
- [ ] AC-3.1: Given "Hello. World!", when sentence_count("Hello. World!"), then returns 2
- [ ] AC-3.2: Given "", when sentence_count(""), then returns 0
- [ ] AC-3.3: Given "No ending", when sentence_count("No ending"), then returns 0
- [ ] AC-3.4: Given "Wait... really?", when sentence_count("Wait... really?"), then returns 2 (each `.!?` counts)

## REQ-4: Paragraph Count [ADDED v1.1]
**User Story**: As a developer, I want to count paragraphs, so I can analyze document structure.
**Acceptance Criteria**:
- [ ] AC-4.1: Given "Para 1\n\nPara 2", when paragraph_count("Para 1\n\nPara 2"), then returns 2
- [ ] AC-4.2: Given "", when paragraph_count(""), then returns 0
- [ ] AC-4.3: Given "Single para", when paragraph_count("Single para"), then returns 1

## Test Coverage Map
| AC | Test Type |
|----|-----------|
| AC-1.1 – AC-1.3 | Unit |
| AC-2.1 – AC-2.3 | Unit |
| AC-3.1 – AC-3.4 | Unit |
| AC-4.1 – AC-4.3 | Unit |
