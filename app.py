import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

app = Flask(__name__)

# Scraper for Dingbatz with updated URL
def scrape_dingbatz():
    url = "https://dingbatzlive.com/show-calendar/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Dingbatz Error: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    events = []

    for event in soup.find_all("div", class_="fusion-event"):
        # Extract event date
        date_tag = event.find("div", class_="fusion-event-date")
        date = date_tag.text.strip() if date_tag else "Unknown Date"

        # Extract event title and link
        title_tag = event.find("h3", class_="fusion-event-title")
        title_link = title_tag.find("a") if title_tag else None
        title = title_link.text.strip() if title_link else "Unknown Event"
        link = title_link["href"] if title_link else "#"

        events.append((date, title, "Dingbatz", link))

    return events

# Scraper for Debonair Music Hall
def scrape_debonair():
    url = "https://www.debonairmusichall.com/shows"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Debonair Error: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    events = []

    for event in soup.find_all("div", class_="event-item"):
        date_tag = event.find("div", class_="event-date")
        date = date_tag.text.strip() if date_tag else "Unknown Date"

        title_tag = event.find("a", class_="event-title")
        title = title_tag.text.strip() if title_tag else "Unknown Event"
        link = title_tag["href"] if title_tag else "#"

        events.append((date, title, "Debonair Music Hall", link))

    return events

@app.route("/")
def home():
    # Combine events from both venues
    all_events = scrape_dingbatz() + scrape_debonair()
    all_events.sort()  # Sort by date (optional)

    return render_template("index.html", events=all_events)

if __name__ == "__main__":
    app.run(debug=True)
