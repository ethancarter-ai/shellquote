# shellquote

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/licenses/MIT)

**shellquote** normalizes, quotes, and validates shell arguments from the command line. It helps prevent quoting bugs, injection issues, and inconsistent shell argument handling across POSIX shells.

## About

Shell quoting is surprisingly error-prone. A single unquoted space or an unexpected character can turn a safe command into a broken one, or worse, a security issue. `shellquote` gives developers, DevOps engineers, and security tooling authors a small but precise utility to:

- Quote arbitrary strings for safe reuse in POSIX shell commands.
- Detect whether a command line is already properly shell-quoted.
- Normalize quoted strings by removing unnecessary quoting while preserving meaning.

This is useful for generating wrapper scripts, building CLI tooling that shells out, auditing command histories, and teaching safe shell habits.

## Features

- `quote` — shell-quote a single argument with POSIX-safe quoting.
- `is_quoted` — detect whether a string is already properly quoted.
- `normalize` — remove unnecessary quoting from an argument while preserving meaning.
- `validate_args` — validate a list of arguments and report quoting issues.
- CLI with multiple output formats: `plain`, `markdown`, and `json`.

## Installation

```bash
python -m pip install -e .
```

## Usage

```bash
shellquote --help

# Quote an argument
shellquote quote 'hello world'
# -> 'hello world'

# Detect quoting
shellquote is-quoted "'already quoted'"
# -> true

# Normalize
shellquote normalize "'overquoted'"
# -> overquoted

# Validate multiple arguments
shellquote validate foo bar 'baz qux'
# -> ok
```

## Project Structure

```text
├── .github/
│   └── workflows/
│       └── tests.yml
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
├── shellquote.py
└── tests/
    └── test_shellquote.py
```

## Tags / Keywords

`shell`, `quoting`, `cli`, `security`, `devtools`, `python`, `posix`

Source: https://github.com/ethancarter-ai/shellquote

## License

MIT
