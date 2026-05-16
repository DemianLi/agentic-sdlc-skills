"""Performance test: REQ-5 — P99 < 500ms for 10K-line file with 200 headings."""
import time
import sys
import os
import tempfile

PYTHONPATH_SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
sys.path.insert(0, PYTHONPATH_SRC)

from mdtoc.core import parse_headers, generate_toc, insert_toc


def make_large_md(lines=10000, headings=200) -> str:
    """Generate a synthetic 10K-line Markdown file with 200 headings."""
    parts = []
    heading_every = lines // headings
    for i in range(lines):
        if i % heading_every == 0:
            level = (i // heading_every % 3) + 1
            parts.append(f"{'#' * level} Section {i // heading_every}\n")
        else:
            parts.append(f"Paragraph line {i} with some text content.\n")
    return "".join(parts)


def measure_p99(text: str, runs: int = 100, warmup: int = 15) -> float:
    """Return P99 latency in ms over `runs` warm-cache iterations."""
    latencies = []
    # Warmup — discard (trial-12 fix: matched warm-cache conditions)
    for _ in range(warmup):
        headers = parse_headers(text)
        toc = generate_toc(headers)
        insert_toc(text, toc)

    # Measurement
    for _ in range(runs):
        t0 = time.perf_counter()
        headers = parse_headers(text)
        toc = generate_toc(headers)
        insert_toc(text, toc)
        t1 = time.perf_counter()
        latencies.append((t1 - t0) * 1000)

    latencies.sort()
    p99_idx = int(0.99 * runs) - 1
    return latencies[p99_idx]


if __name__ == "__main__":
    text = make_large_md(10000, 200)
    print(f"File size: {len(text)} bytes, lines: {text.count(chr(10))}")

    p99 = measure_p99(text, runs=100, warmup=15)
    print(f"P99 latency: {p99:.2f}ms (SLO: < 500ms)")

    if p99 < 500:
        print("SLO: PASS")
        sys.exit(0)
    else:
        print("SLO: FAIL")
        sys.exit(1)
