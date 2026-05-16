"""Unit tests for string_stats module."""
import pytest
from src.string_stats import (
    char_count,
    paragraph_count,
    sentence_count,
    word_count,
)


class TestWordCount:
    """Tests for word_count function."""

    def test_basic_two_words(self):
        """AC-1.1: word_count('hello world') returns 2."""
        assert word_count("hello world") == 2

    def test_empty_string(self):
        """AC-1.2: word_count('') returns 0."""
        assert word_count("") == 0

    def test_leading_trailing_spaces(self):
        """AC-1.3: word_count with leading/trailing spaces returns correct count."""
        assert word_count("  leading  trailing  ") == 2

    def test_single_word(self):
        """Single word returns 1."""
        assert word_count("hello") == 1

    def test_multiple_spaces(self):
        """Multiple spaces between words counted as single separator."""
        assert word_count("hello    world") == 2


class TestCharCount:
    """Tests for char_count function."""

    def test_basic_string(self):
        """AC-2.1: char_count('hello world') returns 10."""
        assert char_count("hello world") == 10

    def test_empty_string(self):
        """AC-2.2: char_count('') returns 0."""
        assert char_count("") == 0

    def test_whitespace_only(self):
        """AC-2.3: char_count with only whitespace returns 0."""
        assert char_count("   ") == 0

    def test_newlines_ignored(self):
        """Newlines are not counted."""
        assert char_count("hello\nworld") == 10

    def test_tabs_ignored(self):
        """Tabs are not counted."""
        assert char_count("hello\tworld") == 10


class TestSentenceCount:
    """Tests for sentence_count function."""

    def test_two_sentences_periods(self):
        """AC-3.1: sentence_count('Hello. World.') returns 2."""
        assert sentence_count("Hello. World.") == 2

    def test_empty_string(self):
        """AC-3.2: sentence_count('') returns 0."""
        assert sentence_count("") == 0

    def test_no_ending_punctuation(self):
        """AC-3.3: sentence_count('no ending') returns 0."""
        assert sentence_count("no ending") == 0

    def test_consecutive_punctuation(self):
        """AC-3.4: consecutive punctuation counts as one boundary."""
        assert sentence_count("Wait... really?") == 2

    def test_mixed_punctuation(self):
        """Mixed sentence endings counted correctly."""
        assert sentence_count("Hello! How are you? Good.") == 3

    def test_exclamation_marks(self):
        """Exclamation marks count as sentence boundaries."""
        assert sentence_count("Wow! Amazing!") == 2

    def test_question_marks(self):
        """Question marks count as sentence boundaries."""
        assert sentence_count("Why? Because!") == 2


class TestParagraphCount:
    """Tests for paragraph_count function."""

    def test_two_paragraphs(self):
        """AC-4.1: paragraph_count('para1\\n\\npara2') returns 2."""
        assert paragraph_count("para1\n\npara2") == 2

    def test_empty_string(self):
        """AC-4.2: paragraph_count('') returns 0."""
        assert paragraph_count("") == 0

    def test_single_paragraph(self):
        """AC-4.3: paragraph_count('single paragraph') returns 1."""
        assert paragraph_count("single paragraph") == 1

    def test_three_paragraphs(self):
        """Three paragraphs separated by double newlines."""
        assert paragraph_count("para1\n\npara2\n\npara3") == 3

    def test_single_newline_not_separator(self):
        """Single newline does not create new paragraph."""
        assert paragraph_count("para1\npara2") == 1

    def test_multiple_double_newlines(self):
        """Multiple consecutive double newlines handled correctly."""
        assert paragraph_count("para1\n\n\n\npara2") == 2
