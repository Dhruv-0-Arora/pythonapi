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
GEMINI_PROMPT = "Using the text that I have provided below, please find the relevant information that is worthy for short form content based on the provided content's theme from an educational lens. This relevant information should be between 60-120 words. Please repeat these sections word for word and divide the sections by a ` symbol. Please keep the punctuation and spacing exactly as it is. Everything should be exactly the way it was provided. Please provide me with around 20 sections of relevant information. Thank you! \n"


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
        self.valuable_information = self.find_valuable_information().split("`")
        self.valuable_information = [info for info in self.valuable_information if info and info.strip('\n')]
        self.valuable_information = [info for info in self.valuable_information if info]
        
        print (self.valuable_information)
        
        # iterating through each of the valuable information and getting the timestamps from self.transcript
        self.timestamps = []
        for valuable_info in self.valuable_information:
            valuable_info = valuable_info.split(" ")
            print (valuable_info)
            start = -1
            end = 0
            
            # iterating through the transcript to find the starting point where the valuable information starts and the ending point. This piece of code does this by finding the first word then iterating through the rest of the transcript to find the last word. If the middle words aren't the exact same then it will return and continue to the find the next instance of the first word.
            for i in range(len(self.transcript)):
                if valuable_info[0] in self.transcript[i]['text'].split():
                    start = self.transcript[i]['start']
                    for j in range(i, len(self.transcript)):
                        if valuable_info[-1] in self.transcript[j]['text'].split():
                            if all(word in self.transcript[k]['text'].split() for k in range(i, j) for word in valuable_info):
                                end = self.transcript[j]['start']
                                break
                    if end != 0:
                        break

            if start != -1 and end != 0:
                self.timestamps.append((start, end))
                
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
        response = Gemini.generate_response(f"{GEMINI_PROMPT} {self.getPromptTranscript()}")
        print (response.text)
        return response.text
    

    # helping function to get the transcript in prompt format (full joined string)
    def getPromptTranscript(self):
        # formatting the transcript in a full string to give the prompt
        full_transcript = ' '.join([item['text'] for item in self.transcript])
        return full_transcript
    