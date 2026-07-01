from app.gmail.gmail_client import get_gmail_service


def search_linkedin_emails(max_results=20):
    service = get_gmail_service()

    queries = [
        "linkedin newer_than:30d",
        "from:linkedin.com newer_than:30d",
        "LinkedIn Jobs newer_than:30d",
    ]

    for query in queries:
        response = (
            service.users()
            .messages()
            .list(
                userId="me",
                q=query,
                maxResults=max_results,
            )
            .execute()
        )

        messages = response.get("messages", [])

        if messages:
            print(f"\nQuery: {query}")
            print(f"Found {len(messages)} emails")
            print(f"Found {len(response.get('messages', []))} emails")
            return messages

    return []