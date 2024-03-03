from flask import Flask, request, jsonify
from video import Video

app = Flask(__name__)



# creating a route where the <api user> can pass in a video link to create a video object
@app.route('/api/post-video', methods=['POST'])
def create_video():

    # getting the api post request parameter of video link
    data = request.get_json()
    video_link = data.get('video') 
    
    # checking if video link is provided
    if video_link is None:
        return jsonify({"status": "failed", "message": "No video link provided"})

    # creating new video class with video_link
    new_video = Video(video_link)

    # returning if successful
    return jsonify({"status": "success"})




@app.route('/api/get-title', methods=['GET'])
def get_title():
    # getting the api get request parameter of video link
    video_link = request.args.get('video')
    
    # checking if video link is provided
    if video_link is None:
        return jsonify({"status": "failed", "message": "No video link provided"})

    # creating new video class with video_link
    new_video = Video(video_link)

    # returning the title
    return jsonify({"status": "success", "title": new_video.getTitle()})





# running the app
if __name__ == '__main__':
    app.run(debug=True)