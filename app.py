from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

# Dictionary of venues and their event page URLs
venues = {
    "Dingbatz": "https://dingbatzlive.com/show-calendar/",
    "Debonair Music Hall": "https://debonairmusichall.com/events"
}

def fetch_events(venue_name, url):
    """Fetch and parse events from a given venue URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')

        events = []

        # Identify venue and extract event details
        if "dingbatz" in url:
            event_entries = soup.find_all('div', class_='event-entry')  # Modify based on actual HTML structure
            for event in event_entries:
                date_str = event.find('div', class_='event-date').get_text(strip=True)
                title = event.find('div', class_='event-title').get_text(strip=True)
                event_date = datetime.strptime(date_str, '%B %d, %Y').date()
                events.append((event_date, title, venue_name))

        elif "debonairmusichall" in url:
            event_entries = soup.find_all('div', class_='event-entry')  # Modify based on actual HTML structure
            for event in event_entries:
                date_str = event.find('div', class_='event-date').get_text(strip=True)
                title = event.find('div', class_='event-title').get_text(strip=True)
                event_date = datetime.strptime(date_str, '%B %d, %Y').date()
                events.append((event_date, title, venue_name))

        return events

    except Exception as e:
        print(f"Error fetching events for {venue_name}: {e}")
        return []

@app.route('/')
def home():
    all_events = []
    for venue, url in venues.items():
        all_events.extend(fetch_events(venue, url))
    
    # Sort events by date
    all_events.sort()

    return render_template('index.html', events=all_events)

if __name__ == '__main__':
    app.run(debug=True)
