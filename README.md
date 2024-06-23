
# YouTube Watch History Data Extraction and Analysis Tool

This project aims to extract data from an HTML file provided by Google Takeout, containing the user's YouTube Watch History, including all of the videos watched with their titles and URLs, the uploader's channel and its URL, and the time they were viewed on YouTube. It will all be stored in a CSV file with additional information for each video, such as its duration, like count, comment count, and description, with the help of the YouTube API. The implementation of general descriptive approaches to the data will provide a comprehensive understanding of YouTube usage habits.


### The source dataset

The dataset for this analysis was created using a two-step process that involved web scraping and API requests to gather comprehensive information about the YouTube watch history.

![](youtube_watch_analytics/Output CSV file (1).gif)


A Python script named `youtube_scraper.py` was utilized to extract data from an HTML file of YouTube History. This HTML file was obtained through Google Takeout, which provides a detailed export of a user's YouTube activity. Using the BeautifulSoup library, the script parsed the HTML file to extract essential information for each video, including the video title, URL, the time it was played, the channel that posted it, and the channel's URL. This information was then saved into a CSV file named `youtube_data.csv`.

However, the HTML file from Google Takeout did not provide all the details required for a comprehensive analysis. To enrich the dataset with additional information, another Python script named `youtube_api.py` was created. This script aimed to fill in the gaps by fetching more data through the YouTube Data API. For each video entry in `youtube_data.csv`, the script extracted the video ID from the URL. With the video ID in hand, the script made API requests to gather further details such as the video's duration, the number of likes it had received, and the total number of comments. This additional data provided a more comprehensive view of each video.

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

## Project Structure

- **Data Collection**: Scripts for extracting and collecting data from Google Takeout.
- **Data Cleaning**: Steps to clean and preprocess the data to ensure it is ready for analysis.
- **Data Analysis**: Notebooks containing analysis and visualizations to uncover insights and trends.
- **Results**: Summary of findings and key takeaways from the analysis.

## How to Use

1. **Clone the Repository**: `git clone https://github.com/your-username/your-repository.git`
2. **Install Dependencies**: `pip install -r requirements.txt`
3. **Run Notebooks**: Open and run the Jupyter Notebooks to reproduce the analysis.

## Requirements

- Python 3.x
- Jupyter Notebook
- pandas
- numpy
- matplotlib
- seaborn
