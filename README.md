# YouTube Live Video Comment Sentiment Analyzer

A real-time sentiment analysis system that analyzes comments posted during a YouTube Live stream and determines the emotional tone of viewers' reactions.

The system uses the **YouTube Data API** to collect live comments and applies **Natural Language Processing (NLP)** techniques to classify and analyze the sentiment of those comments.

## Overview

The YouTube Live Video Comment Sentiment Analyzer is designed to monitor audience reactions during a live YouTube stream.

The application:

1. Accepts a YouTube video URL.
2. Connects to the YouTube Data API.
3. Retrieves comments from the live stream.
4. Processes and cleans the comment text.
5. Analyzes sentiment using NLP techniques.
6. Takes emojis and sentiment patterns into consideration.
7. Displays the analyzed comments and sentiment information through a web interface.

## Key Features

* Real-time YouTube Live comment analysis.
* YouTube Data API integration.
* Natural Language Processing based sentiment analysis.
* Positive, negative, and neutral sentiment detection.
* Emoji-aware sentiment analysis.
* Context-aware sentiment patterns.
* Live comment updates.
* Interactive web interface.
* Flask-based backend.
* HTML, CSS, and JavaScript frontend.
* API endpoints for starting, updating, and resetting analysis.
* Health-check endpoint for monitoring the backend.

## System Architecture

```text
YouTube Live Stream
        |
        v
YouTube Data API
        |
        v
Flask Backend
        |
        v
Comment Collection
        |
        v
Text Preprocessing
        |
        v
Sentiment Analysis
        |
        v
Sentiment Results
        |
        v
HTML / CSS / JavaScript Frontend
```

## Technologies Used

### Backend

* Python
* Flask
* Flask-CORS

### NLP

* TextBlob
* Regular Expressions
* Emoji processing

### API

* YouTube Data API
* Google API Client

### Frontend

* HTML5
* CSS3
* JavaScript

## Project Structure

```text
youtube-liv-video-comment-sentiment-analyzer/
│
├── app.py
├── backend.py
├── backend.cpython-313.pyc
├── index.html
├── script.js
├── style.css
└── README.md
```

## Backend

The backend is implemented using Flask.

The main analyzer is defined in `backend.py` through the `YouTubeAnalyzer` class.

The analyzer connects to the YouTube Data API and processes comments collected from a YouTube video. It also includes sentiment patterns and emoji-based sentiment handling.

The Flask application in `app.py` initializes the analyzer and provides API endpoints for communication with the frontend.

## API Endpoints

### Start Analysis

```text
POST /start
```

Starts the analysis of a YouTube video.

Request example:

