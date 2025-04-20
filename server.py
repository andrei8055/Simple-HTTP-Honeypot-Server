import argparse
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote

class CustomHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, headers=None, routes_dir=None, default_body=None, **kwargs):
        self.custom_headers = headers or {}
        self.routes_dir = routes_dir or "routes"
        self.default_body = default_body or b"Default response"
        super().__init__(*args, **kwargs)

    def send_response(self, code, message=None):
        """Override to skip default 'Server' and 'Date' headers"""
        self.log_request(code)
        self.send_response_only(code, message)
        # Don't call send_header('Server', ...) or send_header('Date', ...)
        # We'll handle headers ourselves in handle_request()

    def handle_request(self):
        path = unquote(self.path).lstrip('/')
        if not path:
            path = 'index'

        # Read and log the request body (if any)
        content_length = int(self.headers.get('Content-Length', 0))
        body_data = self.rfile.read(content_length) if content_length > 0 else b''
        try:
            decoded_body = body_data.decode('utf-8')
        except UnicodeDecodeError:
            decoded_body = "<binary data>"

        print(f"\n--- Incoming {self.command} {self.path} ---")
        print(f"Headers: {dict(self.headers)}")
        if content_length > 0:
            print(f"Body: {decoded_body}")
        else:
            print("Body: <empty>")

        # Load response body from file
        file_path = os.path.join(self.routes_dir, f"{path}.html")
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                response_body = f.read()
        else:
            response_body = self.default_body

        self.send_response(200)
        for key, value in self.custom_headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(response_body)


    # Support all HTTP methods
    def do_GET(self): self.handle_request()
    def do_POST(self): self.handle_request()
    def do_PUT(self): self.handle_request()
    def do_DELETE(self): self.handle_request()
    def do_PATCH(self): self.handle_request()
    def do_OPTIONS(self): self.handle_request()
    def do_HEAD(self):
        self.send_response(200)
        for key, value in self.custom_headers.items():
            self.send_header(key, value)
        self.end_headers()


def run_server(port, headers_file, default_body_file, routes_dir):
    # Load headers
    headers = {}
    if headers_file:
        with open(headers_file, 'r') as f:
            headers = json.load(f)

    # Load default body
    default_body = b"Default response"
    if default_body_file:
        with open(default_body_file, 'rb') as f:
            default_body = f.read()

    def handler(*args, **kwargs):
        CustomHandler(*args, headers=headers, default_body=default_body, routes_dir=routes_dir, **kwargs)

    server = HTTPServer(('0.0.0.0', port), handler)
    print(f"Serving on http://0.0.0.0:{port}")
    server.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Custom HTTP Server with Routes and Headers")
    parser.add_argument('--port', type=int, default=8000, help='Port to listen on')
    parser.add_argument('--headers', type=str, help='Path to JSON file with response headers')
    parser.add_argument('--body', type=str, help='Path to default body file (fallback)')
    parser.add_argument('--routes', type=str, default='routes', help='Directory containing route HTML files')
    args = parser.parse_args()

    run_server(args.port, args.headers, args.body, args.routes)
