from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv

# Initialize Chrome options
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")

# Function to scroll down the page until all content is loaded
def scroll_down_page(driver, scroll_pause_time=2):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Initialize Chrome WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Open YouTube watch history page
driver.get("https://www.youtube.com/feed/history")

# Scroll down the YouTube history page multiple times to load more content
scroll_iterations = 300 # Increase the number of times to scroll
for _ in range(scroll_iterations):
    scroll_down_page(driver, scroll_pause_time=2)  # Increase the pause time between scrolls

# Get the page source after scrolling
page_source = driver.page_source

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Now you can use BeautifulSoup to find and extract the desired data
# For example, search for video titles, timestamps, etc.

video_elements = soup.find_all('ytd-video-renderer')

videos_data = []

for video in video_elements:
    title_element = video.find('a', {'id': 'video-title'})
    title = title_element.text.strip() if title_element else "Title not found"
    url = "https://www.youtube.com" + title_element['href'] if title_element else None

    channel_name_element = video.find('yt-formatted-string', {'class': 'ytd-channel-name'})
    channel_name = channel_name_element.text.strip() if channel_name_element else "Channel name not found"

    description_element = video.find('yt-formatted-string', {'id': 'description-text'})
    description = description_element.text.strip() if description_element else "Description not found"

    thumbnail_tag = video.find('img', {'id': 'img'})
    thumbnail = thumbnail_tag['src'] if thumbnail_tag and 'src' in thumbnail_tag.attrs else None

    videos_data.append({
        'title': title,
        'url': url,
        'channel_name': channel_name,
        'description': description,
        'thumbnail': thumbnail
    })


# Define the filename for the CSV file
csv_filename = "youtube_history.csv"

# Write the data to a CSV file
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'url', 'channel_name', 'description', 'thumbnail']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write header
    writer.writeheader()

    # Write video data
    for video in videos_data:
        writer.writerow(video)

print(f"Scraped data saved to {csv_filename}")

# Close the browser when done
driver.quit()
