import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import time
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_indeed(query, location, max_results=15):
    jobs = []
    url = f"https://www.indeed.com/jobs?q={quote(query)}&l={quote(location)}"
    res = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")
    cards = soup.select(".job_seen_beacon")
    for card in cards[:max_results]:
        title_tag = card.select_one("h2 a")
        company_tag = card.select_one(".companyName")
        location_tag = card.select_one(".companyLocation")
        snippet_tag = card.select_one(".job-snippet")
        description = snippet_tag.text.strip() if snippet_tag else ""
        if not title_tag:
            continue
        link = "https://www.indeed.com" + title_tag.get("href", "")
        jobs.append({
            "title": title_tag.text.strip(),
            "company": company_tag.text.strip() if company_tag else "",
            "location": location_tag.text.strip() if location_tag else "",
            "apply_link": link,
            "snippet_tag": snippet_tag,
            "description": description,
            "source": "indeed"
        })

    return jobs

def scrape_google_jobs(query):
    jobs = []
    url = f"https://www.google.com/search?q={quote(query + ' jobs')}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    for link in soup.select("a"):
        href = link.get("href", "")
        if "url?q=" in href:
            actual_link = href.split("url?q=")[1].split("&")[0]
            if "job" in actual_link or "career" in actual_link:
                jobs.append({
                    "title": query,
                    "company": "",
                    "location": "",
                    "apply_link": actual_link,
                    "source": "google"
                })
        if len(jobs) >= 10:
            break
    return jobs

def scrapeJobs(ai_result,max_jobs=50):
    queries = ai_result.get("queries", [])
    location = ai_result.get("filters", {}).get("location", "India")
    all_jobs = []
    seen_links = set()
    for query in queries:
        indeed_jobs = scrape_indeed(query, location)
        google_jobs = scrape_google_jobs(query)
        combined = indeed_jobs + google_jobs
        for job in combined:
            if job["apply_link"] in seen_links:
                continue
            seen_links.add(job["apply_link"])
            all_jobs.append(job)
            if len(all_jobs) >= max_jobs:
                return all_jobs
        time.sleep(1)
    return all_jobs



#TODO: scraping+web search code
