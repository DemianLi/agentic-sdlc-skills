"""Performance tests: validate SLO compliance (AC-5.1 through AC-5.4)."""
import time

import pytest

from src.string_stats import char_count, paragraph_count, sentence_count, word_count

LARGE_TEXT = "The quick brown fox jumps over the lazy dog. " * 222  # ~10,000 chars


def _p99(times):
    """Calculate 99th percentile from timing data."""
    data = sorted(times)
    k = (len(data) - 1) * 0.99
    lo, hi = int(k), min(int(k) + 1, len(data) - 1)
    return data[lo] + (data[hi] - data[lo]) * (k - lo)


def test_word_count_p99_under_1ms():
    """AC-5.3: word_count P99 < 1ms for 10,000 char text."""
    times = []
    for _ in range(200):
        t0 = time.perf_counter()
        word_count(LARGE_TEXT)
        times.append((time.perf_counter() - t0) * 1000)
    p99 = _p99(times)
    print(f"\nword_count P99: {p99:.3f}ms")
    assert p99 < 1.0, f"word_count P99 = {p99:.3f}ms (SLO: < 1ms)"


def test_char_count_p99_under_1ms():
    """AC-5.3: char_count P99 < 1ms for 10,000 char text."""
    times = []
    for _ in range(200):
        t0 = time.perf_counter()
        char_count(LARGE_TEXT)
        times.append((time.perf_counter() - t0) * 1000)
    p99 = _p99(times)
    print(f"\nchar_count P99: {p99:.3f}ms")
    assert p99 < 1.0, f"char_count P99 = {p99:.3f}ms (SLO: < 1ms)"


def test_sentence_count_p99_under_2ms():
    """AC-5.3: sentence_count P99 < 2ms for 10,000 char text."""
    times = []
    for _ in range(200):
        t0 = time.perf_counter()
        sentence_count(LARGE_TEXT)
        times.append((time.perf_counter() - t0) * 1000)
    p99 = _p99(times)
    print(f"\nsentence_count P99: {p99:.3f}ms")
    assert p99 < 2.0, f"sentence_count P99 = {p99:.3f}ms (SLO: < 2ms)"


def test_paragraph_count_p99_under_1ms():
    """paragraph_count P99 < 1ms for 10,000 char text."""
    times = []
    for _ in range(200):
        t0 = time.perf_counter()
        paragraph_count(LARGE_TEXT)
        times.append((time.perf_counter() - t0) * 1000)
    p99 = _p99(times)
    print(f"\nparagraph_count P99: {p99:.3f}ms")
    assert p99 < 1.0, f"paragraph_count P99 = {p99:.3f}ms (SLO: < 1ms)"
