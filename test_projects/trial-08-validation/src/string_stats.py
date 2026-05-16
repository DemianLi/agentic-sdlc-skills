"""String Stats Library

Provides functions for text analysis:
- word_count: Count words in a string
- char_count: Count characters (excluding whitespace)
- sentence_count: Count sentences (ending in .!?)
- paragraph_count: Count paragraphs (separated by \\n\\n)
"""


def word_count(text):
    """Count words in text.

    Args:
        text: Input string

    Returns:
        Number of words
    """
    if not text or not text.strip():
        return 0
    return len(text.split())


def char_count(text):
    """Count characters in text, excluding whitespace.

    Args:
        text: Input string

    Returns:
        Number of non-whitespace characters
    """
    return len(text.replace(" ", "").replace("\n", "").replace("\t", ""))


def sentence_count(text):
    """Count sentences in text.

    A sentence ends with . ! or ?

    Args:
        text: Input string

    Returns:
        Number of sentences
    """
    if not text:
        return 0
    count = 0
    in_punctuation = False
    for char in text:
        if char in ".!?":
            if not in_punctuation:
                count += 1
                in_punctuation = True
        else:
            in_punctuation = False
    return count


def paragraph_count(text):
    """Count paragraphs in text.

    Paragraphs are separated by double newlines (\\n\\n).

    Args:
        text: Input string

    Returns:
        Number of paragraphs
    """
    if not text or not text.strip():
        return 0
    paragraphs = text.split("\n\n")
    return len([p for p in paragraphs if p.strip()])
