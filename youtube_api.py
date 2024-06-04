import csv
import logging

import pandas as pd
from googleapiclient.discovery import build


def extract_data():
    # Set up logging
    logging.basicConfig(level=logging.DEBUG)

    # Set up YouTube Data API client
    youtube = build(
        "youtube", "v3", developerKey="API KEY"
    )

    with open("../youtube_history.csv", "r", newline="", encoding="latin-1") as csvfile:
        # Create a DictReader object
        reader = csv.DictReader(csvfile)


        # Iterate over each row in the CSV file
        for row in reader:
            # Access values by column names (keys in the row dictionary)
            video_url = row["url"]  # Assuming the column name for video URL is "url"
            if video_url is not None:
                print("Video URL:", video_url)
                logging.debug("Processing video URL: %s", video_url)
            else:
                logging.warning("Encountered None value for video URL.")

            # Extract video ID from the video URL
            video_id = extract_video_id(video_url)

            if video_id:
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
                        video_content_details = video_response["items"][0]["contentDetails"]
                        video_stats = video_response["items"][0].get("statistics", {})

                        csv_filename = "../youtube_history.csv"
                        # read the csv file
                        df = pd.read_csv(csv_filename)
                        # locate each video url and update the returned data from API such as views and likes
                        df.loc[
                            df["url"] == video_url,
                            [
                                "video_id",
                                "video_thumbnail",
                                "video_date_upload",
                                "video_views",
                                "video_likes",
                                "video_dislikes",
                                "video_comment_count",
                                "video_description",
                                "video_tags",
                                "video_duration",
                            ],
                        ] = (
                            str(video_id),  # Assuming video_id is a string
                            str(
                                video_info.get("thumbnails", {})
                                .get("default", {})
                                .get("url", "")
                            ),
                            # Assuming video_thumbnail is a string
                            str(
                                video_info.get("publishedAt", "")
                            ),  # Assuming video_date_upload is a string
                            int(
                                video_stats.get("viewCount", 0)
                            ),  # Assuming video_views is an integer
                            int(
                                video_stats.get("likeCount", 0)
                            ),  # Assuming video_likes is an integer
                            int(
                                video_stats.get("dislikeCount", 0)
                            ),  # Assuming video_dislikes is an integer
                            int(
                                video_stats.get("commentCount", 0)
                            ),  # Assuming video_comment_count is an integer
                            str(
                                video_info.get("description", "")
                            ),  # Assuming video_description is a string
                            ",".join(
                                video_info.get("tags", "")
                            ),  # Assuming video_tags is a string
                            str(clean_time(video_content_details.get("duration", ""))),  # Assuming video_duration is a string
                        )

                        df.to_csv(csv_filename, index=False)

                    else:
                        logging.warning(
                            "No video items found in the response for video ID: %s",
                            video_id,
                        )
                except Exception as e:
                    logging.error(
                        "An error occurred while processing video ID %s: %s",
                        video_id,
                        e,
                    )
            else:
                logging.warning("Failed to extract video ID from URL: %s", video_url)


def extract_video_id(video_url):
    if video_url and "https://www.youtube.com/watch?v=" in video_url:
        return video_url.replace("https://www.youtube.com/watch?v=", "")
    else:
        logging.warning("Invalid or missing video URL: %s", video_url)
        return None


def clean_time(duration):
    duration = pd.Timedelta(duration)
    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60
    seconds = duration.seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"



extract_data()
