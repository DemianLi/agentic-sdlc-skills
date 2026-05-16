"""slugify: Convert text to URL-safe slugs."""


def slugify(text: str, separator: str = "-") -> str:
    """
    Convert text to a URL-safe slug.

    Args:
        text: Input string (any content, including empty)
        separator: Character to replace whitespace (default: "-")

    Returns:
        URL-safe slug: lowercase ASCII [a-z0-9] + separator characters

    Algorithm (applied in order):
        1. Convert text to lowercase
        2. Replace whitespace (space, tab, newline) with separator
        3. Remove characters not in [a-z0-9<separator>]

    Examples:
        >>> slugify("Hello World")
        'hello-world'
        >>> slugify("Héllo & Wörld!", separator="_")
        'hllo__wrld'
        >>> slugify("  a  b  ")
        '--a--b--'
        >>> slugify("!!!")
        ''
    """
    # Step 1: Convert to lowercase
    text = text.lower()

    # Step 2: Replace whitespace with separator
    # Handle space, tab, newline, and other whitespace
    result = []
    for char in text:
        if char.isspace():
            result.append(separator)
        else:
            result.append(char)
    text = "".join(result)

    # Step 3: Keep only [a-z0-9<separator>]
    result = []
    for char in text:
        if (char >= 'a' and char <= 'z') or (char >= '0' and char <= '9') or char == separator:
            result.append(char)

    return "".join(result)


__all__ = ["slugify"]
__version__ = "1.0.0"
