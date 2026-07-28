# 3. Buat username_scanner.py
import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor
import sys
sys.path.append('..')
import config

class UsernameScanner:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': config.USER_AGENT})
        self.timeout = config.TIMEOUT
        self.platforms = {
            'instagram': 'https://www.instagram.com/{}',
            'twitter': 'https://twitter.com/{}',
            'facebook': 'https://www.facebook.com/{}',
            'github': 'https://github.com/{}',
            'reddit': 'https://www.reddit.com/user/{}',
            'tiktok': 'https://www.tiktok.com/@{}',
            'telegram': 'https://t.me/{}',
            'linkedin': 'https://www.linkedin.com/in/{}',
            'snapchat': 'https://www.snapchat.com/add/{}',
            'twitch': 'https://www.twitch.tv/{}',
            'medium': 'https://medium.com/@{}',
            'youtube': 'https://www.youtube.com/@{}',
        }
    
    def check_platform(self, platform, url_template, username):
        try:
            url = url_template.format(username)
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            if response.status_code == 200:
                return {'platform': platform, 'url': url, 'status': 'found'}
            return {'platform': platform, 'url': url, 'status': 'not_found'}
        except:
            return {'platform': platform, 'url': url_template.format(username), 'status': 'error'}
    
    def scan(self, username):
        print(f'\n[+] Scanning username: {username}')
        results = {'username': username, 'timestamp': time.time(), 'found': []}
        with ThreadPoolExecutor(max_workers=config.MAX_THREADS) as executor:
            futures = []
            for platform, url_template in self.platforms.items():
                futures.append(executor.submit(self.check_platform, platform, url_template, username))
            for future in futures:
                result = future.result()
                if result['status'] == 'found':
                    print(f'[FOUND] {result["platform"]}: {result["url"]}')
                    results['found'].append(result)
        return results
    
    def save_results(self, results, filename=None):
        if not filename:
            filename = f'{config.DATA_DIR}/username_{results["username"]}_{int(time.time())}.json'
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f'\n[+] Saved: {filename}')
        return filename
