from urllib.parse import urlparse, urlunparse


def normalize_url(url: str) -> str:
    """
    Remove query parameters and fragments from a URL.
    """

    parsed = urlparse(url)

    return urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            "",
            "",
            "",
        )
    )


def normalize_urls(urls: list[str]) -> list[str]:
    """
    Normalize and deduplicate URLs.
    """

    normalized = {
        normalize_url(url)
        for url in urls
    }

    return list(normalized)