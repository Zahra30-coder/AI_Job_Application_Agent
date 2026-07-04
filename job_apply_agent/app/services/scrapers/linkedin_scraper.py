from urllib.parse import quote
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
from app.services.job_service import get_unscraped_jobs,  update_job


load_dotenv(r"D:\CHATBOT\.env")

EMAIL = os.getenv("LINKEDIN_MAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")

SEARCH_KEYWORDS = [
    "AI Engineer",
    "Backend Developer"
]

LOCATION = "India"
MAX_RESULTS = 30


# ------------------------
# Browser
# ------------------------

def create_browser():

    playwright = sync_playwright().start()

    context = playwright.chromium.launch_persistent_context(
        user_data_dir="./linkedin_profile",
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

    return playwright, context, page

# ------------------------
# Login
# ------------------------

def login(page, context):

    page.goto("https://www.linkedin.com/login")

    print("Log in manually...")
    input("Press Enter after login...")

    context.storage_state(path="linkedin_state.json")


# ------------------------
# Scrape ONE job
# ------------------------

from playwright.sync_api import Page


def scrape_job(page: Page, job_url: str):

    print(f"\nScraping: {job_url}")

    page.goto(job_url, wait_until="domcontentloaded")
    page.wait_for_selector("h2:has-text('About the job')", timeout=15000)
    page.wait_for_timeout(5000)

    header = extract_header(page)
    description = extract_description(page)
    job_details = extract_job_details(page)
    easy_apply = extract_easy_apply(page)
    skills = extract_skills(description)

    return {
        "title": header["title"],
        "company": header["company"],
        "location": header["location"],
        "posted_date": header["posted_date"],
        "applicants": header["applicants"],

        "description": description,

        "experience": job_details["experience"],
        "employment_type": job_details["employment_type"],
        "remote": job_details["remote"],
        "job_status": job_details["job_status"],

        "easy_apply": easy_apply,

        "skills": ", ".join(skills)
    }


def extract_header(page: Page):

    header = {
        "title": "",
        "company": "",
        "location": "",
        "posted_date": "",
        "applicants": ""
    }

    try:
        header["title"] = page.locator("h1").first.inner_text().strip()
    except:
        pass

    try:
        header["company"] = page.locator(
            'a[href*="/company/"]'
        ).first.inner_text().strip()
    except:
        pass

    try:
        metadata = page.locator(
            "p:has-text('ago')"
        ).first.inner_text()

        parts = [x.strip() for x in metadata.split("·")]

        if len(parts) >= 1:
            header["location"] = parts[0]

        if len(parts) >= 2:
            header["posted_date"] = parts[1]

        if len(parts) >= 3:
            header["applicants"] = parts[2]

    except:
        pass

    return header


def extract_description(page: Page):

    try:

        return page.locator(
            '[data-testid="expandable-text-box"]'
        ).inner_text().strip()

    except:

        return ""
import re

import re

def extract_experience(description: str):

    if not description:
        return ""

    description = description.lower()

    patterns = [
        r"\d+\s*\+\s*years?",
        r"\d+\s*-\s*\d+\s*years?",
        r"\d+\s*to\s*\d+\s*years?",
        r"\d+\s*years?"
    ]

    for pattern in patterns:
        match = re.search(pattern, description)
        if match:
            return match.group().strip()

    # Fallback
    for year in range(6):
        if f"{year} year" in description or f"{year} years" in description:
            return f"{year} years"

    return ""

def extract_job_details(page: Page):

    details = {
        "employment_type": "",
        "experience": "",
        "remote": False,
        "job_status": "Open"
    }

    text = page.locator("body").inner_text().lower()

    if "remote" in text:
        details["remote"] = True

    if "full-time" in text:
        details["employment_type"] = "Full-time"

    elif "contract" in text:
        details["employment_type"] = "Contract"

    elif "internship" in text:
        details["employment_type"] = "Internship"

    elif "part-time" in text:
        details["employment_type"] = "Part-time"

    if "entry level" in text:
        details["experience"] = "Entry level"

    elif "associate" in text:
        details["experience"] = "Associate"

    elif "mid-senior" in text:
        details["experience"] = "Mid-Senior"

    elif "director" in text:
        details["experience"] = "Director"

    elif "executive" in text:
        details["experience"] = "Executive"

    if "no longer accepting applications" in text:
        details["job_status"] = "Closed"

    return details


def extract_easy_apply(page: Page):

    return page.locator(
        "button:has-text('Easy Apply')"
    ).count() > 0


def extract_skills(description: str):

    skills = []

    keywords = [
        "Python",
        "FastAPI",
        "Flask",
        "Django",
        "React",
        "Next.js",
        "JavaScript",
        "TypeScript",
        "Docker",
        "Kubernetes",
        "Azure",
        "AWS",
        "GCP",
        "Redis",
        "PostgreSQL",
        "MySQL",
        "MongoDB",
        "LLM",
        "OpenAI",
        "Gemini",
        "LangChain",
        "CrewAI",
        "RAG",
        "MCP",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "PyTorch",
        "n8n",
        "automation"
    ]

    lower = description.lower()

    for skill in keywords:

        if skill.lower() in lower:
            skills.append(skill)

    return skills