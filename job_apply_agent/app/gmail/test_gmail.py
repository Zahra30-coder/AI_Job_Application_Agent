from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import pickle

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

BASE_DIR = Path(__file__).parent

CLIENT_SECRET = BASE_DIR / "client_secret.json"   # Change if your filename is different
TOKEN = BASE_DIR / "token.pickle"

creds = None

if TOKEN.exists():
    with open(TOKEN, "rb") as f:
        creds = pickle.load(f)

if not creds or not creds.valid:

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET,
            SCOPES
        )
        creds = flow.run_local_server(port=0, open_browser=True)

    with open(TOKEN, "wb") as f:
        pickle.dump(creds, f)

service = build("gmail", "v1", credentials=creds)

profile = service.users().getProfile(userId="me").execute()

print("\nSUCCESS!")
print(f"Email: {profile['emailAddress']}")
print(f"Messages: {profile['messagesTotal']}")
print(f"Threads: {profile['threadsTotal']}")