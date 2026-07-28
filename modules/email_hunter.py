# 4. Buat email_hunter.py
import requests
import hashlib
import json
import time
import dns.resolver
import sys
sys.path.append('..')
import config

class EmailHunter:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': config.USER_AGENT})
    
    def check_gravatar(self, email):
        email_hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
        url = f'https://www.gravatar.com/{email_hash}?d=404'
        try:
            r = self.session.get(url, timeout=config.TIMEOUT)
            return {'exists': r.status_code == 200, 'hash': email_hash}
        except:
            return {'exists': False, 'error': True}
    
    def check_hibp(self, email):
        try:
            url = f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}'
            r = self.session.get(url, timeout=config.TIMEOUT)
            if r.status_code == 200:
                data = r.json()
                return {'breaches': len(data), 'details': data}
            return {'breaches': 0}
        except:
            return {'error': True}
    
    def check_emailrep(self, email):
        try:
            url = f'https://emailrep.io/{email}'
            r = self.session.get(url, timeout=config.TIMEOUT)
            if r.status_code == 200:
                return r.json()
            return {'error': True}
        except:
            return {'error': True}
    
    def check_domain(self, email):
        domain = email.split('@')[1] if '@' in email else ''
        if not domain:
            return {'error': 'invalid_email'}
        results = {}
        try:
            mx = dns.resolver.resolve(domain, 'MX')
            results['mx'] = [str(record.exchange) for record in mx]
        except:
            results['mx'] = []
        try:
            spf = dns.resolver.resolve(domain, 'TXT')
            results['spf'] = [str(r) for r in spf if 'v=spf1' in str(r)]
        except:
            results['spf'] = []
        return results
    
    def hunt(self, email):
        print(f'\n[+] Investigating email: {email}')
        results = {
            'email': email,
            'timestamp': time.time(),
            'gravatar': self.check_gravatar(email),
            'hibp': self.check_hibp(email),
            'emailrep': self.check_emailrep(email),
            'domain': self.check_domain(email)
        }
        if results['gravatar']['exists']:
            print('[+] Gravatar exists')
        if isinstance(results['hibp'], dict) and results['hibp'].get('breaches', 0) > 0:
            print(f'[!] Found in {results["hibp"]["breaches"]} breaches')
        return results
    
    def save_results(self, results, filename=None):
        if not filename:
            filename = f'{config.DATA_DIR}/email_{results["email"]}_{int(time.time())}.json'
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f'\n[+] Saved: {filename}')
        return filename
