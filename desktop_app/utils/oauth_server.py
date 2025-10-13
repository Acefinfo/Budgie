# desktop_app/utils/oauth_server.py
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    access_token = None

    def do_GET(self):
        if self.path.startswith('/callback'):
            # Parse token from query params
            if '?' in self.path:
                query = self.path.split('?', 1)[-1]
                params = dict(q.split('=') for q in query.split('&') if '=' in q)
                OAuthCallbackHandler.access_token = params.get('access_token')

            # Respond to browser
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            if OAuthCallbackHandler.access_token:
                self.wfile.write(b"<h2> Login successful! You can close this window now.</h2>")
            else:
                self.wfile.write("<h2> Login failed — no access token found.</h2>")
        else:
            self.send_response(404)
            self.end_headers()

def start_callback_server(port=5000):
    server = HTTPServer(('127.0.0.1', port), OAuthCallbackHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return server
