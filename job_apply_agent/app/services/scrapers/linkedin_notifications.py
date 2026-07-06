from playwright.sync_api import Page, sync_playwright

from app.gmail.processors.url_normalizer import normalize_urls
from app.services.job_service import save_job_url
from app.services.scrapers.linkedin_scraper import login

NOTIFICATIONS_URL = "https://www.linkedin.com/notifications/"


def collect_notification_job_links(page: Page, scrolls: int = 6) -> list[str]:
    print("collect_notification_job_links entered")
    print("[1] Opening notifications page...")

    page.goto(NOTIFICATIONS_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(3000)

    print(f"[2] Current URL: {page.url}")

    if "login" in page.url or "checkpoint" in page.url:
        print("[ERROR] Login required.")
        return []

    print("[3] Scrolling notifications...")

    for i in range(scrolls):
        page.mouse.wheel(0, 1800)
        page.wait_for_timeout(1200)
        print(f"    Scroll {i + 1}/{scrolls}")

    cards = page.locator("article.nt-card")
    print(f"[4] Notification cards found: {cards.count()}")

    view_buttons = page.get_by_role("button", name="View jobs")
    print(f"[5] 'View jobs' buttons found: {view_buttons.count()}")

    # Optional: print every button text
    for i in range(view_buttons.count()):
        print(f"    Button {i}: '{view_buttons.nth(i).inner_text()}'")

    job_links = []

    index = 0

    while True:
        print(f"\n[6] Processing index {index}")

        view_buttons = page.get_by_role("button", name="View jobs")

        print(f"    Buttons currently available: {view_buttons.count()}")

        if index >= view_buttons.count():
            print("[7] No more buttons to process.")
            break

        button = view_buttons.nth(index)

        try:
            print("[8] Clicking 'View jobs'...")

            with page.expect_navigation(wait_until="domcontentloaded"):
                button.click()

            print(f"[9] Navigated to: {page.url}")

            normalized = normalize_urls([page.url])

            print(f"[10] Normalized URL: {normalized}")

            if normalized:
                job_links.append(normalized[0])
                print("[11] URL added.")

            print("[12] Going back...")
            page.go_back(wait_until="domcontentloaded")
            page.wait_for_timeout(2000)

            index += 1

        except Exception as e:
            print(f"[ERROR] Failed at index {index}: {e}")

            try:
                print("[RECOVERY] Reloading notifications...")
                page.goto(NOTIFICATIONS_URL, wait_until="domcontentloaded")
                page.wait_for_timeout(2000)

                for _ in range(scrolls):
                    page.mouse.wheel(0, 1800)
                    page.wait_for_timeout(1200)

            except Exception as ex:
                print(f"[RECOVERY ERROR] {ex}")

            index += 1

    print(f"[DONE] Collected {len(job_links)} job links.")

    return job_links


def collect_notification_job_links(page: Page, scrolls: int = 6) -> list[str]:
    print("[1] Opening notifications page...")

    page.goto(NOTIFICATIONS_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(3000)

    print(f"[2] Current URL: {page.url}")

    if "login" in page.url or "checkpoint" in page.url:
        print("[ERROR] Login required.")
        return []

    print("[3] Scrolling...")

    for i in range(scrolls):
        page.mouse.wheel(0, 1800)
        page.wait_for_timeout(1200)
        print(f"    Scroll {i + 1}/{scrolls}")

    job_links = []

    index = 0

    while True:
        cards = page.locator("article.nt-card")
        total_cards = cards.count()

        print(f"\n[4] Total cards: {total_cards}")

        if index >= total_cards:
            print("[DONE] No more cards.")
            break

        card = cards.nth(index)

        print(f"[5] Processing card {index}")

        try:
            print(card.inner_text())
        except Exception:
            pass

        # ---- Time filter ----
        try:
            time_text = (
                card.locator("p.nt-card__time-ago")
                .inner_text()
                .strip()
                .lower()
            )

            print(f"[6] Time: {time_text}")

            if time_text.endswith(("w", "mo", "y")):
                print("[STOP] Older than 3 days.")
                break

            if time_text.endswith("d"):
                days = int(time_text[:-1])
                if days > 3:
                    print("[STOP] Older than 3 days.")
                    break

        except Exception as e:
            print(f"[WARN] Couldn't read timestamp: {e}")

        # ---- Find button ----
        button = card.locator("button").filter(has_text="View jobs")

        print(f"[7] Buttons found: {button.count()}")

        if button.count() == 0:
            print("[SKIP] No View jobs button.")
            index += 1
            continue

        try:
            print("[8] Clicking View jobs...")

            with page.expect_navigation(wait_until="domcontentloaded"):
                button.first.click()

            print(f"[9] Arrived at: {page.url}")

            normalized = normalize_urls([page.url])

            print(f"[10] Normalized: {normalized}")

            if normalized:
                job_links.extend(normalized)

            print("[11] Going back...")

            page.go_back(wait_until="domcontentloaded")
            page.wait_for_timeout(2000)

        except Exception as e:
            print(f"[ERROR] {e}")

            page.goto(NOTIFICATIONS_URL, wait_until="domcontentloaded")
            page.wait_for_timeout(3000)

            for _ in range(scrolls):
                page.mouse.wheel(0, 1800)
                page.wait_for_timeout(1200)

        index += 1

    print(f"[DONE] Collected {len(job_links)} links.")

    return job_links