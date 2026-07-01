from app.gmail.search import search_linkedin_emails

emails = search_linkedin_emails()

print(f"Found {len(emails)} emails")
print("\nMessage IDs:")

for email in emails:
    print(email["id"])