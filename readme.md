# Job Apply Agent

AI-powered job discovery and application automation tool that collects jobs from LinkedIn, enriches job data, filters relevant opportunities, and tracks applications.

## Impact

Automates a highly manual job search workflow, reducing the time spent discovering, organizing, and tracking job opportunities.

## Features

- Extract jobs from LinkedIn Job Alerts using Gmail API and LinkedIn-in app notifications 
- Scrape job details with Playwright and insert jobs in SQLite
- Apply on the candidate's behalf

  ## Workflow

```text
 Gmail API, LinkedIn Notification Alerts
      ↓
 Link Extraction
      ↓
 Playwright Scraper
      ↓
 SQLite Database
      ↓
 Job Filtering & Tracking
```

## Tech Stack

- Python
- Playwright
- Gmail API
- SQLite

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
#Creating DB

python -m app.gmail.collector
#Running Gmail Scraper

python -m app.agents.run_linkedin_notifications
#Running Linkedin Notification Scraper
```

## Key Challenge

LinkedIn emails contain tracking links and LinkedIn pages load dynamically. To improve reliability, I built a URL normalization pipeline and implemented Playwright-based retry logic, explicit waits, and persistent login sessions.

