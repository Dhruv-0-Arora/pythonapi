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
# GEMINI_PROMPT = '''Using the text that I have provided below, please find the relevant information only from the text that is worthy for short form content based on the provided content's theme from an educational lens. Each section of relevant information must be between 60-120 words. Please repeat these sections word for word and divide the sections by a ` symbol. Please keep the punctuation and spacing exactly as it is. Everything should be exactly the way it was provided. Please provide me with around 20 sections of relevant information that is exactly formated the way it is given.
# Here are a couple examples of exactly how the relevant information should be formatted:
# `The shortest war in history lasted only 38 minutes. It occurred between Britain and Zanzibar on August 27, 1896. Zanzibar had declared independence from Britain, but its new sultan was unacceptable to the British government. When the ultimatum for him to step down was ignored, British warships bombarded the sultan's palace. The conflict ended swiftly with the surrender of Zanzibar's forces, solidifying its status as the shortest recorded war in history.`
# `Octopuses have three hearts. Two pump blood to the gills, while the third pumps oxygenated blood to the rest of the body. Additionally, their blood is blue due to a copper-based molecule called hemocyanin, which transports oxygen more efficiently in cold, low-oxygen environments like the deep sea. This unique adaptation helps octopuses thrive in their diverse habitats, showcasing the fascinating evolutionary solutions found in marine life.`
# `The world's largest desert isn't the Sahara; it's Antarctica. While it's covered in ice instead of sand, Antarctica meets the criteria of a desert: low precipitation and very little vegetation. With an area of around 14 million square kilometers, it's larger than the Sahara Desert and contains about 70% of the world's fresh water in the form of ice. Despite its icy landscape, Antarctica is a desert in its own right, showcasing the diversity of Earth's ecosystems.`

# Using the information I have provided below, please return exactly those lines in the exact format mentioned above, matching the information I provided. Please provide around 20 sections of relevant information.


# '''

GEMINI_PROMPT = '''Using the text that I have provided below, please find the relevant information that is worthy for short form content based on the provided content's theme from an educational lens. This relevant information should be between 60-120 words. Please repeat these sections word for word and divide the sections by a ` symbol. Please keep the punctuation and spacing exactly as it is. Everything should be exactly the way it was provided. 
This is an example of exactly how you should format the response: 
`section1`section2`section3`section4`section5`section6`section7`section8`section9`section10`section11`section12`section13`section14`section15`section16`section17`section18`section19`section20

Please provide me with around 20 sections of relevant information that is exactly formated word for word the way it is provided below:

'''


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
        self.valuable_information = []
        self.timestamps = []
        # checking to see if a value is either '' or '\n' or if removing all the \n's from the string results in an empty string and removing all of them
        
        while len(self.timestamps) < 20:
            self.find_valuable_information()       
        
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
        
        self.valuable_information = response.text.split("`")
        self.valuable_information = [valuable_info for valuable_info in self.valuable_information if valuable_info != '' and valuable_info != '\n' and valuable_info != '\n\n']
        for valuable_info in self.valuable_information:
            if valuable_info == '\n' or valuable_info == '' or valuable_info == '\n\n':
                continue
            valuable_info = valuable_info.split(" ")
            start = -1
            end = 0
            
            # iterating through the transcript to find the starting point where the valuable information starts and the ending point. This piece of code does this by finding the first word then iterating through the rest of the transcript to find the last word. If the middle words aren't the exact same then it will return and continue to the find the next instance of the first word.
            for i in range(len(self.transcript)):
                if valuable_info[0] in self.transcript[i]['text'].split():
                    start = self.transcript[i]['start']
                    for j in range(i, min(i + 4, len(self.transcript))):  # limit to next 3 words
                        if valuable_info[-1] in self.transcript[j]['text'].split():
                            if all(word in self.transcript[k]['text'].split() for k in range(i, j) for word in valuable_info):
                                end = self.transcript[j]['start'] + self.transcript[j]['duration']
                                break
                    if end != 0:
                        break

        if start != -1 and end != 0:
            self.timestamps.append((start, end))
        print (self.timestamps)
    

    # helping function to get the transcript in prompt format (full joined string)
    def getPromptTranscript(self):
        # formatting the transcript in a full string to give the prompt
        full_transcript = ' '.join([item['text'] for item in self.transcript])
        return full_transcript
    