import csv
import isodate
import logging
import re
import pandas as pd
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from datetime import datetime
from dateutil import parser
from dateutil.parser import ParserError

API_KEY = "<API KEY HERE>"


def main():
    html_file_path = "watch-history.html"
    # The output file as csv
    youtube_data = "youtube_data.csv"
    # Extract metadata for each video
    extract_data_from_api(youtube_data)


def extract_data_from_html(html_file_path: str, csv_output_path: str) -> None:
    """
    This function takes an HTML file and extracts preliminary data from it: the title of the video and its URL,
    watch date, channel uploader, and its URL. Then it will return a CSV file storing the extracted data.

    :param html_file_path: The path to the HTML file to be parsed.
    :param csv_output_path: The path where the output CSV file should be saved.
    :return: None
    """

    print("Extracting data from HTML file....")
    # Read the HTML file
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Store extracted information in a list of dictionaries
    videos_data = []

    # Find html elements containing the video information
    video_elements = soup.find_all(
        "div", class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"
    )

    # Extract each video data founded for each HTML elements
    for video in video_elements:
        # Find the first <a> tag for the title and URL
        title_element = video.find("a")
        title = title_element.text.strip() if title_element else None

        """
        Handle case where there is no video title extracted from the HTML element due to:
        (1) the video being removed/deleted from YouTube, or (2) the element being a YouTube Ad.
        In such cases, we skip to the next HTML element and do not include videos with missing information.
        """
        if title is None or (
            re.fullmatch(
                r"https?://(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)", title
            )
        ) or title.endswith(".mp4"):
            continue  # Skip to the next video element

        url = title_element["href"] if title_element else None

        # Initialize default values for channel name and date time
        channel_name = channel_url = date_time = None

        # additional data
        video_date_upload = video_views = video_likes = (
            video_comment_count
        ) = video_description = video_tags = video_duration = video_category = None

        try:
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
                        # Parse the string into a datetime object
                        dt = parser.parse(date_time, ignoretz=True)
                        # Format the datetime object without timezone information
                        date_time = dt.strftime("%b %d, %Y, %I:%M:%S %p")
        except ParserError:
            continue

        # only the title, url, channel_name, channel_url, and date_time are filled for now
        videos_data.append(
            {
                "title": title,
                "url": url,
                "video_duration": video_duration,
                "channel_name": channel_name,
                "channel_url": channel_url,
                "date_time": date_time,
                "video_date_upload": video_date_upload,
                "video_category": video_category,
                "video_views": video_views,
                "video_likes": video_likes,
                "video_comment_count": video_comment_count,
                "video_description": video_description,
                "video_tags": video_tags,
            }
        )

    # Write the data to a CSV file
    with open(csv_output_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [data for data in videos_data[0].keys()]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Write header
        writer.writeheader()
        # Write video data
        for video in videos_data:
            writer.writerow(video)

    print(f"Scraped data saved to {csv_output_path}\n")


def extract_data_from_api(youtube_data: str) -> None:
    """
    This function takes a pre-existing CSV file that already contains some video information extracted from an HTML file.
    It iterates through each video in the CSV, requests additional information from the YouTube API,
    and then saves this information back to the CSV file.

    :param youtube_data: csv file where preliminary data is stored.
    :return: None
    """

    # Set up YouTube API client
    # Go to https://developers.google.com/youtube/v3/getting-started for more information
    youtube = build(
        "youtube", "v3", developerKey=API_KEY
    )

    print("The extraction process time varies on how big is the YouTube Watch History Data.\n")
    print("Extracting Data.......")

    logging.basicConfig(level=logging.WARNING)

    # Read the csv file to iterate on every YouTube Video
    with open(youtube_data, "r", newline="", encoding="latin-1") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # Access values by column names (keys in the dictionary)
            video_url = row['url']

            if video_url and "https://www.youtube.com/watch?v=" in video_url:
                print("Processing video URL: %s", video_url)
            else:
                continue  # Skip this row and move to the next one

            video_id = video_url.replace("https://www.youtube.com/watch?v=", "")

            try:
                # Make API request to retrieve detailed video information
                video_response = (
                    youtube.videos()
                    .list(part="snippet,contentDetails,statistics", id=video_id)
                    .execute()
                )

                # Extract additional details from video response
                if "items" in video_response and video_response["items"]:
                    video_info = video_response["items"][0]["snippet"]
                    video_content_details = video_response["items"][0][
                        "contentDetails"
                    ]
                    video_stats = video_response["items"][0].get("statistics", {})

                    # read the csv file
                    df = pd.read_csv(youtube_data)
                    cast_dtype = ["video_duration", "video_description", "video_tags", "video_category", "video_date_upload"]
                    # handle dtype error when reading the csv (pandas read the column dtype as float64)
                    df[cast_dtype] = df[cast_dtype].astype('object')

                    # locate each video url and update the returned data from API
                    df.loc[
                        df["url"] == video_url,
                        [
                            "video_date_upload",
                            "video_category",
                            "video_views",
                            "video_likes",
                            "video_comment_count",
                            "video_description",
                            "video_tags",
                            "video_duration",
                        ],
                    ] = (
                        str(
                            process_datetime(video_info.get("publishedAt", ""))
                        ),
                        str(
                            get_category_name(video_info.get("categoryId", ""))
                        ),
                        int(
                            video_stats.get("viewCount", 0)
                        ),
                        int(
                            video_stats.get("likeCount", 0)
                        ),
                        int(
                            video_stats.get("commentCount", 0)
                        ),
                        str(
                            video_info.get("description", "")
                        ),
                        ",".join(
                            video_info.get("tags", "")
                        ),
                        str(
                            clean_duration_time(
                                video_content_details.get("duration", "")
                            )
                        ),

                    )

                    df.to_csv(youtube_data, index=False, float_format='%.0f')

            except Exception as e:
                logging.warning(
                    "An error occurred while processing video ID %s: %s",
                    video_id,
                    e,
                )

    print("Successfully extracted data from YouTube API. Check the updated CSV file.")


def clean_duration_time(duration: str) -> str:
    """
    This function cleans and formats an ISO 8601 duration string into a readable time format.

    :param duration: A string representing the ISO 8601 duration (e.g., 'PT1H2M3S').
    :return: A string formatted as 'HH:MM:SS'.

    Example:
    >>> clean_duration_time('PT1H2M3S')
    '01:02:03'
    >>> clean_duration_time('PT15M25S')
    '00:15:25'
    """

    # Parse the ISO 8601 duration
    duration = isodate.parse_duration(duration)
    total_seconds = int(duration.total_seconds())

    # Calculate hours, minutes, and seconds
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # Return formatted string
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def process_datetime(datetime_str: str) -> str:
    """
    Cleans and formats an ISO 8601 datetime string into a readable time format.

    :param datetime_str: A string representing the ISO 8601 duration (e.g., '2017-11-13T06:06:22Z').
    :return: A string formatted as 'YYYY-MM-DD HH:MM:SS'.

    Example:
    >>> process_datetime('2017-11-13T06:06:22Z')
    '2017-11-13 06:06:22'
    >>> process_datetime('2020-04-10T05:36:02Z')
    '2020-04-10 05:36:02'
    """
    # Parse the datetime string into a datetime object
    dt = datetime.fromisoformat(datetime_str)

    # Format the datetime object as per requirement
    formatted_datetime = dt.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_datetime


def get_category_name(category_id: str) -> str:
    """
    This function receives a category ID and returns the name of the category.

    :param category_id: Contains the category ID of the category (e.g., '10').
    :return: A string representing the name of the category (e.g., 'Music').

    Example:
    >>> get_category_name('10')
    'Music'
    >>> get_category_name('20')
    'Gaming'
    """
    category_names = {
        "2": "Autos & Vehicles",
        "1": "Film & Animation",
        "10": "Music",
        "15": "Pets & Animals",
        "17": "Sports",
        "18": "Short Movies",
        "19": "Travel & Events",
        "20": "Gaming",
        "21": "Videoblogging",
        "22": "People & Blogs",
        "23": "Comedy",
        "24": "Entertainment",
        "25": "News & Politics",
        "26": "Howto & Style",
        "27": "Education",
        "28": "Science & Technology",
        "29": "Nonprofits & Activism",
        "30": "Movies",
        "31": "Anime/Animation",
        "32": "Action/Adventure",
        "33": "Classics",
        "34": "Comedy",
        "35": "Documentary",
        "36": "Drama",
        "37": "Family",
        "38": "Foreign",
        "39": "Horror",
        "40": "Sci-Fi/Fantasy",
        "41": "Thriller",
        "42": "Shorts",
        "43": "Shows",
        "44": "Trailers"
    }

    return category_names.get(category_id)


if __name__ == "__main__":
    main()