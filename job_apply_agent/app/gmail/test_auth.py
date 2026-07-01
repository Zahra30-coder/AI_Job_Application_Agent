from googleapiclient.discovery import build

from auth import authenticate

creds = authenticate()

service = build("gmail", "v1", credentials=creds)

profile = service.users().getProfile(userId="me").execute()

print(profile)