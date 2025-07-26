"""
Multi-Site Scraper

Scrapes multiple websites with similar structures and saves the results to a CSV file.
Optionally appends to a Google Sheet.
"""

import argparse
import csv
import os
from dataclasses import dataclass
from typing import Iterable, List

import requests
from bs4 import BeautifulSoup

try:
    import gspread
    from google.oauth2.service_account import Credentials
except ImportError:
    gspread = None
    Credentials = None

@dataclass
class Job:
    source: str
    title: str
    company: str
    location: str

def parse_jobs(url: str) -> List[Job]:
    """Parse job postings from a single page."""
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    jobs: List[Job] = []
    for job_el in soup.select("div.job"):
        title_el = job_el.select_one("h2.title")
        company_el = job_el.select_one("span.company")
        location_el = job_el.select_one("span.location")
        if not (title_el and company_el and location_el):
            continue
        jobs.append(Job(
            source=url,
            title=title_el.get_text(strip=True),
            company=company_el.get_text(strip=True),
            location=location_el.get_text(strip=True),
        ))
    return jobs

def write_csv(jobs: Iterable[Job], csv_path: str) -> None:
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source","title","company","location"])
        writer.writeheader()
        for job in jobs:
            writer.writerow(job.__dict__)

def append_to_sheet(jobs: Iterable[Job], sheet_id: str) -> None:
    if gspread is None or Credentials is None:
        raise RuntimeError("gspread is not installed. Install gspread and google-auth.")
    creds = Credentials.from_service_account_file(os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
                                                 scopes=["https://www.googleapis.com/auth/spreadsheets"])
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).sheet1
    rows = [[job.source, job.title, job.company, job.location] for job in jobs]
    sheet.append_rows(rows)

def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape multiple websites with a shared structure")
    parser.add_argument("--to-sheets", metavar="SHEET_ID", help="append results to the given Google Sheet")
    args = parser.parse_args()

    sites = [
        "https://example-site1.com/jobs",
        "https://example-site2.com/jobs",
        "https://example-site3.com/jobs",
    ]
    all_jobs: List[Job] = []
    for site in sites:
        try:
            jobs = parse_jobs(site)
            all_jobs.extend(jobs)
            print(f"Fetched {len(jobs)} jobs from {site}")
        except Exception as exc:
            print(f"Failed to scrape {site}: {exc}")

    if not all_jobs:
        print("No jobs found.")
        return

    csv_path = "jobs.csv"
    write_csv(all_jobs, csv_path)
    print(f"Wrote {len(all_jobs)} jobs to {csv_path}")

    if args.to_sheets:
        append_to_sheet(all_jobs, args.to_sheets)
        print(f"Appended {len(all_jobs)} jobs to Google Sheet {args.to_sheets}")

if __name__ == "__main__":
    main()
