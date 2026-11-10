import pytest

from src.preprocess import tokenize_text


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello World", ["hello", "world"]),
        ("Machine   Learning", ["machine", "learning"]),
        ("Line one\nLine two", ["line", "one", "line", "two"]),
        ("", []),
        ("   ", []),
    ],
)
def test_tokenize_text(text: str, expected: list[str]) -> None:
    assert tokenize_text(text) == expected
