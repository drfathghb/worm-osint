# 5. Buat ip_hunter.py
import requests
import json
import time
import sys
sys.path.append('..')
import config

class IPHunter:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': config.USER_AGENT})
    
    def check_ipinfo(self, ip):
        try:
            url = f'https://ipinfo.io/{ip}/json'
            r = self.session.get(url, timeout=config.TIMEOUT)
            return r.json() if r.status_code == 200 else {'error': True}
        except:
            return {'error': True}
    
    def check_geo(self, ip):
        try:
            url = f'http://ip-api.com/json/{ip}'
            r = self.session.get(url, timeout=config.TIMEOUT)
            return r.json() if r.status_code == 200 else {'error': True}
        except:
            return {'error': True}
    
    def check_abuseipdb(self, ip):
        if not config.API_KEYS.get('abuseipdb'):
            return {'error': 'no_api_key'}
        try:
            url = 'https://api.abuseipdb.com/api/v2/check'
            headers = {'Key': config.API_KEYS['abuseipdb'], 'Accept': 'application/json'}
            params = {'ipAddress': ip, 'maxAgeInDays': '90'}
            r = requests.get(url, headers=headers, params=params, timeout=config.TIMEOUT)
            return r.json() if r.status_code == 200 else {'error': True}
        except:
            return {'error': True}
    
    def scan(self, ip):
        print(f'\n[+] Investigating IP: {ip}')
        results = {
            'ip': ip,
            'timestamp': time.time(),
            'ipinfo': self.check_ipinfo(ip),
            'geo': self.check_geo(ip),
            'abuseipdb': self.check_abuseipdb(ip)
        }
        if results['ipinfo'] and not results['ipinfo'].get('error'):
            print(f'[+] Location: {results["ipinfo"].get("city")}, {results["ipinfo"].get("country")}')
        return results
    
    def save_results(self, results, filename=None):
        if not filename:
            filename = f'{config.DATA_DIR}/ip_{results["ip"]}_{int(time.time())}.json'
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f'\n[+] Saved: {filename}')
        return filename
