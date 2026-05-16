"""CLI entry point for slugify."""
import sys
import argparse
from slugify import slugify


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Convert text to a URL-safe slug",
        prog="python -m slugify",
    )
    parser.add_argument(
        "text",
        nargs="?",
        default=None,
        help="Text to slugify (if absent, reads from stdin)",
    )
    parser.add_argument(
        "--separator",
        default="-",
        help="Character to replace whitespace (default: -)",
    )

    args = parser.parse_args()

    # Determine input: TEXT or stdin
    if args.text is not None:
        text = args.text
    else:
        text = sys.stdin.read()

    # Strip trailing newline if present (from stdin)
    if text.endswith("\n"):
        text = text[:-1]

    # Slugify
    slug = slugify(text, separator=args.separator)

    # Output and exit code
    if slug:
        print(slug)
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
