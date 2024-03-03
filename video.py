# this file uses object oriented programming to create a video class that will contain all the important information about each video.

# including:
# - title
# - transcript
# - timestamps
# - video_link

# importing the transcript api
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build

# imports for the Gemini API
import Gemini
from IPython.display import Markdown


class Video:

    def get_video_id(video_link):
        # Parse the URL
        parsed_url = urlparse(video_link)

        # Check if the URL is a YouTube URL
        if parsed_url.netloc == "www.youtube.com":
            # Extract the video ID from the query parameters
            video_id = parse_qs(parsed_url.query).get("v")
            if video_id:
                return video_id[0]

        # If the URL is not a YouTube URL or does not contain a video ID, return None
        return None


    # function to get the video title
    def get_video_title(self, video_id, api_key):
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        response = request.execute()

        # Extract the title from the response
        title = response['items'][0]['snippet']['title']
        return title

    # initializing the video object
    def __init__(self, video_link):
        self.video_link = video_link
        self.video_id = Video.get_video_id(video_link)
        
        # getting the video title
        with open("config.txt", "r") as file:
            api_key = file.read().strip()
        self.title = self.get_video_title(self.video_id, api_key)
        
        self.transcript = YouTubeTranscriptApi.get_transcript(self.video_id)
        self.prompt()


    # function to get the title
    def getTitle(self):
        return self.title
        
    def getPromptTranscript(self):
        # formatting the transcript in a full string to give the prompt
        full_transcript = ' '.join([item['text'] for item in self.transcript])
        return full_transcript
    
    def prompt(self):
        # getting the prompt transcript
        response = Gemini.generate_response("What is the difference between dogs and cats?")
        
        # creating a new Gemini object
        print(response.text)
    
    