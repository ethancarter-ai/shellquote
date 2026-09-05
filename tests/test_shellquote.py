import shellquote as sq


def test_quote_wraps_with_spaces():
    assert sq.quote("hello world") == "'hello world'"


def test_quote_avoids_plain_empty_string_when_unsafe():
    quoted = sq.quote("")
    assert quoted == "''"


def test_is_quoted_single_quotes():
    assert sq.is_quoted("'safe text'") is True


def test_is_quoted_double_quotes():
    assert sq.is_quoted('"safe text"') is True


def test_is_quoted_unquoted():
    assert sq.is_quoted("plain text") is False


def test_is_quoted_empty_string():
    assert sq.is_quoted("") is False


def test_normalize_removes_safe_quotes():
    assert sq.normalize("'safe'") == "safe"


def test_normalize_keeps_quotes_when_needed():
    assert sq.normalize("'hello world'") == "'hello world'"


def test_normalize_empty_inner_returns_original():
    assert sq.normalize("''") == "''"


def test_validate_args_positive():
    results = sq.validate_args(["safe", "also safe"])
    assert all(valid for _, valid, _ in results)


def test_validate_args_negative():
    results = sq.validate_args(["unsafe$var"])
    assert all(valid is False for _, valid, _ in results)


def test_validate_args_edge_case_empty():
    results = sq.validate_args([""])
    assert results[0][1] is False
