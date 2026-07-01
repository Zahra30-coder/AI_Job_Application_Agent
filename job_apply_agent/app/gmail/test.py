from app.gmail.collector import collect_jobs

jobs = collect_jobs()

print(f"Found {len(jobs)} jobs")

for job in jobs:
    print(job)