import base64

from app.gmail.gmail_client import get_gmail_service


def get_message(message_id):
    service = get_gmail_service()

    return (
        service.users()
        .messages()
        .get(
            userId="me",
            id=message_id,
            format="full"
        )
        .execute()
    )