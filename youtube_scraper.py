from bs4 import BeautifulSoup
import csv


def main():
    html_file_path = "history.html"
    # Read the HTML file
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # extract information
    videos_data = []
    video_elements = soup.find_all(
        "div", class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"
    )

    for video in video_elements:
        # Find the first <a> tag for the title and URL
        title_element = video.find("a")
        title = title_element.text.strip() if title_element else "Title not found"
        url = title_element["href"] if title_element else "URL not found"

        # Initialize default values for channel name and date time
        channel_name = "Unknown Channel"
        channel_url = "Unknown URL"
        date_time = "Unknown Date/Time"

        # additional data
        video_id = video_thumbnail = video_date_upload = video_views = video_likes = (
            video_dislikes
        ) = video_comment_count = video_description = video_tags = None

        # Find the second <a> tag for the channel name
        if title_element:
            channel_element = title_element.find_next("a")
            if channel_element:
                channel_name = channel_element.text.strip()
                channel_url = channel_element["href"]

                # Find the date and time, which is the text after the channel link
                date_time_element = channel_element.find_next_sibling(string=True)
                if date_time_element:
                    date_time = date_time_element.strip()
                    cleaned_date_time = clean_date_time(date_time)

        videos_data.append(
            {
                "title": title,
                "url": url,
                "channel_name": channel_name,
                "channel_url": channel_url,
                "date_time": cleaned_date_time,
                "video_id": video_id,
                "video_thumbnail": video_thumbnail,
                "video_date_upload": video_date_upload,
                "video_views": video_views,
                "video_likes": video_likes,
                "video_dislikes": video_dislikes,
                "video_comment_count": video_comment_count,
                "video_description": video_description,
                "video_tags": video_tags,
            }
        )

    csv_filename = "youtube_history.csv"

    # Write the data to a CSV file
    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "title",
            "url",
            "channel_name",
            "channel_url",
            "date_time",
            "video_id",
            "video_thumbnail",
            "video_date_upload",
            "video_views",
            "video_likes",
            "video_dislikes",
            "video_comment_count",
            "video_description",
            "video_tags",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write video data
        for video in videos_data:
            writer.writerow(video)

    print(f"Scraped data saved to {csv_filename}")


def clean_date_time(date_time):
    # Replace any non-ASCII characters with an empty string
    cleaned_date_time = "".join(char for char in date_time if ord(char) < 128)
    # Add any additional cleaning or formatting logic here if needed
    if "PM" in cleaned_date_time:
        return cleaned_date_time.replace("PM", " PM")
    return cleaned_date_time.replace("AM", " AM")


if __name__ == "__main__":
    main()
