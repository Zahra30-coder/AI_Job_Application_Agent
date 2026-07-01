from urllib.parse import urlparse


KEYWORDS = [
    "/jobs/",
    "/jobs/view/",
    "/comm/jobs/",
    "/e/v2",
    "jobs/view",
    "currentJobId",
]


def extract_job_links(links: list[str]) -> list[str]:
    """
    Extract LinkedIn job-related URLs from a list of links.
    """

    job_links = []

    for link in links:

        if not link:
            continue

        parsed = urlparse(link)

        domain = parsed.netloc.lower()
        path = parsed.path.lower()
        query = parsed.query.lower()

        # Only consider LinkedIn URLs
        if "linkedin.com" not in domain:
            continue

        # Keep URLs that look job-related
        if any(keyword in path or keyword in query for keyword in KEYWORDS):
            job_links.append(link)

    # Remove duplicates while preserving order
    seen = set()
    unique_links = []

    for link in job_links:
        if link not in seen:
            seen.add(link)
            unique_links.append(link)

    return unique_links