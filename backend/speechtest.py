from flask import Flask, request, jsonify, render_template
import requests
# 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
app = Flask(__name__)

YOUTUBE_API_KEY = 'YOUR_YOUTUBE_API_KEY'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search_youtube():
    data = request.json
    query = data.get('query')

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': 5,
        'key': 'AIzaSyAlZ9egFTO7aCHcFtCQ7UkgA8WQ-tpQvFk'
    }
    response = requests.get(url, params=params)
    videos = []
    if response.status_code == 200:
        items = response.json().get('items', [])
        for item in items:
            video_info = {
                'title': item['snippet']['title'],
                'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            }
            videos.append(video_info)
    return jsonify({'results': videos})

if __name__ == '__main__':
    app.run(debug=True)
