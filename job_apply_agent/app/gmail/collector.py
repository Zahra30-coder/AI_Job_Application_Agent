from app.gmail.gmail_client import get_gmail_service
from app.gmail.processors.html_parser import get_html
from app.gmail.processors.link_extractor import extract_links
from app.gmail.processors.link_filter import extract_job_links
from app.gmail.processors.url_normalizer import normalize_urls
from app.services.job_service import save_job_url


class GmailCollector:

    def __init__(self):
        self.service = get_gmail_service()

    def search_linkedin_emails(self, max_results=50):

        # Change this if needed
        query = "from:jobalerts-noreply@linkedin.com newer_than:5d"

        response = (
            self.service.users()
            .messages()
            .list(
                userId="me",
                q=query,
                maxResults=max_results
            )
            .execute()
        )

        messages = response.get("messages", [])

        print(f"\nFound {len(messages)} matching emails.\n")

        return messages

    def get_message(self, message_id):

        return (
            self.service.users()
            .messages()
            .get(
                userId="me",
                id=message_id,
                format="full"
            )
            .execute()
        )
    

    def collect_job_links(self):

        emails = self.search_linkedin_emails()

        if not emails:
            print("No LinkedIn emails found.")
            return []

        all_links = []

        for email in emails:

            print("=" * 10)
            print("Message ID:", email["id"])

            message = self.get_message(email["id"])
        
            # -----------------------------
            # Extract email headers
            # -----------------------------
            subject = ""
            sender = ""

            for header in message["payload"].get("headers", []):
                name = header["name"].lower()

                if name == "subject":
                    subject = header["value"]

                elif name == "from":
                    sender = header["value"]

            print(f"From   : {sender}")
            print(f"Subject: {subject}")

            # Only process LinkedIn Job Alert emails
            if "jobalerts-noreply@linkedin.com" not in sender.lower():
                print("⏭️ Skipping (not a LinkedIn Job Alert)\n")
                continue

            print("✅ LinkedIn Job Alert found")

            # -----------------------------
            # Extract HTML
            # -----------------------------

            html = get_html(message["payload"])

            if html is None:
                print("❌ HTML not found")
                continue

            print("✅ HTML extracted")

            # -----------------------------
            # Extract all links
            # -----------------------------

            links = extract_links(html)

            print(f"Found {len(links)} links\n")

            print("FIRST 20 LINKS:\n")

            for link in links[:20]:
                print(link)

            print("\n")

            job_links = extract_job_links(links)

            print(f"Job links after filter: {len(job_links)}")

            job_links = normalize_urls(job_links)

            for link in job_links:
                save_job_url(link, source="gmail")

            all_links.extend(job_links)

        all_links = sorted(set(all_links))

        print("\nFINAL JOB LINKS\n")

        for link in all_links:
            print(link)

        return all_links


if __name__ == "__main__":

    collector = GmailCollector()

    collector.collect_job_links()
