# Job Apply Agent

AI-powered job discovery and application automation tool that collects jobs from LinkedIn, enriches job data, filters relevant opportunities, and tracks applications.

## Features

- Extract jobs from LinkedIn Job Alerts using Gmail API
- Scrape job details with Playwright
- Store and manage jobs in SQLite
- Enrich jobs with title, company, location, skills, and description
- Filter jobs by experience, location, and remote preference
- Detect Easy Apply opportunities
- Track application status

## Tech Stack

- Python
- Playwright
- Gmail API
- SQLite
- SQLAlchemy
- BeautifulSoup

## Installation

```bash
git clone <repository-url>
cd job_apply_agent

python -m venv chatbot-env
chatbot-env\Scripts\activate

pip install -r requirements.txt

playwright install
```

## Run

```bash
python -m app.database.init_db
python -m app.agents.run_collector
```

## Workflow

```text
LinkedIn Alerts
      ↓
 Gmail API
      ↓
 Link Extraction
      ↓
 Playwright Scraper
      ↓
 SQLite Database
      ↓
 Job Filtering & Tracking
```

## Key Challenge

LinkedIn emails contain tracking links and LinkedIn pages load dynamically. To improve reliability, I built a URL normalization pipeline and implemented Playwright-based retry logic, explicit waits, and persistent login sessions.

## Impact

Automates a highly manual job search workflow, reducing the time spent discovering, organizing, and tracking job opportunities.