from playwright.sync_api import Page
from app.services.job_service import save_job
from app.agents.job_collector import LinkedInCollector
from app.gmail.processors.url_normalizer import normalize_urls
import traceback

NOTIFICATIONS_URL = "https://www.linkedin.com/notifications/?filter=jobs_all"

MAX_NOTIFICATIONS = 20
MAX_PAGES = 3
MAX_JOBS = 50


def apply_remote_filter(page: Page):

    print("\n[INFO] Applying Remote filter...")

    try:

        page.wait_for_timeout(5000)

        remote_buttons = page.locator(
            "button"
        ).filter(
            has_text="Remote"
        )

        print(
            f"[DEBUG] Remote buttons: "
            f"{remote_buttons.count()}"
        )

        if remote_buttons.count() == 0:

            print(
                "[WARN] Remote filter "
                "not found."
            )

            return

        remote_buttons.first.click()

        page.wait_for_timeout(2000)

        show_results = page.get_by_role(
            "button"
        ).filter(
            has_text="Show results"
        )

        if show_results.count():

            show_results.first.click()

            page.wait_for_timeout(
                5000
            )

        print(
            "[OK] Remote filter applied."
        )

    except Exception as e:

        print(
            f"[FILTER ERROR] {e}"
        )


def save_job_url(
    job_url: str,
    processed_urls: set
):

    if not job_url:
        return False

    if job_url.startswith("/"):

        job_url = (
            "https://www.linkedin.com"
            + job_url
        )

    job_url = job_url.split("?")[0]

    normalized = normalize_urls(
        [job_url]
    )

    if not normalized:
        return False

    job_url = normalized[0]

    if "/jobs/view/" not in job_url:
        return False

    if job_url in processed_urls:
        return False

    processed_urls.add(job_url)

    inserted = save_job(
        title="",
        company="",
        location="",
        job_url=job_url,
        description="",
        experience="",
        employment_type="",
        skills="",
        match_score=0,
        posted_date="",
        source="linkedin_notifications"
    )

    if inserted:

        print(
            f"[SAVED] {job_url}"
        )

    return inserted


def scrape_jobs_from_results(
    page: Page,
    processed_urls: set
):

    saved_count = 0
    print("A")
    try:
        apply_remote_filter(page)
    except Exception:
        traceback.print_exc()
        raise
    print("B")

    for page_no in range(1, MAX_PAGES + 1):
        print("C")

        try:

            print(
                f"\n========== "
                f"PAGE {page_no} "
                f"=========="
            )

            page.wait_for_timeout(5000)
            print("D")

            cards = page.locator(
                ".scaffold-layout__list-item"
            )

            if cards.count() == 0:

                cards = page.locator(
                    ".job-card-container"
                )
            
            print("E")
            total_jobs = cards.count()
            print("F")

            print(
                f"[INFO] Found "
                f"{total_jobs} jobs"
            )

            for i in range(
                total_jobs
            ):

                if (
                    saved_count
                    >= MAX_JOBS
                ):

                    print(
                        f"[LIMIT] "
                        f"{MAX_JOBS} jobs "
                        f"saved."
                    )

                    return saved_count

                try:

                    cards = page.locator(
                        ".scaffold-layout__list-item"
                    )

                    if cards.count() == 0:

                        cards = page.locator(
                            ".job-card-container"
                        )

                    if i >= cards.count():
                        break

                    card = cards.nth(i)

                    card.scroll_into_view_if_needed()

                    page.wait_for_timeout(
                        1000
                    )

                    card.click()

                    page.wait_for_timeout(
                        6000
                    )

                    job_url = None

                    title_link = page.locator(
                        "a.jobs-unified-top-card__job-title"
                    )

                    if title_link.count():

                        job_url = (
                            title_link.first
                            .get_attribute(
                                "href"
                            )
                        )

                    if not job_url:

                        links = page.locator(
                            "a[href*='/jobs/view/']"
                        )

                        for j in range(
                            links.count()
                        ):

                            href = (
                                links.nth(j)
                                .get_attribute(
                                    "href"
                                )
                            )

                            if (
                                href
                                and "/jobs/view/"
                                in href
                            ):

                                job_url = href
                                break

                    if not job_url:
                        continue

                    if save_job_url(
                        job_url,
                        processed_urls
                    ):
                        saved_count += 1

                except Exception as e:

                    print(
                        f"[JOB ERROR] "
                        f"{e}"
                    )

            if page_no == MAX_PAGES:
                break

            try:

                next_button = page.get_by_role(
                    "button"
                ).filter(
                    has_text=str(
                        page_no + 1
                    )
                )

                if next_button.count():

                    print(
                        f"\nOpening page "
                        f"{page_no + 1}"
                    )

                    next_button.first.click()

                    page.wait_for_timeout(
                        5000
                    )

                else:

                    print(
                        "[STOP] No next page."
                    )

                    break

            except Exception as e:

                print(
                    f"[PAGE ERROR] "
                    f"{e}"
                )

                break

        except Exception as e:

            print(
                f"[PAGE {page_no} "
                f"ERROR] {e}"
            )

            continue

    return saved_count


