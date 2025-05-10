from flask import Flask, request, jsonify
import requests
import time
import random
from fake_useragent import UserAgent
import json

app = Flask(__name__)
ua = UserAgent()

def make_human_like_request(username):
    # Configure request parameters
    url = 'https://www.pathsocial.com/wp-admin/admin-ajax.php'
    
    # Random delay between 1-5 seconds
    time.sleep(random.uniform(1, 5))
    
    # Form data
    post_data = {
        'action': 'get_instagram_data_for_analyzer',
        'account_handle': username,
        'source': 'Free Instagram Profile Analyzer | Path Social'
    }
    
    # Headers with random user agent
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': ua.random,
        'Referer': 'https://www.pathsocial.com/free-instagram-tools/instagram-profile-analyzer',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://www.pathsocial.com',
        'Connection': 'keep-alive'
    }
    
    # Create session
    session = requests.Session()
    
    # Set cookies
    session.cookies.update({
        'wordpress_test_cookie': 'WP+Cookie+check',
        'pll_language': 'en'
    })
    
    try:
        response = session.post(url, data=post_data, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                'error': f'HTTP {response.status_code}',
                'message': 'Request blocked by server'
            }
    except Exception as e:
        return {'error': str(e)}

@app.route('/analyze', methods=['GET'])
def analyze():
    username = request.args.get('username', '').strip()
    if not username:
        return jsonify({'error': 'Username parameter is required'}), 400
    
    result = make_human_like_request(username)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)