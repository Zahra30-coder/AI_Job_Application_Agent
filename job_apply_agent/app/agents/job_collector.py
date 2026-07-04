from app.services.scrapers.linkedin_scraper import scrape_job, create_browser, login, scrape_job
from app.services.job_service import save_job, get_unscraped_jobs, update_job
from playwright.sync_api import sync_playwright

#del jobs.db
#python -m app.database.init_db
#python -m app.agents.run_collector

class LinkedInCollector:

    def __init__(self):
        self.context = None
        self.page = None
            
    def collect_jobs():
        jobs = scrape_job()

        count = 0

        for job in jobs:
            inserted = save_job(
                title=job.get("title"),
                company=job.get("company"),
                location=job.get("location"),
                job_url=job.get("job_url"),
                description=job.get("description"),
                experience=job.get("experience"),
                employment_type=job.get("employment_type"),
                skills=job.get("skills"),
                match_score=job.get("match_score"),
                posted_date=job.get("posted_date"),
                inserted_at=job.get("inserted_at"),
                applied_at=job.get("applied_at"),
                source = job.get("source"),
                application_status=job.get(
                    "application_status",
                    "Not Applied"
                )
            )

        if inserted:
            count += 1

        print(f"{count} jobs added")

    '''--------------------------------------------------------'''

    def collect_jobs_db(self):
        jobs=get_unscraped_jobs()
        print(f"Found {len(jobs)} jobs to enrich.")

        for job in jobs:
            try:
                details = scrape_job(self.page, job.job_url)
                update_job(job.id, details)
            except Exception as e:
                print(f"❌ Failed: {job.job_url}")
                print(e)

    '''--------------------------------------------------------'''

    def enrich_jobs(self):

        jobs = get_unscraped_jobs()

        print(f"\nFound {len(jobs)} jobs to enrich.\n")

        updated = 0

        with sync_playwright() as p:

            self.context = p.chromium.launch_persistent_context(
                user_data_dir="./linkedin_profile",
                headless=False,
            )

            self.page = self.context.new_page()

            login(self.page, self.context)

            try:

                for job in jobs:

                    print("=" * 80)
                    print(job.job_url)

                    details = scrape_job(
                        self.page,
                        job.job_url
                    )

                    update_job(
                        job.id,
                        details
                    )

                    updated += 1

            finally:

                self.context.close()

        print(f"\nUpdated {updated} jobs.")


    if __name__ == "__main__":

        enrich_jobs()