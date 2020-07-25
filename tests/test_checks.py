from flake8_multiline_containers import ErrorCode


def test_check_opening_contains_error(linter):
    linter._check_opening('{', '}', 0, "foo={a\n", ErrorCode.JS101)
    assert 1 == len(linter.errors)


def test_check_opening_no_error(linter):
    linter._check_opening('{', '}', 0, "foo={\n", ErrorCode.JS101)
    assert 0 == len(linter.errors)
