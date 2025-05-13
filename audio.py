from flask import Flask, request, jsonify, send_from_directory
import os
import requests
import uuid
import subprocess
import threading
import time
import re

app = Flask(__name__)

TEMP_DIR = 'temp'

os.makedirs(TEMP_DIR, exist_ok=True)

def is_instagram_reel_url(url):
    """Check if the URL is a valid Instagram Reel URL"""
    instagram_reel_pattern = r'^(https?:\/\/)?(www\.)?instagram\.com\/reel\/[a-zA-Z0-9_-]+\/?(\?.*)?$'
    return re.match(instagram_reel_pattern, url) is not None

def delete_file_after_delay(path, delay=300):
    def delete():
        time.sleep(delay)
        if os.path.exists(path):
            os.remove(path)
    threading.Thread(target=delete).start()

@app.route('/', methods=['GET'])
def convert_reel_to_mp3():
    reel_url = request.args.get('url')
    if not reel_url:
        return jsonify({'error': 'No URL provided'}), 400
    
    # Validate Instagram Reel URL
    if not is_instagram_reel_url(reel_url):
        return jsonify({
            'error': 'Invalid Instagram Reel URL',
            'message': 'Please provide a valid Instagram Reel URL (e.g., https://www.instagram.com/reel/ABC123/)'
        }), 400

    try:
        # Step 1: Call your download API
        api_url = f"https://devilboy.shop/tanji/download.php?link={reel_url}"
        api_response = requests.get(api_url)
        json_data = api_response.json()

        if json_data.get("error") or "url" not in json_data["result"]:
            return jsonify({'error': 'Failed to download the reel'}), 500

        mp4_url = json_data["result"]["url"]

        # Step 2: Download MP4
        unique_id = uuid.uuid4().hex
        mp4_path = os.path.join(TEMP_DIR, unique_id + ".mp4")
        mp3_path = os.path.join(TEMP_DIR, unique_id + ".mp3")

        with open(mp4_path, "wb") as f:
            f.write(requests.get(mp4_url).content)

        # Step 3: Convert to MP3
        subprocess.run(['ffmpeg', '-i', mp4_path, '-vn', '-acodec', 'libmp3lame', mp3_path],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Step 4: Delete MP4 immediately
        if os.path.exists(mp4_path):
            os.remove(mp4_path)

        # Step 5: Schedule MP3 delete after 5 minutes
        delete_file_after_delay(mp3_path, delay=300)

        # Step 6: Return MP3 URL
        return jsonify({
            'status': 'success',
            'mp3_url': request.host_url.replace('http://', 'https://') + 'temp/' + os.path.basename(mp3_path)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/temp/<filename>')
def serve_file(filename):
    return send_from_directory(TEMP_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
    