def collect_notification_job_links(
    page: Page,
    scrolls: int = 6
):
    print("VERSION-2026-07-14")
    print("[1] Opening notifications page...")

    page.goto(
        NOTIFICATIONS_URL,
        wait_until="domcontentloaded"
    )

    page.wait_for_timeout(5000)

    if (
        "login" in page.url
        or "checkpoint" in page.url
    ):

        print(
            "[ERROR] Login required."
        )

        return []

    print(
        "[2] Scrolling notifications..."
    )

    for _ in range(scrolls):

        page.mouse.wheel(
            0,
            1800
        )

        page.wait_for_timeout(
            1200
        )

    cards = page.locator(
        "article.nt-card"
    )

    total_cards = min(
        cards.count(),
        MAX_NOTIFICATIONS
    )

    print(
        f"[4] Notification cards found: "
        f"{total_cards}"
    )

    processed_urls = set()
    saved_count = 0

    for idx in range(
        total_cards
    ):

        try:

            cards = page.locator(
                "article.nt-card"
            )

            if idx >= cards.count():
                break

            card = cards.nth(idx)

            headline = card.locator(
                "a.nt-card__headline"
            )

            if headline.count() == 0:
                continue

            text = (
                headline.first
                .inner_text()
                .lower()
            )

            if (
                "hiring" not in text
                and "apply" not in text
            ):

                continue

            href = (
                headline.first
                .get_attribute(
                    "href"
                )
            )

            if not href:
                continue

            if href.startswith("/"):

                href = (
                    "https://www.linkedin.com"
                    + href
                )

            print(
                f"\nOpening notification "
                f"{idx + 1}"
            )

            page.goto(
                href,
                wait_until="domcontentloaded"
            )

            page.wait_for_timeout(
                8000
            )

            print(
                f"[OPENED] "
                f"{page.url}"
            )

            saved_count += (
                scrape_jobs_from_results(
                    page,
                    processed_urls
                )
            )

            print(
                "\nReturning to "
                "notifications..."
            )

            page.goto(
                NOTIFICATIONS_URL,
                wait_until="domcontentloaded"
            )

            page.wait_for_timeout(
                5000
            )

            for _ in range(scrolls):

                page.mouse.wheel(
                    0,
                    1800
                )

                page.wait_for_timeout(
                    1200
                )

        except Exception as e:

            print(
                f"[ERROR] Notification "
                f"{idx + 1}: {e}"
            )
            traceback.print_exc()

            try:

                saved_count += (
                    scrape_jobs_from_results(
                        page,
                        processed_urls
                    )
                )

            except Exception as e:

                print(
                    f"[SCRAPE ERROR] {e}"
                )

                continue

    print(
        f"\n[DONE] Saved "
        f"{saved_count} jobs."
    )

    print(
        f"[DONE] Collected "
        f"{len(processed_urls)} "
        f"unique URLs."
    )

    if saved_count > 0:

        print(
            "\nStarting enrichment "
            "pipeline..."
        )

        LinkedInCollector().enrich_jobs()

    return list(processed_urls)
