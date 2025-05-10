from flask import Flask, request, jsonify, send_file
import instaloader
import requests
import os
import tempfile
from urllib.parse import urlparse

app = Flask(__name__)

def get_audio_download_url(reel_url):
    try:
        # Initialize instaloader without login
        L = instaloader.Instaloader()
        L.context._session.headers.update({'User-Agent': 'Instagram 10.3.2'})
        
        # Extract shortcode from URL
        parsed = urlparse(reel_url)
        if not parsed.path.startswith('/reel/'):
            return None, "Invalid Instagram Reel URL"
            
        shortcode = parsed.path.split('/')[2]
        
        # Get post metadata
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        if not post.is_video:
            return None, "This post doesn't contain a video"
        
        # Create temp file
        temp_dir = tempfile.mkdtemp()
        audio_path = os.path.join(temp_dir, f"{shortcode}_audio.mp3")
        
        # Download video and extract audio
        video_url = post.video_url
        video_path = os.path.join(temp_dir, f"{shortcode}.mp4")
        
        # Download video
        with requests.get(video_url, stream=True) as r:
            r.raise_for_status()
            with open(video_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        # Convert to audio
        os.system(f"ffmpeg -i {video_path} -q:a 0 -map a {audio_path} -y -loglevel quiet")
        os.remove(video_path)
        
        return audio_path, None
        
    except Exception as e:
        return None, str(e)

@app.route('/download-audio', methods=['GET'])
def download_audio():
    reel_url = request.args.get('url')
    if not reel_url:
        return jsonify({"error": "URL parameter is required"}), 400
    
    audio_path, error = get_audio_download_url(reel_url)
    if error:
        return jsonify({"error": error}), 400
    
    return send_file(
        audio_path,
        as_attachment=True,
        download_name=f"instagram_audio.mp3",
        mimetype='audio/mpeg'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)