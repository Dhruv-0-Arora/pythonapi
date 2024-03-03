from flask import Flask, request, jsonify

app = Flask(__name__)

# creating routes
@app.route('/')
def home():
    return "Home"

# creating a route where the <api user> can pass in a video link to create a video object
@app.route('/api/post-video', methods=['POST'])
def create_video():
    data = request.get_json()
    video_link = data.get('video')  # Extract the video link from the data
    print(video_link)
    # creating a new video object with the video link that is passed in the request
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)