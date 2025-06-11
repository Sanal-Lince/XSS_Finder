import argparse
from xss_lib.tester import XSSTester

def create_cli():
    parser = argparse.ArgumentParser(description="XSS Vulnerability Testing CLI Tool")
    parser.add_argument('url', help="URL to test for XSS vulnerabilities")
    parser.add_argument('-p', '--payload', help="Custom payload to test for XSS")
    parser.add_argument('--csp', action='store_true', help="Check for Content Security Policy (CSP) header")
    parser.add_argument('--dom', action='store_true', help="Test for DOM-based XSS")
    parser.add_argument('--event', action='store_true', help="Test for event handler-based XSS")
    parser.add_argument('--blind', action='store_true', help="Test for Blind XSS vulnerabilities")
    parser.add_argument('--mutation', action='store_true', help="Test for mutated XSS payloads")
    return parser

def main():
    parser = create_cli()
    args = parser.parse_args()

    xss_tester = XSSTester()

    if args.payload:
        print(f"Testing with custom payload: {args.payload}")
        xss_tester.test_payload(args.url, args.payload)
    if args.dom:
        print(f"Testing for DOM-based XSS on {args.url}")
        xss_tester.test_dom_xss(args.url, args.payload if args.payload else '<script>alert("XSS")</script>')
    if args.csp:
        print(f"Checking CSP for {args.url}")
        xss_tester.check_csp(args.url)
    if args.event:
        print(f"Testing for event handler XSS on {args.url}")
        xss_tester.test_event_handler(args.url, args.payload if args.payload else "<img src='nonexistent.jpg' onerror='alert(1)'>")
    if args.blind:
        print(f"Testing for Blind XSS on {args.url}")
        xss_tester.test_blind_xss(args.url, args.payload if args.payload else "<script>alert('Blind XSS')</script>")
    if args.mutation:
        print(f"Testing for mutated payloads on {args.url}")
        xss_tester.test_mutation_payloads(args.url)

if __name__ == '__main__':
    main()
