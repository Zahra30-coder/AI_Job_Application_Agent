import sqlite3
#python check-db.copy()
#python -c "from sqlalchemy import inspect; from app.database.db import engine; print(inspect(engine).get_table_names())"
#['jobs']

#Open DB Browser for SQLite
#Click Open Database
#Select:
#D:\CHATBOT\JOB_APPLY_AGENT\jobs.db
#Go to Browse Data
#Select the jobs table

conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

# Show all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables:")
print(tables)

# Show all jobs
cursor.execute("""
SELECT
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
    application_status,
    source,
    inserted_at,
    applied_at
FROM jobs
""")

jobs = cursor.fetchall()

print(f"\nFound {len(jobs)} jobs:\n")

for job in jobs:
    print(job)

conn.close()