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

## 🏗️ System Architecture

```text
                               Scheduler
                                   │
                                   ▼
                           LangGraph Agent
                                   │
        ┌──────────────────┬──────────────────────┬
        ▼                  ▼                      ▼
   Gmail Jobs     LinkedIn Notifications      #Hiring Posts
        │                  │                      │
        └──────────────────┴──────────────────────┘
                                   │
                                   ▼
                    Does a "View Job" link exist?
                           │                 │
                        Yes │                 │ No
                           ▼                 ▼
                 Scrape Full LinkedIn JD   Continue with
                                           post/email data
                           │                 │
                           └─────────┬───────┘
                                     ▼
                        Opportunity Extraction
          (Job URL, Company, Title, Description, Email, Source)
                                     │
                                     ▼
                 Link Normalization & Deduplication
             (Canonical URL + Company + Role matching)
                                     │
                                     ▼
                   Structured Extraction (LLM)
          ──────────────────────────────────────────────
          • Company
          • Job Title
          • Skills
          • Experience
          • Location
          • HR Email (from post and/or JD)
          • Easy Apply Availability
          • External ATS Link
          ──────────────────────────────────────────────
                                     │
                                     ▼
                          Resume Match Scoring
                                     │
                         Score ≥ Threshold?
                           │               │
                          No              Yes
                           │               │
                        Reject             ▼
                                  Resume Tailoring
                                          │
                                          ▼
                                Cover Letter Generation
                                          │
                                          ▼
                               Application Policy Engine
                                          │
             ┌────────────────────────────┼────────────────────────────┐
             ▼                            ▼                            ▼
        Easy Apply                 Send HR Email              External ATS Apply
             │                            │                            │
             └────────────────────────────┴────────────────────────────┘
                                          │
                                          ▼
                           Update Database & Notify User
```

### Workflow Overview

1. **Job Discovery**
   - Collect opportunities from Gmail, LinkedIn Notifications, and LinkedIn `#Hiring` posts.

2. **Job Enrichment**
   - If a `#Hiring` post contains a **View Job** link, scrape the complete LinkedIn job description.
   - Otherwise, continue using the information available in the post or email.

3. **Opportunity Processing**
   - Extract relevant job information.
   - Normalize job links and remove duplicate opportunities.

4. **LLM-Based Analysis**
   - Parse the job description into structured fields.
   - Evaluate resume-job compatibility using an LLM.

5. **Application Preparation**
   - Tailor the resume.
   - Generate a personalized cover letter.

6. **Application Execution**
   - Depending on the available application methods, the agent can:
     - Submit **LinkedIn Easy Apply**
     - Send a personalized application via **HR Email**
     - Apply through an **External ATS**
   - Multiple application methods can be executed for the same opportunity when appropriate.

7. **Tracking**
   - Record all actions in the database and notify the user of the application status.

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

