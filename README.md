# Cyber Threat Intelligence Tracker

A full-stack web application for logging, categorizing, and analyzing cyber threats. Built with Python, Flask, and SQLite — directly aligned with MITRE's threat intelligence and adversary emulation workflows.

## Features

- **Dashboard** — Live stats showing total threats, critical count, and high severity count
- **Search & Filter** — Filter threats by keyword, type (Ransomware, APT, Phishing, etc.), or severity level
- **Log New Threats** — Form to record new threat intelligence entries with source attribution
- **Threat Detail View** — Full detail page per threat with direct link to MITRE ATT&CK framework
- **Delete Records** — Remove outdated or resolved threats
- **Pre-seeded Data** — Includes 6 real-world threats (WannaCry, Emotet, SolarWinds, Log4Shell, etc.)

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Flask |
| Database | SQLite (via sqlite3) |
| Templating | Jinja2 |
| Frontend | HTML/CSS (dark GitHub-inspired theme) |

## Project Structure

```
threat_tracker/
├── app.py                  # Flask application, routes, DB logic
├── threats.db              # SQLite database (auto-created on first run)
├── requirements.txt        # Python dependencies
└── templates/
    ├── base.html           # Shared layout (nav, styles)
    ├── index.html          # Dashboard + threat table
    ├── add.html            # Log new threat form
    └── detail.html         # Individual threat detail view
```

## Setup & Run

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/threat-tracker.git
cd threat-tracker

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Open your browser to: **http://127.0.0.1:5000**

The database is auto-created with 6 sample threats on first launch.

## Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Dashboard — view all threats, search, filter |
| `/add` | GET/POST | Log a new threat |
| `/threat/<id>` | GET | View threat detail |
| `/delete/<id>` | POST | Delete a threat |

## Relevance to Cybersecurity Roles

This project demonstrates:
- **Threat Intelligence** — Structured logging and categorization of IOCs and threat actors
- **Adversary Emulation** — Pre-seeded data maps to MITRE ATT&CK techniques (ransomware, APT, supply chain)
- **Detection Engineering** — Severity classification system mirrors real SOC triage workflows
- **Data Analysis** — Filter/search functionality reflects threat hunting query patterns
- **Full-Stack Development** — End-to-end ownership from database schema to UI

## Sample Threats Included

| Threat | Type | Severity | Source |
|--------|------|----------|--------|
| WannaCry | Ransomware | Critical | DHS Alert |
| Emotet | Malware | High | CISA Advisory |
| SolarWinds SUNBURST | APT | Critical | NSA Report |
| Phishing Campaign - IRS | Phishing | Medium | Internal |
| Log4Shell Exploit | Vulnerability Exploit | Critical | MITRE ATT&CK |
| BlackCat Ransomware | Ransomware | High | FBI Flash |
