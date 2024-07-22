from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp as youtube_dl
import os

app = Flask(__name__)
CORS(app)  # Enable CORS

DOWNLOAD_DIR = 'downloads'
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    video_id = data.get('url')

    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=True)
            filename = ydl.prepare_filename(info_dict)
            file_path = os.path.abspath(filename).replace(DOWNLOAD_DIR + '/', '')
            return jsonify({'message': 'Download successful', 'file_path': file_path})
    except Exception as e:
        return jsonify({'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)










# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import youtube_dl
# import os

# app = Flask(__name__)
# CORS(app)  # Enable CORS

# DOWNLOAD_DIR = 'downloads'
# if not os.path.exists(DOWNLOAD_DIR):
#     os.makedirs(DOWNLOAD_DIR)

# @app.route('/download', methods=['POST'])
# def download_video():
#     data = request.json
#     video_id = data.get('url')

#     ydl_opts = {
#         'format': 'best',
#         'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
#     }

#     try:
#         with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#             info_dict = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=True)
#             filename = ydl.prepare_filename(info_dict)
#             file_path = os.path.abspath(filename).replace(DOWNLOAD_DIR + '/', '')
#             return jsonify({'message': 'Download successful', 'file_path': file_path})
#     except Exception as e:
#         return jsonify({'message': str(e)})

# if __name__ == '__main__':
#     app.run(debug=True)
