from app.database.db import SessionLocal
from app.database.models import Job
from datetime import datetime
from urllib.parse import urlparse


def is_job_detail_url(job_url: str) -> bool:
    path = urlparse(job_url or "").path.lower()
    return "/jobs/view/" in path or "/comm/jobs/view/" in path

def save_job(
    title,
    company,
    location,
    job_url,
    description,
    experience=None,
    employment_type=None,
    skills=None,
    match_score=0,
    posted_date=None,
    inserted_at=None,
    applied_at=None,
    source=None,
):
    db = SessionLocal()

    try:
        existing = (
            db.query(Job)
            .filter(Job.job_url == job_url)
            .first()
        )

        if existing:
            return False

        job = Job(
            title=title,
            company=company,
            location=location,
            job_url=job_url,
            description=description,
            experience=experience,
            employment_type=employment_type,
            skills=skills,
            match_score=match_score or 0,
            posted_date=posted_date,
            inserted_at=inserted_at or datetime.now(),
            applied_at=applied_at,
            source=source
        )

        db.add(job)
        db.commit()

        return True

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

'''---------------------------------------------------'''

def save_job_url(job_url: str, source: str | None = None):
    """
    Save a job URL if it doesn't already exist.
    """

    if not is_job_detail_url(job_url):
        print(f"Skipped non-job URL: {job_url}")
        return False

    db = SessionLocal()

    try:
        # Check if URL already exists
        existing_job = (
            db.query(Job)
            .filter(Job.job_url == job_url)
            .first()
        )

        if existing_job:
            if source and not existing_job.source:
                existing_job.source = source
                db.commit()

            print(f"Already exists: {job_url}")
            return False

        job = Job(
            job_url=job_url,
            source=source
        )

        db.add(job)
        db.commit()
        db.refresh(job)

        print(f"Saved: {job_url}")
        return True

    except Exception as e:
        db.rollback()
        print(f"Error saving job URL: {e}")
        return False

    finally:
        db.close()

'''---------------------------------------------------'''

def get_unscraped_jobs():
    db = SessionLocal()

    try:
        jobs = (
            db.query(Job)
            .filter(Job.title == None)
            .all()
        )
        return [job for job in jobs if is_job_detail_url(job.job_url)]

    finally:
        db.close()
        
'''---------------------------------------------------'''

def update_job(job_id: int, details: dict):
    """
    Update an existing job with scraped details.
    """

    db = SessionLocal()

    try:

        job = db.query(Job).filter(Job.id == job_id).first()

        if not job:
            return False

        job.title = details.get("title")
        job.company = details.get("company")
        job.location = details.get("location")
        job.description = details.get("description")
        job.experience = details.get("experience")
        job.employment_type = details.get("employment_type")
        job.skills = details.get("skills")
        job.posted_date = details.get("posted_date")
        job.active = details.get("active", job.active)
        job.remote = details.get("remote", job.remote)
        job.easy_apply = details.get("easy apply", job.easy_apply)

        db.commit()

        return True

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
