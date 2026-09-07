import pytest

from common_helpers.type_validators import TypeValidators


@pytest.mark.parametrize(
    "email, expected",
    [
        ("simple@example.com", True),
        ("very.common@example.com", True),
        ("disposable.style.email+withletters@example.com", True),
        ("other.email-with-dash@example.com", True),
        ("x@example.com", True),
        ("user.name+tag+sorting@example.net", True),
        ("admin@subdomain.example.org", True),
        ("Abc.example.com", False),
        ("A@b@c@example.com", False),
        ("john.doe@example.", False),
    ],
)
def test_is_email(email: str, expected: bool):
    actual = TypeValidators.is_email(email)
    assert actual == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        # --- VALID URLS ---
        ("http://example.com", True),  # Basic HTTP
        ("https://example.com", True),  # Basic HTTPS
        ("https://example.co.uk", True),  # Multi-level subdomains
        ("https://example.com/", True),  # Trailing slash
        ("https://example.compath/to/resource", True),  # Simple path
        ("https://example.com:8080", True),  # Custom port number
        ("https://example.compage.html", True),  # File extension in path
        (
            "https://example.com/search&q=pytest&lang=en",
            True,
        ),  # Query parameters
        ("https://example.com/home#profile-section", True),  # Fragment anchor
        # --- INVALID URLS ---
        ("example.com", False),  # Missing protocol scheme
        ("https:/example.com", False),  # Malformed protocol (missing slash)
        ("ftp://example.com", False),  # Unsupported protocol (FTP)
        ("https://example.com:abc", False),  # Non-numeric port
        ("https://", False),  # Empty host address
        ("://example.com", False),  # Empty protocol scheme
        ("https:// exam ple.com", False),  # Whitespace characters inside domain
    ],
)
def test_is_url(url: str, expected: bool):
    actual = TypeValidators.is_url(url)
    assert actual == expected
