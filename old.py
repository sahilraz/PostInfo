import requests
import time
import random
from fake_useragent import UserAgent
import json

def analyze_instagram_profile(username):
    # Initialize fake user agent
    ua = UserAgent()
    
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
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }
    
    # Add random delays between actions
    time.sleep(random.uniform(0.1, 0.7))
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Set cookies to appear more human-like
    session.cookies.update({
        'wordpress_test_cookie': 'WP+Cookie+check',
        'pll_language': 'en',
        'gdpr_popup': '1'
    })
    
    try:
        # Add some jitter to the request timing
        time.sleep(random.uniform(0.05, 0.3))
        
        # Make the request with human-like headers and delays
        response = session.post(
            url,
            data=post_data,
            headers=headers,
            timeout=30
        )
        
        # Random delay before processing response
        time.sleep(random.uniform(0.2, 0.5))
        
        if response.status_code == 200:
            try:
                return response.json()
            except json.JSONDecodeError:
                return {
                    'error': 'Invalid JSON response',
                    'raw_response': response.text[:500]
                }
        else:
            return {
                'error': f'HTTP request failed with code {response.status_code}',
                'details': 'Server might be blocking automated requests',
                'suggestions': [
                    'Try using rotating proxies',
                    'Add more human-like interaction patterns',
                    'Try from a different IP address'
                ]
            }
            
    except requests.exceptions.RequestException as e:
        return {'error': f'Request failed: {str(e)}'}

# Example usage
if __name__ == '__main__':
    username = input("Enter Instagram username: ").strip()
    if not username:
        print(json.dumps({'error': 'Username is required'}, indent=2))
    else:
        result = analyze_instagram_profile(username)
        print(json.dumps(result, indent=2))