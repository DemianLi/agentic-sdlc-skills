"""String Stats Library Tests — TDD Implementation

Test suite covering AC-1.1 through AC-4.3 from v1.1 requirements.
"""

import pytest
from string_stats import word_count, char_count, sentence_count, paragraph_count


class TestWordCount:
    """REQ-1: Word Count"""

    def test_word_count_basic(self):
        """AC-1.1: Given "hello world", when word_count("hello world"), then returns 2"""
        assert word_count("hello world") == 2

    def test_word_count_empty_string(self):
        """AC-1.2: Given "", when word_count(""), then returns 0"""
        assert word_count("") == 0

    def test_word_count_leading_trailing_spaces(self):
        """AC-1.3: Given "  spaces  ", when word_count("  spaces  "), then returns 1"""
        assert word_count("  spaces  ") == 1


class TestCharCount:
    """REQ-2: Character Count (no whitespace)"""

    def test_char_count_basic(self):
        """AC-2.1: Given "hello world", when char_count("hello world"), then returns 10"""
        assert char_count("hello world") == 10

    def test_char_count_empty_string(self):
        """AC-2.2: Given "", when char_count(""), then returns 0"""
        assert char_count("") == 0

    def test_char_count_only_whitespace(self):
        """AC-2.3: Given "   ", when char_count("   "), then returns 0"""
        assert char_count("   ") == 0


class TestSentenceCount:
    """REQ-3: Sentence Count"""

    def test_sentence_count_basic(self):
        """AC-3.1: Given "Hello. World!", when sentence_count("Hello. World!"), then returns 2"""
        assert sentence_count("Hello. World!") == 2

    def test_sentence_count_empty_string(self):
        """AC-3.2: Given "", when sentence_count(""), then returns 0"""
        assert sentence_count("") == 0

    def test_sentence_count_no_ending_punctuation(self):
        """AC-3.3: Given "No ending", when sentence_count("No ending"), then returns 0"""
        assert sentence_count("No ending") == 0

    def test_sentence_count_multiple_punctuation(self):
        """AC-3.4: Given "Wait... really?", when sentence_count("Wait... really?"), then returns 2 (each `.!?` counts)"""
        assert sentence_count("Wait... really?") == 2


class TestParagraphCount:
    """REQ-4: Paragraph Count [ADDED v1.1]"""

    def test_paragraph_count_basic(self):
        """AC-4.1: Given "Para 1\n\nPara 2", when paragraph_count("Para 1\n\nPara 2"), then returns 2"""
        assert paragraph_count("Para 1\n\nPara 2") == 2

    def test_paragraph_count_empty_string(self):
        """AC-4.2: Given "", when paragraph_count(""), then returns 0"""
        assert paragraph_count("") == 0

    def test_paragraph_count_single_para(self):
        """AC-4.3: Given "Single para", when paragraph_count("Single para"), then returns 1"""
        assert paragraph_count("Single para") == 1