def scrape_jobs_from_results(page: Page,processed_urls: set,) -> int:

    saved_count = 0

    print("\n[INFO] Applying Remote filter...")

    try:

        remote_btn = page.locator(
            "#searchFilter_workplaceType"
        )

        if remote_btn.count():

            remote_btn.first.click()

            page.wait_for_timeout(1500)

            remote_checkbox = page.locator(
                "#workplaceType-2"
            )

            if remote_checkbox.count():

                try:

                    if not remote_checkbox.is_checked():
                        remote_checkbox.check()

                except Exception:
                    pass

            show_results = page.get_by_role(
                "button",
                name="Show results"
            )

            if show_results.count():
                show_results.last.click()

            page.wait_for_load_state(
                "networkidle"
            )

            page.wait_for_timeout(
                5000
            )

            print(
                "[OK] Remote filter applied."
            )

    except Exception as e:

        print(
            f"[FILTER ERROR] {e}"
        )

    # ===================================
    # SCRAPE 3 PAGES
    # ===================================

    for page_no in range(1, 4):

        print(
            f"\n========== PAGE {page_no} =========="
        )

        page.wait_for_load_state(
            "networkidle"
        )

        page.wait_for_timeout(
            5000
        )

        job_cards = page.locator(
            ".job-card-container"
        )

        if job_cards.count() == 0:

            job_cards = page.locator(
                ".scaffold-layout__list-item"
            )

        total_jobs = job_cards.count()

        print(
            f"[INFO] Found "
            f"{total_jobs} jobs"
        )

        for i in range(total_jobs):

            try:

                cards = page.locator(
                    ".job-card-container"
                )

                if cards.count() == 0:

                    cards = page.locator(
                        ".scaffold-layout__list-item"
                    )

                if i >= cards.count():
                    break

                card = cards.nth(i)

                try:

                    title = (
                        card.inner_text()
                        .strip()
                    )

                    print(
                        f"\n[{i+1}] "
                        f"{title[:100]}"
                    )

                except Exception:
                    pass

                card.click()

                page.wait_for_timeout(
                    2500
                )

                job_url = None

                try:

                    title_link = page.locator(
                        "a.jobs-unified-top-card__job-title"
                    )

                    if title_link.count():

                        job_url = (
                            title_link.first
                            .get_attribute(
                                "href"
                            )
                        )

                except Exception:
                    pass

                if not job_url:

                    links = page.locator(
                        "a[href*='/jobs/view/']"
                    )

                    for j in range(
                        links.count()
                    ):

                        href = (
                            links.nth(j)
                            .get_attribute(
                                "href"
                            )
                        )

                        if (
                            href
                            and "/jobs/view/"
                            in href
                        ):

                            job_url = href
                            break

                if not job_url:
                    continue

                if job_url.startswith("/"):

                    job_url = (
                        "https://www.linkedin.com"
                        + job_url
                    )

                job_url = (
                    job_url.split("?")[0]
                )

                normalized = normalize_urls(
                    [job_url]
                )

                if not normalized:
                    continue

                job_url = normalized[0]

                if (
                    "/jobs/view/"
                    not in job_url
                ):
                    continue

                if (
                    job_url
                    in processed_urls
                ):
                    continue

                processed_urls.add(
                    job_url
                )

                try:

                    inserted = save_job(
                        title="",
                        company="",
                        location="",
                        job_url=job_url,
                        description="",
                        experience="",
                        employment_type="",
                        skills="",
                        match_score=0,
                        posted_date="",
                        source="linkedin_notifications"
                    )

                    if inserted:

                        saved_count += 1

                        print(
                            f"[SAVED] "
                            f"{job_url}"
                        )

                except Exception as e:

                    print(
                        f"[SAVE ERROR] "
                        f"{job_url} -> {e}"
                    )

            except Exception as e:

                print(
                    f"[JOB ERROR] "
                    f"{e}"
                )

        # ===================================
        # NEXT PAGE
        # ===================================

        if page_no == 3:
            break

        try:

            pagination_buttons = page.locator(
                "button.artdeco-pagination__indicator"
            )

            if (
                pagination_buttons.count()
                > page_no
            ):

                print(
                    f"\nOpening page "
                    f"{page_no + 1}"
                )

                pagination_buttons.nth(
                    page_no
                ).click()

                page.wait_for_load_state(
                    "networkidle"
                )

                page.wait_for_timeout(
                    5000
                )

            else:

                print(
                    "[STOP] No more pages."
                )

                break

        except Exception as e:

            print(
                f"[PAGE ERROR] {e}"
            )

            break

    return saved_count

