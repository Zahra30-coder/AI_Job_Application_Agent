import base64

def get_html(payload):
    """
    Recursively extract the HTML part from a Gmail message payload.
    """

    # Case 1: Current part is HTML
    if payload.get("mimeType") == "text/html":
        body = payload.get("body", {})

        if "data" in body:
            return base64.urlsafe_b64decode(
                body["data"]
            ).decode("utf-8", errors="ignore")

    # Case 2: Search nested parts
    for part in payload.get("parts", []):
        html = get_html(part)

        if html:
            return html

    return None

