# this file uses object oriented programming to create a video class that will contain all the important information about each video.

# including:
# - title
# - transcript
# - timestamps
# - video_link

# importing the 

class Video:
    def __init__(self, video_link):
        self.video_link = video_link
        self.title = ""

    def get_title(self):
        return self.title

    def get_transcript(self):
        return self.transcript

    def get_timestamps(self):
        return self.timestamps

    def get_video_link(self):
        return self.video_link

    def set_title(self, title):
        self.title = title

    def set_transcript(self, transcript