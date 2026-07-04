from app.database.db import SessionLocal
from app.database.models import Job
from datetime import datetime

def save_job(
    title,
    company,
    location,
    job_url,
    description,
    experience,
    employment_type,
    skills,
    match_score,
    posted_date,
    inserted_at,
    applied_at,
    application_status,
    source,
):
    db = SessionLocal()

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
        match_score=0,
        posted_date=posted_date,
        inserted_at = datetime.now(),
        applied_at = None,
        application_status="NEW",
        source=source
    )

    db.add(job)
    db.commit()

    return True

'''---------------------------------------------------'''

def save_job_url(job_url: str):
    """
    Save a job URL if it doesn't already exist.
    """

    db = SessionLocal()

    try:
        # Check if URL already exists
        existing_job = (
            db.query(Job)
            .filter(Job.job_url == job_url)
            .first()
        )

        if existing_job:
            print(f"Already exists: {job_url}")
            return False

        job = Job(
            job_url=job_url
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
        return (
            db.query(Job)
            .filter(Job.title == None)
            .all()
        )

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

        # Optional fields if your model has them
        if hasattr(job, "easy_apply"):
            job.easy_apply = details.get("easy_apply")

        if hasattr(job, "remote"):
            job.remote = details.get("remote")

        if hasattr(job, "job_status"):
            job.job_status = details.get("job_status")

        db.commit()

        return True

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()