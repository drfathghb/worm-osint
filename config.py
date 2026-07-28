# config.py - Worm Aiva OSINT Config

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
REPORTS_DIR = BASE_DIR / 'reports'
WORDLISTS_DIR = BASE_DIR / 'wordlists'

API_KEYS = {
    'ipinfo': '',
    'shodan': '',
    'virustotal': '',
    'hunter': '',
    'numverify': '',
    'abstract': '',
    'securitytrails': '',
    'dehashed': '',
    'twitter': '',
    'abuseipdb': '',
}

TIMEOUT = 10
MAX_THREADS = 20
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

for dir_path in [DATA_DIR, REPORTS_DIR, WORDLISTS_DIR]:
    dir_path.mkdir(exist_ok=True)
