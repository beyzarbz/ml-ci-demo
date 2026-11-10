"""Text preprocessing functions for the CI/CD teaching demo."""


def tokenize_text(text: str) -> list[str]:
    """Convert text to lowercase whitespace-separated tokens.

    Python's ``str.split`` without an explicit separator treats consecutive
    whitespace characters as one separator and returns an empty list for an
    empty or whitespace-only string.
    """
    return text.lower().split()
