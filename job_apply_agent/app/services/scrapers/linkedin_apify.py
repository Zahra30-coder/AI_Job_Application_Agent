import os

from apify_client import ApifyClient
from dotenv import load_dotenv


load_dotenv(r"D:\CHATBOT\.env")

APIFY_TOKEN = os.getenv("APIFY_TOKEN")

if not APIFY_TOKEN:
    raise ValueError("APIFY_TOKEN not found in .env")


client = ApifyClient(APIFY_TOKEN)


SEARCH_KEYWORDS = [
    "AI Engineer",
    "Backend Developer",
]

LOCATION = "India"

MAX_RESULTS = 50

# Replace with your actor id
ACTOR_ID = "YOUR_ACTOR_ID"


def scrape_jobs():

    jobs = []

    for keyword in SEARCH_KEYWORDS:

        print(f"\nSearching: {keyword}")

        run_input = {
            "keywords": keyword,
            "location": LOCATION,
            "maxItems": MAX_RESULTS,
            "remote": True,
            "experienceLevel": [
                "ENTRY_LEVEL",
                "ASSOCIATE"
            ]
        }

        run = client.actor(
            ACTOR_ID
        ).call(
            run_input=run_input
        )

        dataset = client.dataset(
            run["defaultDatasetId"]
        )

        for item in dataset.iterate_items():

            jobs.append({

                "title": item.get("title"),

                "company": (
                    item.get("companyName")
                    or item.get("company")
                ),

                "location": item.get("location"),

                "job_url": (
                    item.get("url")
                    or item.get("jobUrl")
                ),

                "description": (
                    item.get("description")
                    or ""
                ),

                "experience": (
                    item.get("experienceLevel")
                    or item.get("experience")
                ),

                "employment_type": (
                    item.get("employmentType")
                    or ""
                ),

                "skills": (
                    ", ".join(item.get("skills", []))
                    if isinstance(item.get("skills"), list)
                    else item.get("skills", "")
                ),

                "match_score": 0,

                "posted_date": (
                    item.get("postedAt")
                    or item.get("postedDate")
                ),

                "inserted_at": None,

                "applied_at": None,

                "application_status": "Not Applied",

                "source":item.get("source")
            })

    print(f"\nCollected {len(jobs)} jobs")

    return jobs