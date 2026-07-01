from urllib.parse import quote
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

load_dotenv(r"D:\CHATBOT\.env")

EMAIL = os.getenv("LINKEDIN_MAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")

SEARCH_KEYWORDS = [
    "AI Engineer",
    "Backend Developer"
]

LOCATION = "India"
MAX_RESULTS = 30

def scrape_jobs():

    jobs = []

    with sync_playwright() as p:

        context = p.chromium.launch_persistent_context(
        user_data_dir="./linkedin_profile",   # Creates/reuses this folder
        headless=False,
        slow_mo=500,
        viewport={"width": 1400, "height": 900},
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0.0.0 Safari/537.36"
        ),
        args=[
            "--disable-blink-features=AutomationControlled",
            "--start-maximized",
        ],
    )
        page = context.new_page()

        # -------- LOGIN --------

        page.goto("https://www.linkedin.com/login")

        print("Log in manually...")
        input("Press Enter after login...")

        context.storage_state(path="linkedin_state.json")

        # -------- SEARCH --------

        for keyword in SEARCH_KEYWORDS:

            search_url = (
                "https://www.linkedin.com/jobs/search/"
                f"?keywords={quote(keyword)}"
                f"&location={quote(LOCATION)}"
                "&f_WT=2"
                "&f_E=2,3"
            )

            print(f"\nSearching: {keyword}")

            page.goto(
                search_url,
                wait_until="domcontentloaded"
            )

            page.wait_for_timeout(8000)

            print(page.url)
            print(page.title())

            job_cards = page.locator(".base-card")

            print(page.locator(".base-card").count())
            print(page.locator("li").count())
            print(page.locator(".jobs-search-results-list").count())
            print(page.locator(".job-card-container").count())

            print(page.locator("li").first.inner_html())
            
            count = min(job_cards.count(), MAX_RESULTS)

            print(f"Found {count} jobs")

            for i in range(count):

                card = job_cards.nth(i)

                try:

                    title = card.locator(
                        ".base-search-card__title"
                    ).inner_text().strip()

                    company = card.locator(
                        ".base-search-card__subtitle"
                    ).inner_text().strip()

                    location = card.locator(
                        ".job-search-card__location"
                    ).inner_text().strip()

                    posted_date = card.locator(
                        "time"
                    ).inner_text().strip()

                    job_url = card.locator(
                        "a"
                    ).first.get_attribute("href")

                    card.click()

                    page.wait_for_timeout(3000)

                    try:
                        description = page.locator(
                            ".show-more-less-html__markup"
                        ).inner_text()
                    except:
                        description = ""

                    description_lower = description.lower()

                    experience = None

                    for year in range(6):
                        if f"{year} year" in description_lower:
                            experience = year
                            break

                    employment_type = ""

                    if "full-time" in description_lower:
                        employment_type = "Full-time"
                    elif "contract" in description_lower:
                        employment_type = "Contract"
                    elif "intern" in description_lower:
                        employment_type = "Internship"
                    elif "part-time" in description_lower:
                        employment_type = "Part-time"

                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "job_url": job_url,
                        "description": description,
                        "experience": experience,
                        "employment_type": employment_type,
                        "skills": "",
                        "match_score": 0,
                        "posted_date": posted_date,
                        "application_status": "Not Applied"
                    })

                except Exception as e:
                    print(e)

        context.close()

    return jobs