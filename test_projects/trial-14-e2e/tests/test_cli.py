"""Integration tests for mdtoc CLI entry point."""
import subprocess
import sys
import tempfile
import os
import pytest


def run_mdtoc(*args, input_text=None):
    cmd = [sys.executable, "-m", "mdtoc"] + list(args)
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    )
    return result


class TestCLI:
    def test_generate_writes_to_stdout(self, tmp_path):
        # AC-4.1
        md = tmp_path / "test.md"
        md.write_text("# Hello\n\n## World\n\nBody.")
        result = run_mdtoc("generate", str(md))
        assert result.returncode == 0
        assert "<!-- TOC -->" in result.stdout
        assert "[Hello]" in result.stdout

    def test_generate_in_place_overwrites_file(self, tmp_path):
        # AC-4.2
        md = tmp_path / "test.md"
        md.write_text("# Hello\n\nBody.")
        result = run_mdtoc("generate", str(md), "--in-place")
        assert result.returncode == 0
        assert result.stdout == ""
        content = md.read_text()
        assert "<!-- TOC -->" in content
        assert "[Hello]" in content

    def test_max_level_flag(self, tmp_path):
        # AC-4.3
        md = tmp_path / "test.md"
        md.write_text("# H1\n## H2\n### H3\n\nBody.")
        result = run_mdtoc("generate", str(md), "--max-level", "2")
        assert result.returncode == 0
        assert "[H3]" not in result.stdout
        assert "[H1]" in result.stdout

    def test_nonexistent_file_exits_1(self):
        # AC-4.4
        result = run_mdtoc("generate", "/nonexistent/path/file.md")
        assert result.returncode == 1
        assert "error" in result.stderr.lower() or "not found" in result.stderr.lower()

    def test_no_subcommand_prints_help(self):
        # AC-4.5
        result = run_mdtoc()
        assert result.returncode == 0
        assert "usage" in result.stdout.lower() or "usage" in result.stderr.lower()
