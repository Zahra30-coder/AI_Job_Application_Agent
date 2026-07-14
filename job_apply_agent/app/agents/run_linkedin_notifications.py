from playwright.sync_api import sync_playwright

from app.services.scrapers.linkedin_notifications import (
    collect_notification_job_links,
)

def main():

    with sync_playwright() as p:

        context = p.chromium.launch_persistent_context(
            user_data_dir="./linkedin_profile",
            headless=False,
        )

        page = context.new_page()

        try:

            collected_urls = (
                collect_notification_job_links(
                    page=page,
                    scrolls=6
                )
            )

            print(
                f"\nCollected "
                f"{len(collected_urls)} URLs"
            )

            for url in collected_urls:
                print(url)

        finally:

            context.close()


if __name__ == "__main__":
    main()