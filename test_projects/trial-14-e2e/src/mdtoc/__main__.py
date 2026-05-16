"""CLI entry point: python -m mdtoc generate <file> [--max-level N] [--in-place]"""
import argparse
import sys
from pathlib import Path
from .core import parse_headers, generate_toc, insert_toc


def cmd_generate(args):
    path = Path(args.file)
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: permission denied: {args.file}", file=sys.stderr)
        sys.exit(1)

    headers = parse_headers(text)
    toc = generate_toc(headers, max_level=args.max_level)
    result = insert_toc(text, toc)

    if args.in_place:
        path.write_text(result, encoding="utf-8")
    else:
        print(result, end="")


def main():
    parser = argparse.ArgumentParser(
        prog="mdtoc",
        description="Generate and insert a Table of Contents into Markdown files.",
    )
    sub = parser.add_subparsers(dest="command")

    gen = sub.add_parser("generate", help="Insert or update TOC in a Markdown file")
    gen.add_argument("file", help="Path to the Markdown file")
    gen.add_argument("--max-level", type=int, default=3, metavar="N",
                     help="Maximum heading level to include (default: 3)")
    gen.add_argument("--in-place", action="store_true",
                     help="Overwrite the file instead of writing to stdout")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if args.command == "generate":
        if not 1 <= args.max_level <= 6:
            print("Error: --max-level must be between 1 and 6", file=sys.stderr)
            sys.exit(1)
        cmd_generate(args)


if __name__ == "__main__":
    main()
