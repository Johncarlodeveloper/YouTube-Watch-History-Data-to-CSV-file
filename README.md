
# YouTube Watch History Data to CSV

This project aims to extract data from an HTML file provided by Google Takeout that contains the user's YouTube Watch History, including all of the videos watched with their titles and URLs, the uploader's channel and its URL, and the time they were viewed on YouTube. It will all be stored in a CSV file with additional information for each video, such as its duration, like count, comment count, and description, with the help of the YouTube API. The implementation of general descriptive approaches to the data will provide a comprehensive findings of YouTube usage habits.

![Alt Text](https://github.com/Johncarlodeveloper/youtube_watch_analytics/blob/main/Output%20CSV%20file%20(1).gif)


A Python script named `youtube.py` was utilized to extract data from an HTML file of YouTube History. This HTML file was obtained through Google Takeout, which provides a detailed export of a user's YouTube activity. Using the BeautifulSoup library, the script parsed the HTML file to extract essential information for each video, including the video title, URL, the time it was played, the channel that posted it, and the channel's URL. This information was then saved into a CSV file named `youtube_data.csv`.

![Alt Text](https://github.com/Johncarlodeveloper/youtube_watch_analytics/blob/main/Output%20CSV%20file%20(2).gif)

However, the HTML file from Google Takeout did not provide all the details required for a comprehensive analysis. To enrich the dataset with additional information, fill in the gaps by fetching more data through the YouTube Data API. For each video entry in `youtube_data.csv`, the script extracted the video ID from the URL. With the video ID in hand, the script made API requests to gather further details such as the video's duration, the number of likes it had received, and the total number of comments. This additional data provided a more comprehensive view of each video.

### Extraction Process

1. **Google Takeout**:
    - The initial dataset was downloaded from Google Takeout, which provided an HMTL file containing basic information about each video watched, including the video title, timestamp, link, and channel name.

2. **YouTube API**:
    - Using the video IDs extracted from the Google Takeout dataset, the YouTube Data API was used to retrieve additional information. 
    - A script was written in Python to interact with the YouTube Data API. This script performed the following steps:
        1. **Authenticate**: Connect to the YouTube Data API using an API key.
        2. **Request Data**: For each video ID, send a request to the YouTube API to fetch video details.
        3. **Parse Response**: Extract relevant information from the API response, such as video tags, number of likes, number of comments, and other metadata.
        4. **Merge Data**: Combine the additional information from the YouTube API with the original Google Takeout data to create a more comprehensive dataset and output it in a CSV file.

## How to Use

**Step 1: Download YouTube Watch History Data**
Download Your YouTube Watch History Data:
- Go to Google Takeout.
- Select and download your YouTube data archive.
- Locate the downloaded file in your computer's directory.
- Find the HTML file named 'watch-history.html' within the archive.

**Step 2: Set Up YouTube API Access**
-Obtain a YouTube Data API Key:
-Go to YouTube Data API documentation.
-Follow the instructions to create and obtain your API key.
-Make sure to enable the YouTube Data API for your project.

**Step 3: Clone and Set Up the Repository**

## Run Locally

Clone the project

```bash
  git clone https://link-to-project
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  npm install
```

Start the server

```bash
  npm run start
```




