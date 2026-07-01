from pathlib import Path
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]

BASE_DIR = Path(__file__).parent

CLIENT_SECRET_FILE = BASE_DIR / "client_secret.json"    
TOKEN_FILE = BASE_DIR / "token.pickle"


def authenticate():
    creds = None

    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE,
                SCOPES,
            )

            creds = flow.run_local_server(port=0, open_browser=True)

        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    return creds