```json
{
    "video_url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

The endpoint sends the video URL to the analyzer and returns the analysis status and results.

### Get Comments

```text
GET /comments
```

Retrieves the current comments and sentiment statistics.

The backend updates the comments before returning the current analysis data.

### Reset Analysis

```text
POST /reset
```

Resets the current analysis data and starts a fresh analysis session.

### Health Check

```text
GET /health
```

Checks whether the Flask backend is running.

Example response:

```json
{
    "status": "ok",
    "message": "Server is running"
}
```

## Sentiment Analysis

The project uses **TextBlob** as part of its NLP-based sentiment analysis pipeline.

The backend also contains custom sentiment patterns and emoji handling to improve the interpretation of comments, particularly for expressions commonly used in social-media conversations.

Comments can be interpreted according to their overall emotional polarity, such as:

```text
Positive
Negative
Neutral
```

## YouTube Data API

The application uses the YouTube Data API to access comments from YouTube videos.

A valid YouTube API key is required for the application to communicate with the API.

The API key is passed to the `YouTubeAnalyzer` when the backend is initialized.

### Getting a YouTube API Key

1. Open Google Cloud Console.
2. Create or select a Google Cloud project.
3. Enable the YouTube Data API v3.
4. Create API credentials.
5. Generate an API key.
6. Configure the application to use the API key.

For security, API keys should not be publicly committed to GitHub. It is recommended to store the key in an environment variable instead of directly writing it inside the source code.

## Installation

Clone the repository:

```bash
git clone https://github.com/qadeesanoor/youtube-liv-video-comment-sentiment-analyzer.git
```

Move into the project directory:

```bash
cd youtube-liv-video-comment-sentiment-analyzer
```

Install the required Python packages:

```bash
pip install flask flask-cors textblob google-api-python-client emoji
```

## TextBlob Setup

If required, download the TextBlob/NLTK data:

```bash
python -m textblob.download_corpora
```

## Configuration

Configure your YouTube Data API key before running the application.

The analyzer requires an API key to initialize the YouTube API client.

For a safer configuration, an environment variable can be used:

```python
import os

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
```

Then set the environment variable before running the application.

On Windows Command Prompt:

```bash
set YOUTUBE_API_KEY=your_api_key
```

On PowerShell:

```powershell
$env:YOUTUBE_API_KEY="your_api_key"
```

## Running the Application

Start the Flask backend:

```bash
python app.py
```

The backend runs on:

```text
http://127.0.0.1:5000
```

Once the server is running, open:

```text
index.html
```

in a web browser.

The frontend communicates with the Flask backend to start the analysis and retrieve updated comments and sentiment information.

## How to Use

### Step 1

Start the Flask backend:

```bash
python app.py
```

### Step 2

Open the frontend:

```text
index.html
```

### Step 3

Enter the URL of a YouTube video or live stream.

### Step 4

Start the analysis.

### Step 5

The system communicates with the backend and retrieves available comments.

### Step 6

The comments are processed and analyzed for sentiment.

### Step 7

The frontend displays the analysis results.

## Frontend

The frontend consists of three main files:

### `index.html`

Provides the structure of the application interface.

### `style.css`

Controls the visual appearance and layout of the application.

### `script.js`

Handles frontend interactions and communication with the Flask API.

The JavaScript frontend communicates with backend endpoints such as:

```text
/start
/comments
/reset
/health
```

## Processing Pipeline

The comment-processing process can be summarized as:

```text
YouTube Comment
      |
      v
Comment Retrieval
      |
      v
Text Cleaning
      |
      v
Emoji Processing
      |
      v
Sentiment Pattern Analysis
      |
      v
TextBlob Sentiment Analysis
      |
      v
Sentiment Classification
      |
      v
Result Display
```

## Example Workflow

A user provides:

```text
https://www.youtube.com/watch?v=VIDEO_ID
```

The application sends the URL to:

```text
POST /start
```

The backend extracts the required video information and starts collecting comments.

The comments are then processed by the sentiment analyzer.

The frontend can request the current results using:

```text
GET /comments
```

The application returns the current comments and statistics for display.

## Error Handling

The backend handles several possible errors, including:

* Missing video URL.
* Invalid input.
* Invalid video information.
* API-related errors.
* Unexpected server errors.

The `/start` endpoint returns appropriate JSON responses when an error occurs.

## Health Monitoring

The `/health` endpoint can be used to verify that the Flask server is active.

Request:

```text
GET /health
```

Response:

```json
{
    "status": "ok",
    "message": "Server is running"
}
```

## Security Considerations

The YouTube API key should be kept private.

Do not commit a real API key directly to a public GitHub repository.

A recommended approach is to use environment variables:

```text
YOUTUBE_API_KEY
```

and exclude local configuration files containing secrets using `.gitignore`.

If an API key has already been exposed publicly, it should be revoked and replaced through Google Cloud Console.

## Limitations

* The application depends on the YouTube Data API.
* API quotas can limit the number of requests.
* Sentiment analysis may not correctly interpret sarcasm, slang, or highly contextual comments.
* Mixed-language comments may produce less reliable sentiment results.
* Internet access is required for retrieving live YouTube comments.
* The quality of results depends on the quality and context of the comments.

## Future Improvements

Possible improvements include:

* Support for multiple languages.
* More advanced transformer-based sentiment models.
* Improved sarcasm detection.
* Sentiment confidence scores.
* Sentiment trend graphs over time.
* Word clouds for frequently used terms.
* Comment filtering.
* Exporting analysis results to CSV.
* Real-time sentiment charts.
* Improved error messages.
* Secure environment-based API configuration.
* Deployment to a cloud platform.

## Conclusion

The YouTube Live Video Comment Sentiment Analyzer demonstrates how **YouTube API integration, Flask, JavaScript, and NLP** can be combined to analyze audience reactions in real time.

By automatically collecting and processing live comments, the system provides an overview of the emotional tone of viewers during a YouTube stream.