#-----------------------------------------
def collect_notification_job_links(
    page: Page,
    scrolls: int = 6
):

    print("[1] Opening notifications page...")

    page.goto(
        NOTIFICATIONS_URL,
        wait_until="domcontentloaded"
    )

    page.wait_for_timeout(5000)

    if (
        "login" in page.url
        or "checkpoint" in page.url
    ):
        print("[ERROR] Login required.")
        return []

    print("[2] Scrolling notifications...")

    for _ in range(scrolls):

        page.mouse.wheel(
            0,
            1800
        )

        page.wait_for_timeout(
            1200
        )

    cards = page.locator(
        "article.nt-card"
    )

    print(
        f"[4] Notification cards found: "
        f"{cards.count()}"
    )

    processed_urls = set()
    saved_count = 0

    for idx in range(cards.count()):

        try:

            cards = page.locator(
                "article.nt-card"
            )

            if idx >= cards.count():
                break

            card = cards.nth(idx)

            view_button = card.locator(
                "button[role='link']"
            )

            if view_button.count() == 0:

                print(
                    f"[SKIP] Card "
                    f"{idx+1} has no "
                    f"View Jobs button."
                )

                continue

            print(
                f"\nOpening notification "
                f"{idx + 1}"
            )

            view_button.first.scroll_into_view_if_needed()

            page.wait_for_timeout(
                1000
            )

            view_button.first.click()

            page.wait_for_load_state(
                "networkidle"
            )

            page.wait_for_timeout(
                5000
            )

            print(
                f"[OPENED] {page.url}"
            )

            saved_count += (
                scrape_jobs_from_results(
                    page,
                    processed_urls
                )
            )

            print(
                "\nReturning to notifications..."
            )

            page.goto(
                NOTIFICATIONS_URL,
                wait_until="domcontentloaded"
            )

            page.wait_for_timeout(
                5000
            )

            for _ in range(scrolls):

                page.mouse.wheel(
                    0,
                    1800
                )

                page.wait_for_timeout(
                    1200
                )

        except Exception as e:

            print(
                f"[ERROR] Notification "
                f"{idx + 1}: {e}"
            )

            try:

                page.goto(
                    NOTIFICATIONS_URL,
                    wait_until="domcontentloaded"
                )

                page.wait_for_timeout(
                    5000
                )

                for _ in range(scrolls):

                    page.mouse.wheel(
                        0,
                        1800
                    )

                    page.wait_for_timeout(
                        1200
                    )

            except Exception:
                pass

    print(
        f"\n[DONE] Saved "
        f"{saved_count} jobs."
    )

    print(
        f"[DONE] Collected "
        f"{len(processed_urls)} "
        f" unique URLs."
    )

    if saved_count > 0:

        print(
            "\nStarting enrichment "
            "pipeline..."
        )

        LinkedInCollector().enrich_jobs()

    return list(processed_urls)