# 6. Buat domain_hunter.py
import requests
import json
import time
import whois
import dns.resolver
import socket
from concurrent.futures import ThreadPoolExecutor
import sys
sys.path.append('..')
import config

class DomainHunter:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': config.USER_AGENT})
        self.subdomain_wordlist = [
            'www', 'mail', 'ftp', 'webmail', 'smtp', 'pop', 'ns1', 'ns2',
            'cpanel', 'whm', 'autodiscover', 'autoconfig', 'm', 'imap',
            'test', 'ns', 'blog', 'pop3', 'dev', 'admin', 'forum',
            'news', 'vpn', 'support', 'mobile', 'mx', 'static', 'docs',
            'beta', 'shop', 'sql', 'secure', 'demo', 'cp', 'calendar',
            'wiki', 'web', 'media', 'email', 'images', 'img', 'download',
            'dns', 'api', 'app', 'stage', 'portal', 'help', 'info'
        ]
    
    def check_whois(self, domain):
        try:
            w = whois.whois(domain)
            return {
                'registrar': w.registrar,
                'creation_date': str(w.creation_date) if w.creation_date else None,
                'expiration_date': str(w.expiration_date) if w.expiration_date else None,
                'name_servers': w.name_servers,
                'org': w.org,
                'country': w.country
            }
        except:
            return {'error': True}
    
    def check_dns(self, domain):
        results = {}
        for record_type in ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                results[record_type] = [str(a) for a in answers]
            except:
                results[record_type] = []
        return results
    
    def check_subdomain(self, subdomain, domain):
        try:
            target = f'{subdomain}.{domain}'
            socket.gethostbyname(target)
            return {'subdomain': target, 'exists': True}
        except:
            return {'subdomain': target, 'exists': False}
    
    def enumerate_subdomains(self, domain):
        print(f'[+] Enumerating subdomains for: {domain}')
        found = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(self.check_subdomain, sub, domain) 
                      for sub in self.subdomain_wordlist]
            for future in futures:
                result = future.result()
                if result['exists']:
                    print(f'[FOUND] {result["subdomain"]}')
                    found.append(result['subdomain'])
        return found
    
    def scan(self, domain):
        print(f'\n[+] Investigating domain: {domain}')
        results = {
            'domain': domain,
            'timestamp': time.time(),
            'whois': self.check_whois(domain),
            'dns': self.check_dns(domain),
            'subdomains': self.enumerate_subdomains(domain)
        }
        if results['whois'] and not results['whois'].get('error'):
            print(f'[+] Registrar: {results["whois"].get("registrar")}')
        return results
    
    def save_results(self, results, filename=None):
        if not filename:
            filename = f'{config.DATA_DIR}/domain_{results["domain"]}_{int(time.time())}.json'
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f'\n[+] Saved: {filename}')
        return filename
