# desktop_app/utils/oauth_server.py
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """
    This handler processes the OAuth callback request. It listens for a GET request to
    the `/callback` path, extracts the access token from the query parameters, and
    sends an appropriate response to the browser.

    Attributes:
        access_token (str): A class-level attribute that stores the received access token.
    """
    access_token = None

    def do_GET(self):
        """
        Handles GET requests. Specifically, it listens for the OAuth callback and
        extracts the access token from the URL query parameters.

        If the access token is successfully extracted, the handler responds with a success
        message; otherwise, it informs the user of the failure.

        The server responds with a simple HTML message indicating whether the login was successful.

        If the request is not a valid OAuth callback, a 404 error is returned.
        """
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
    """
    Starts a simple HTTP server that listens for the OAuth callback on the specified port.

    The server listens for incoming requests, and when it receives the OAuth callback,
    it processes the request to extract the access token.

    Args:
        port (int, optional): The port number the server will listen on. Defaults to 5000.

    Returns:
        HTTPServer: The server instance that is running in the background.
    """
    server = HTTPServer(('127.0.0.1', port), OAuthCallbackHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return server
