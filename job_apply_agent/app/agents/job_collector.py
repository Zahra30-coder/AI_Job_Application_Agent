from app.services.scrapers.linkedin_scraper import scrape_jobs
from app.services.job_service import save_job

#del jobs.db
#python -m app.database.init_db
#python -m app.agents.run_collector

def collect_jobs():
    jobs = scrape_jobs()

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