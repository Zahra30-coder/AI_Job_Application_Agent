from app.database.db import SessionLocal
from app.database.models import Job

db = SessionLocal()

job = Job(
    title="AI Engineer",
    company="OpenAI",
    location="Remote",
    job_url="https://example.com/job1",
    description="Test Job",
    experience=3,
    employment_type="Contractual",
    skills="RAG",
    match_score=0,
    posted_date="25/06/2026",
    application_status="demo insert",
    source="gmail"
)

db.add(job)
db.commit()

print("Job inserted successfully")