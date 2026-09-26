from __future__ import annotations

import argparse
import json
import shlex
import sys
from typing import Iterable, List, Optional, Sequence, Tuple

__all__ = [
    "quote",
    "is_quoted",
    "normalize",
    "validate_args",
    "main",
]

QuoteReturn = str
ValidationResult = Tuple[str, bool, Optional[str]]


def quote(arg: str) -> str:
    """Return a POSIX shell-safe quoted form of *arg*.

    This mirrors :func:`shlex.quote` behavior so tool authors have a
    single stable surface for quoting.
    """
    return shlex.quote(arg)


def is_quoted(arg: str) -> bool:
    """Return ``True`` if *arg* looks like a POSIX single-quoted or double-quoted string.

    The heuristic checks for matching, non-empty outer quoting rather than full
    shell syntax correctness.
    """
    if not arg:
        return False

    for quote_char in ('"', "'"):
        if len(arg) >= 2 and arg.startswith(quote_char) and arg.endswith(quote_char):
            if arg.count(quote_char) == 2:
                return True

    return False


def normalize(arg: str) -> str:
    """Remove unnecessary outer quoting from *arg*.

    If the string is wrapped in matching quotes and contains no shell-sensitive
    characters that require escaping, return the inner text. Otherwise return
    the original string unchanged.
    """
    if not is_quoted(arg):
        return arg

    inner = arg[1:-1]
    if not inner or not inner.strip():
        return arg

    if any(ch in inner for ch in (' ', '\t', '\\', '$', '&', '|', ';', '<', '>', '`', '*')):
        return arg

    return inner


def validate_args(args: Iterable[str]) -> List[ValidationResult]:
    """Validate shell quoting for *args* and return per-argument findings.

    Each item is ``(arg, is_valid, issue)``.
    """
    results: List[ValidationResult] = []

    for arg in args:
        if not arg:
            issue = "empty arguments can be unsafe"
            results.append((arg, False, issue))
            continue

        if any(ch in arg for ch in ('\\', '`', '$')):
            if not is_quoted(arg):
                issue = "argument contains shell-sensitive characters without quoting"
                results.append((arg, False, issue))
                continue

        results.append((arg, True, None))

    return results


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shellquote",
        description="Normalize, quote, and validate shell arguments.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    quote_parser = subparsers.add_parser("quote", help="quote an argument")
    quote_parser.add_argument("arg", help="argument to quote")

    is_quoted_parser = subparsers.add_parser("is-quoted", help="check quoting")
    is_quoted_parser.add_argument("arg", help="argument to inspect")

    normalize_parser = subparsers.add_parser("normalize", help="normalize quoting")
    normalize_parser.add_argument("arg", help="argument to normalize")

    validate_parser = subparsers.add_parser("validate", help="validate arguments")
    validate_parser.add_argument("args", nargs="+", help="arguments to validate")
    validate_parser.add_argument(
        "--format",
        choices=("plain", "markdown", "json"),
        default="plain",
        help="output format",
    )

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _build_parser().parse_args(list(argv) if argv is not None else None)

    if args.command == "quote":
        print(quote(args.arg))
    elif args.command == "is-quoted":
        print(str(is_quoted(args.arg)).lower())
    elif args.command == "normalize":
        print(normalize(args.arg))
    elif args.command == "validate":
        results = validate_args(args.args)
        fmt = getattr(args, "format", "plain")
        if fmt == "plain":
            for arg, valid, issue in results:
                if valid:
                    print(f"ok: {arg}")
                else:
                    print(f"error: {arg} -- {issue}")
        elif fmt == "markdown":
            print("| arg | valid | issue |")
            print("| --- | --- | --- |")
            for arg, valid, issue in results:
                issue_text = issue or ""
                print(f"| `{arg}` | {'true' if valid else 'false'} | {issue_text} |")
        elif fmt == "json":
            payload = [
                {"arg": arg, "valid": valid, "issue": issue}
                for arg, valid, issue in results
            ]
            print(json.dumps(payload))

    return 0


if __name__ == "__main__":
    sys.exit(main())
