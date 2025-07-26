# Multi‑Site Job Scraper

This project provides a generic Python scraper that extracts data from three websites with a common structure (for example, job vacancies or classified listings).  The script fetches HTML pages, parses relevant fields such as title, company and location, and outputs the combined results into a CSV file.  Optionally, it can export the data to Google Sheets using the `gspread` library.

## Purpose

Automate data collection from multiple similar sources.  If you frequently gather listings from different sites with the same layout (e.g. regional job boards built on the same CMS), writing one scraper per site is wasteful.  This project demonstrates a single parser that can be configured for multiple domains.

## Technology Stack

* **Python 3**
* **requests** – HTTP client for downloading pages
* **BeautifulSoup 4** – HTML parser for extracting information
* **csv** / **pandas** – for exporting data
* **gspread** (optional) – integration with Google Sheets

## Installation

1. Clone the repository and install dependencies:

   ```bash
   git clone https://github.com/your‑username/multi-site-scraper.git
   cd multi-site-scraper
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. (Optional) To export results to Google Sheets you need to create a [service account](https://developers.google.com/identity/protocols/oauth2/service-account) and share the destination spreadsheet with the service account email.  Save the JSON credentials file and set `GOOGLE_APPLICATION_CREDENTIALS` to its path.

## Usage

Edit the `sites` list in `main.py` to contain the URLs of the pages you wish to scrape.  Ensure that the CSS selectors in `parse_jobs()` match the page structure (title, company, location).  Then run:

```bash
python main.py
```

After execution the script writes `jobs.csv` with all collected rows.  If the `--to-sheets` flag is provided and `GOOGLE_APPLICATION_CREDENTIALS` is set, the data is also appended to the specified Google Sheets document.

## Example

A sample output file `data/example_jobs.csv` is included to illustrate the format:

| source                             | title               | company         | location    |
|------------------------------------|---------------------|-----------------|-------------|
| https://example-site1.com/jobs     | Python Developer    | Acme Corp       | Stockholm   |
| https://example-site2.com/careers  | Data Analyst        | DataCo          | Göteborg    |
| https://example-site3.com/vacancies| Full‑Stack Engineer | Future Solutions| Malmö       |

## Demonstration idea (≤2 min)

1. Record a Loom video showing how you adjust the `sites` list and CSS selectors in `main.py` for three demo pages.
2. Run the script and display the console output while it fetches data.
3. Open the generated CSV and Google Sheet (if enabled) to show the aggregated results.
4. Highlight that adding a new site requires only a URL and that the parser logic is shared.

## Possible extensions for a client

* **Pagination support** – iterate through multiple pages on each site.
* **Playwright integration** – scrape dynamic pages that require JavaScript rendering.
* **Flexible fields** – allow the user to specify which fields to extract via a configuration file.
* **Database storage** – write results to a relational database (SQLite, PostgreSQL) instead of CSV.
* **Scheduling** – run the scraper periodically (e.g. daily) and append new postings to Google Sheets.

## Google Sheets API note

The `gspread` library is a thin wrapper around the Google Sheets API v4.  Under the hood gspread uses the official API and each method call typically results in one HTTP request【35006277061964†L184-L186】.  When exporting large amounts of data it's more efficient to batch updates rather than updating cells individually.
