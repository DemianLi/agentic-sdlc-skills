"""Integration tests for slugify CLI."""
import subprocess
import sys
import pytest


def run_slugify(*args, input_text=None):
    """Run slugify CLI and return (returncode, stdout, stderr)."""
    cmd = [sys.executable, "-m", "slugify"] + list(args)
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        input=input_text,
        cwd="/Users/demian/Projects_vibecoding/research_skill_from_github/test_projects/trial-15-gates",
    )
    return result.returncode, result.stdout, result.stderr


class TestCLIBasic:
    """Test basic CLI behavior from design.md AC-2.x."""

    def test_cli_hello_world(self):
        """AC-2.1: python -m slugify "Hello World" → hello-world\\n (exit 0)."""
        code, stdout, stderr = run_slugify("Hello World")
        assert code == 0
        assert stdout == "hello-world\n"

    def test_cli_empty_string(self):
        """AC-2.2: python -m slugify "" → exit 1, no output."""
        code, stdout, stderr = run_slugify("")
        assert code == 1
        assert stdout == ""


class TestCLICustomSeparator:
    """Test custom separator flag."""

    def test_cli_custom_separator_underscore(self):
        """AC-3.1: python -m slugify "Hello World" --separator _ → hello_world\\n."""
        code, stdout, stderr = run_slugify("Hello World", "--separator", "_")
        assert code == 0
        assert stdout == "hello_world\n"

    def test_cli_custom_separator_period(self):
        """AC-3.2: python -m slugify "Hello World" --separator . → hello.world\\n."""
        code, stdout, stderr = run_slugify("Hello World", "--separator", ".")
        assert code == 0
        assert stdout == "hello.world\n"


class TestCLIExitCodes:
    """Test exit code behavior."""

    def test_cli_nonempty_exit_0(self):
        """AC-4.1: Non-empty slug → exit 0."""
        code, stdout, stderr = run_slugify("Hello")
        assert code == 0

    def test_cli_empty_exit_1(self):
        """AC-4.2: Empty slug → exit 1."""
        code, stdout, stderr = run_slugify("!!!")
        assert code == 1
        assert stdout == ""


class TestCLIStdin:
    """Test stdin fallback behavior."""

    def test_cli_stdin_reads_from_stdin(self):
        """echo "Hello" | python -m slugify → hello\\n (exit 0)."""
        code, stdout, stderr = run_slugify(input_text="Hello\n")
        assert code == 0
        assert stdout == "hello\n"

    def test_cli_stdin_multiline(self):
        """Multi-line stdin: newlines become separators."""
        code, stdout, stderr = run_slugify(input_text="Hello\nWorld\n")
        assert code == 0
        assert stdout == "hello-world\n"

    def test_cli_stdin_with_separator(self):
        """stdin with custom separator."""
        code, stdout, stderr = run_slugify("--separator", "_", input_text="Hello World\n")
        assert code == 0
        assert stdout == "hello_world\n"

    def test_cli_text_priority_over_stdin(self):
        """When TEXT is provided, stdin is not read."""
        code, stdout, stderr = run_slugify("Hello", input_text="Ignored\n")
        assert code == 0
        assert stdout == "hello\n"


class TestCLIHelp:
    """Test help text."""

    def test_cli_help_flag(self):
        """python -m slugify --help exits 0."""
        code, stdout, stderr = run_slugify("--help")
        assert code == 0
        # Help text should contain usage info
        assert "usage" in stdout.lower() or "slugify" in stdout.lower()


class TestCLISpecialCases:
    """Test special cases."""

    def test_cli_only_special_chars(self):
        """Only special characters → exit 1."""
        code, stdout, stderr = run_slugify("!!!")
        assert code == 1

    def test_cli_accented_chars(self):
        """Accented characters are stripped."""
        code, stdout, stderr = run_slugify("Café")
        assert code == 0
        assert stdout == "caf\n"

    def test_cli_preserves_digits(self):
        """Digits are preserved."""
        code, stdout, stderr = run_slugify("Hello 123")
        assert code == 0
        assert stdout == "hello-123\n"
