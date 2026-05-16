"""String statistics analysis library."""


def word_count(text: str) -> int:
    """Count the number of space-separated words in text."""
    return len(text.split())


def char_count(text: str) -> int:
    """Count non-whitespace characters in text."""
    return len(text.replace(" ", "").replace("\n", "").replace("\t", ""))


def sentence_count(text: str) -> int:
    """Count sentence boundaries (., !, ?) in text."""
    if not text:
        return 0
    count = 0
    prev_char = ""
    for char in text:
        if char in ".!?" and prev_char != "":
            if prev_char not in ".!?":
                count += 1
        prev_char = char
    return count


def paragraph_count(text: str) -> int:
    """Count paragraphs separated by double newlines."""
    if not text:
        return 0
    parts = text.split("\n\n")
    return len([p for p in parts if p.strip()])
