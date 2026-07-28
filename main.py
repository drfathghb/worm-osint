#!/usr/bin/env python3

import sys
import os
import json
import time
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.username_scanner import UsernameScanner
from modules.email_hunter import EmailHunter
from modules.ip_hunter import IPHunter
from modules.domain_hunter import DomainHunter
import config

class OSINTSuite:
    def __init__(self):
        self.username_scanner = UsernameScanner()
        self.email_hunter = EmailHunter()
        self.ip_hunter = IPHunter()
        self.domain_hunter = DomainHunter()
        self.current_results = {}

    def clear_screen(self):
        os.system('clear')

    def banner(self):
        print("""
===========================================
   WORM AIVA OSINT SUITE PRO
   Author: OpetxDy
   TikTok: @opetxdy2
===========================================
        """)

    def menu(self):
        print("""
[1] Username Scanner
[2] Email Investigator
[3] IP Address Hunter
[4] Domain Investigator
[5] Full Scan
[6] View Results
[7] Generate Report
[0] Exit
        """)
        return input("[>] Pilih: ")

    def username_scan_flow(self):
        self.clear_screen()
        print("=== USERNAME SCANNER ===")
        username = input("[?] Username: ")
        if not username:
            return
        results = self.username_scanner.scan(username)
        self.username_scanner.save_results(results)
        self.current_results['username'] = results
        input("\n[>] Enter untuk lanjut...")

    def email_scan_flow(self):
        self.clear_screen()
        print("=== EMAIL INVESTIGATOR ===")
        email = input("[?] Email: ")
        if not email or '@' not in email:
            print("[!] Email invalid")
            return
        results = self.email_hunter.hunt(email)
        self.email_hunter.save_results(results)
        self.current_results['email'] = results
        input("\n[>] Enter untuk lanjut...")

    def ip_scan_flow(self):
        self.clear_screen()
        print("=== IP ADDRESS HUNTER ===")
        ip = input("[?] IP Address: ")
        if not ip:
            return
        results = self.ip_hunter.scan(ip)
        self.ip_hunter.save_results(results)
        self.current_results['ip'] = results
        input("\n[>] Enter untuk lanjut...")

    def domain_scan_flow(self):
        self.clear_screen()
        print("=== DOMAIN INVESTIGATOR ===")
        domain = input("[?] Domain: ")
        if not domain:
            return
        results = self.domain_hunter.scan(domain)
        self.domain_hunter.save_results(results)
        self.current_results['domain'] = results
        input("\n[>] Enter untuk lanjut...")

    def full_scan_flow(self):
        self.clear_screen()
        print("=== FULL SCAN ===")
        target = input("[?] Target (username/email/ip/domain): ")
        if not target:
            return
        print(f"\n[*] Scanning: {target}")
        
        print("\n[*] Username scan...")
        user_results = self.username_scanner.scan(target)
        self.username_scanner.save_results(user_results)
        
        if '@' in target:
            print("\n[*] Email scan...")
            email_results = self.email_hunter.hunt(target)
            self.email_hunter.save_results(email_results)
        
        try:
            import ipaddress
            ipaddress.ip_address(target)
            print("\n[*] IP scan...")
            ip_results = self.ip_hunter.scan(target)
            self.ip_hunter.save_results(ip_results)
        except:
            pass
        
        if '.' in target and not target.startswith('@'):
            print("\n[*] Domain scan...")
            domain_results = self.domain_hunter.scan(target)
            self.domain_hunter.save_results(domain_results)
        
        print("\n[+] Full scan selesai")
        input("\n[>] Enter untuk lanjut...")

    def view_results(self):
        self.clear_screen()
        print("=== LAST RESULTS ===")
        if not self.current_results:
            print("[!] Belum ada hasil")
            input("\n[>] Enter untuk lanjut...")
            return
        for key, value in self.current_results.items():
            print(f"\n[{key.upper()}]")
            print(json.dumps(value, indent=2)[:1000])
        input("\n[>] Enter untuk lanjut...")

    def generate_report(self):
        self.clear_screen()
        print("=== GENERATE REPORT ===")
        if not self.current_results:
            print("[!] Belum ada hasil")
            input("\n[>] Enter untuk lanjut...")
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{config.REPORTS_DIR}/report_{timestamp}.html"
        html = f"""<!DOCTYPE html>
<html>
<head><title>OSINT Report</title>
<style>
body{{background:#0a0a0a;color:#00ff00;font-family:monospace;padding:20px;}}
.section{{border:1px solid #00ff00;margin:10px 0;padding:10px;}}
pre{{background:#1a1a1a;padding:10px;}}
</style>
</head>
<body>
<h1>OSINT REPORT</h1>
<p>Generated: {timestamp}</p>
"""
        for key, value in self.current_results.items():
            html += f'<div class="section"><h2>{key.upper()}</h2><pre>{json.dumps(value, indent=2)}</pre></div>'
        html += "</body></html>"
        with open(filename, 'w') as f:
            f.write(html)
        print(f"[+] Report: {filename}")
        input("\n[>] Enter untuk lanjut...")

    def run(self):
        while True:
            self.clear_screen()
            self.banner()
            choice = self.menu()
            if choice == '1':
                self.username_scan_flow()
            elif choice == '2':
                self.email_scan_flow()
            elif choice == '3':
                self.ip_scan_flow()
            elif choice == '4':
                self.domain_scan_flow()
            elif choice == '5':
                self.full_scan_flow()
            elif choice == '6':
                self.view_results()
            elif choice == '7':
                self.generate_report()
            elif choice == '0':
                print("\n[*] Exit...")
                sys.exit(0)
            else:
                print("[!] Pilihan salah")
                time.sleep(1)

if __name__ == '__main__':
    try:
        app = OSINTSuite()
        app.run()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted")
        sys.exit(0)
