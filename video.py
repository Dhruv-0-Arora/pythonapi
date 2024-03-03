# this file uses object oriented programming to create a video class that will contain all the important information about each video.

# including:
# - title
# - transcript
# - timestamps
# - video_link






# importing the transcript api and other youtube api libraries
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build

# imports for the Gemini API
import Gemini
from IPython.display import Markdown


# final variable for the Gemini prompt
GEMINI_PROMPT = "Using the text that I have provided below, please find the relevant information that is worthy for short form content based on the provided content's theme from an educational lens. This relevant information should be between 60-120 words. Please repeat these sections word for word and divide the sections by a ';;;'. Please keep the punctuation and spacing exactly as it is. Everything should be exactly the way it was provided. Please provide me with around 20 sections of relevant information. Thank you! \n"


class Video:

    # initializing the video object
    def __init__(self, video_link):
        self.video_link = video_link
        self.video_id = Video.get_video_id(video_link)
        
        # getting the video title
        import json
        with open("config.json", "r") as file:
            api_key = json.load(file)['Google_API_Key']
        self.title = self.get_video_title(self.video_id, api_key)
        
        # discerning the valuable information using Gemini
        self.transcript = YouTubeTranscriptApi.get_transcript(self.video_id)
        self.valuable_information = self.find_valuable_information().split(";;;")
        
        # iterating through each of the valuable information and getting the timestamps from self.transcript
        self.timestamps = []
        for valuable_info in self.valuable_information:
            valuable_info = valuable_info.split(" ")
            start = -1
            for (i, item) in enumerate(self.transcript):
                if valuable_info[0] in item['text']:
                    start = item['start']
                    # continue traversing through valuable_info to see if the rest of the words are in the transcript
                    for word in valuable_info[1:]:
                        if word not in item['text'] and word not in self.transcript[i+1]['text']:
                            start = -1
                            break
                    break
            if start == -1:
                continue
                
        print (self.timestamps)


    # helping function to retrieve the video id from the video link
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


    # helping function to get the video title
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






    # function to get the title
    def getTitle(self):
        return self.title
    
    
    
    
    
    # function to prompt Gemini to discern the valuable information
    def find_valuable_information(self):
        response = Gemini.generate_response(f"{GEMINI_PROMPT} \n\n\n {self.getPromptTranscript()}")
        
        return response.text
    

    # helping function to get the transcript in prompt format (full joined string)
    def getPromptTranscript(self):
        # formatting the transcript in a full string to give the prompt
        full_transcript = ' '.join([item['text'] for item in self.transcript])
        return full_transcript
    