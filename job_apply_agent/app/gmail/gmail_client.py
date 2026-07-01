from pathlib import Path
import pickle

from googleapiclient.discovery import build


BASE_DIR = Path(__file__).parent
TOKEN_FILE = BASE_DIR / "token.pickle"


def get_gmail_service():
    with open(TOKEN_FILE, "rb") as f:
        creds = pickle.load(f)

    return build("gmail", "v1", credentials=creds)