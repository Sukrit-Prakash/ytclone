from flask import Flask, request, jsonify, render_template
import os
import boto3

app = Flask(__name__)

# AWS Rekognition Configuration
AWS_ACCESS_KEY_ID = '010526240951'
AWS_SECRET_ACCESS_KEY = 's6CEgg7rPOXqIfMAapOfCtsDLDmGXoehcjR6Xakb'
AWS_REGION_NAME = 'us-east-1'  # e.g., us-east-1


rekognition_client = boto3.client(
    'rekognition',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)

def detect_labels(image_path):
    try:
        with open(image_path, 'rb') as image_file:
            image_bytes = image_file.read()

        response = rekognition_client.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=10
        )
        tags = [label['Name'] for label in response['Labels']]
        return tags
    except Exception as e:
        print(f"Error in detect_labels: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    file_path = os.path.join('static', file.filename)
    
    os.makedirs('static', exist_ok=True)
    file.save(file_path)

    tags = detect_labels(file_path)
    if tags:
        return jsonify({'tags': tags})
    else:
        return jsonify({'error': 'Image recognition failed'}), 500

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
        'key': 'YOUR_YOUTUBE_API_KEY'  # Replace with your YouTube API key
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


# AWS Rekognition Configuration
# AWS_ACCESS_KEY_ID = '010526240951'
# AWS_SECRET_ACCESS_KEY = 's6CEgg7rPOXqIfMAapOfCtsDLDmGXoehcjR6Xakb'
# AWS_REGION_NAME = 'us-east-1'  # e.g., us-east-1
