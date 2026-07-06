from playwright.sync_api import sync_playwright

from app.services.scrapers.linkedin_notifications import (
    collect_notification_job_links,
)

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir="./linkedin_profile",
        headless=False,
    )

    page = context.new_page()

    links = collect_notification_job_links(page)

    print(links)

    context.close()