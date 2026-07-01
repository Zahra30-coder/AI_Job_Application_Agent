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
