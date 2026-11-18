from api.routes import _LOGGED_BODY_MAX_LENGTH, _truncate


def test_truncate_cuts_long_body_and_gives_its_length():
    assert _truncate(b"a" * (_LOGGED_BODY_MAX_LENGTH + 1)) == (
        f"{'a' * _LOGGED_BODY_MAX_LENGTH}… ({_LOGGED_BODY_MAX_LENGTH + 1} chars)"
    )
