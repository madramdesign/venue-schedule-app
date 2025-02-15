from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

def setup_driver():
    """Sets up the Selenium WebDriver with headless Chrome."""
    options = Options()
    options.add_argument("--headless")  # Run in background
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_dingbatz():
    """Scrapes events from Dingbatz website."""
    url = "https://dingbatzlive.com/show-calendar/"
    driver = setup_driver()

    try:
        driver.get(url)
        time.sleep(5)  # Wait for page load

        events = []
        event_elements = driver.find_elements(By.CLASS_NAME, "fusion-event")

        for event in event_elements:
            date_elem = event.find_element(By.CLASS_NAME, "fusion-event-date")
            date = date_elem.text.strip() if date_elem else "Unknown Date"

            title_elem = event.find_element(By.CLASS_NAME, "fusion-event-title")
            title_link = title_elem.find_element(By.TAG_NAME, "a") if title_elem else None
            title = title_link.text.strip() if title_link else "Unknown Event"
            link = title_link.get_attribute("href") if title_link else "#"

            events.append((date, title, "Dingbatz", link))

    except Exception as e:
        print(f"Error fetching events from Dingbatz: {e}")
        events = []
    
    finally:
        driver.quit()
    
    return events

def scrape_debonair():
    """Scrapes events from Debonair Music Hall website."""
    url = "https://www.debonairmusichall.com/"
    driver = setup_driver()

    try:
        driver.get(url)
        time.sleep(5)  # Wait for page load

        events = []
        event_elements = driver.find_elements(By.CLASS_NAME, "event-item")

        for event in event_elements:
            date_elem = event.find_element(By.CLASS_NAME, "event-date")
            date = date_elem.text.strip() if date_elem else "Unknown Date"

            title_elem = event.find_element(By.CLASS_NAME, "event-title")
            title_link = title_elem.find_element(By.TAG_NAME, "a") if title_elem else None
            title = title_link.text.strip() if title_link else "Unknown Event"
            link = title_link.get_attribute("href") if title_link else "#"

            events.append((date, title, "Debonair Music Hall", link))

    except Exception as e:
        print(f"Error fetching events from Debonair Music Hall: {e}")
        events = []
    
    finally:
        driver.quit()
    
    return events

@app.route('/')
def home():
    """Combines and displays upcoming events from multiple venues."""
    dingbatz_events = scrape_dingbatz()
    debonair_events = scrape_debonair()
    all_events = dingbatz_events + debonair_events

    # Sort events by date
    all_events.sort(key=lambda x: x[0])

    return render_template("index.html", events=all_events)

if __name__ == "__main__":
    app.run(debug=True)
