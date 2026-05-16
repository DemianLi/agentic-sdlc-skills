"""Unit tests for slugify.core module."""
import pytest
from slugify import slugify


class TestSlugifyBasic:
    """Test basic slugify behavior from design.md AC-1.1 and AC-1.2."""

    def test_hello_world_default_separator(self):
        """AC-1.1: slugify("Hello World") → "hello-world"."""
        assert slugify("Hello World") == "hello-world"

    def test_accented_chars_custom_separator(self):
        """AC-1.2: slugify("Héllo & Wörld!", separator="_") → "hllo__wrld"."""
        assert slugify("Héllo & Wörld!", separator="_") == "hllo__wrld"


class TestSlugifyEdgeCases:
    """Test edge cases and special inputs."""

    def test_empty_string(self):
        """Empty input returns empty string."""
        assert slugify("") == ""

    def test_whitespace_only_default(self):
        """Whitespace-only input becomes separators."""
        assert slugify("   ") == "---"

    def test_whitespace_only_custom(self):
        """Whitespace-only with custom separator."""
        assert slugify("   ", separator="_") == "___"

    def test_multiple_consecutive_whitespace(self):
        """Multiple whitespace becomes multiple separators (not collapsed)."""
        assert slugify("  a  b  ") == "--a--b--"

    def test_special_chars_only(self):
        """String with only special characters returns empty."""
        assert slugify("!!!") == ""

    def test_accented_stripped_not_transliterated(self):
        """Accented characters are stripped, not converted."""
        assert slugify("Café") == "caf"

    def test_unicode_cjk(self):
        """CJK characters are stripped."""
        assert slugify("你好世界") == ""

    def test_custom_separator_period(self):
        """Custom separator as period."""
        assert slugify("Hello World", separator=".") == "hello.world"

    def test_custom_separator_underscore(self):
        """Custom separator as underscore."""
        assert slugify("Hello World", separator="_") == "hello_world"

    def test_custom_separator_tilde(self):
        """Custom separator as tilde."""
        assert slugify("Hello World", separator="~") == "hello~world"

    def test_mixed_case_lowercased(self):
        """Mixed case is converted to lowercase."""
        assert slugify("HeLLo WoRLd") == "hello-world"

    def test_digits_preserved(self):
        """Digits are preserved."""
        assert slugify("Hello 123 World") == "hello-123-world"

    def test_tabs_and_newlines(self):
        """Tabs and newlines are treated as whitespace."""
        assert slugify("hello\tworld") == "hello-world"
        assert slugify("hello\nworld") == "hello-world"

    def test_ampersand_stripped(self):
        """Ampersand and other special chars are stripped."""
        assert slugify("Hello & World") == "hello--world"

    def test_exclamation_stripped(self):
        """Exclamation marks are stripped."""
        assert slugify("Hello!") == "hello"

    def test_question_stripped(self):
        """Question marks are stripped."""
        assert slugify("Hello?") == "hello"
