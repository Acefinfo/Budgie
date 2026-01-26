import threading
import webbrowser
import os
from http.server import HTTPServer, BaseHTTPRequestHandler


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """
    A request handler that processes OAuth callbacks and serves the Budgie logo image.

    This class handels two main tasks:
    1. Process the OAuth callback URL (eg. Extract excess token from query parameter. )
    2. Serve a branched HTML page indicating the result of the login attpmpt (Sucess or failure).
    3. Serve the Budgie logo for display in the Html response.

    Attribute:
        access_token(str): Stores the extracted OAuth token if avaliable.

    """

    # Class-level attribute to store the access token
    access_token = None

    def do_GET(self):
        """
        Handels the incomming GET requests.
        This method distinguishes between two type of requests:
        1. '/callback' : Handels the Outh callback and displays either sucess or failure page.
        2. '/budgie_logo.png' : Serves the Budgie logo image from the assets folder.

        If the requested URL is unreconized, a 404 Not Found response is returned.

        Flow
            - if the request is for the Budgie logo, it attempts to serve the image from the file system.
            - If the request is for the OAuth callback ('/callback'), it proccesses the quert parameters to extract the 
              access token and render the appropriate sucess or failure page.
            - Any other request result in a 404 response.
        """

        if self.path == "/budgie_logo.png":
            # Construct the absolute path to the Budgie logo file in the assets directory.
            base_dir = os.path.dirname(os.path.abspath(__file__))   # Get the current file's directory
            logo_path = os.path.join(base_dir, "..", "..", "assets", "Budgie_Logo.png") # Build path to logo
            logo_path = os.path.abspath(logo_path)  # Ensure the path is absolute

            # Check if the logo file exists
            if os.path.exists(logo_path):
                self.send_response(200)
                self.send_header("Content-type", "image/png")
                self.end_headers()
                with open(logo_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                # If the logo file does not exist, send a 404 Not Found response
                self.send_response(404)
                self.end_headers()
            return

        # Handle OAuth callback requests
        if self.path.startswith("/callback"):
            # Extract query parameters (e.g., access_token) from the URL
            if "?" in self.path:
                query = self.path.split("?", 1)[-1]  # Extract query string after "?"
                params = dict(q.split("=") for q in query.split("&") if "=" in q)   # Parse query parameters
                OAuthCallbackHandler.access_token = params.get("access_token")  # Save the access token

            # Respond with an appropriate HTML page based on the availability of the access token
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            # If an access token is present, render a login success page
            if OAuthCallbackHandler.access_token:
                html_content = """
                <html>
                    <head>
                        <meta charset="UTF-8">
                        <title>Login Successful - Budgie</title>
                        <style>
                            body {
                                background: linear-gradient(135deg, #74ebd5 0%, #9face6 100%);
                                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                                display: flex;
                                flex-direction: column;
                                align-items: center;
                                justify-content: center;
                                height: 100vh;
                                color: #333;
                                margin: 0;
                            }
                            .card {
                                background: white;
                                padding: 40px 60px;
                                border-radius: 16px;
                                box-shadow: 0 6px 20px rgba(0,0,0,0.15);
                                text-align: center;
                                animation: fadeIn 1s ease-in-out;
                            }
                            img {
                                width: 120px;
                                height: 120px;
                                border-radius: 50%;
                                object-fit: cover;
                                margin-bottom: 20px;
                                animation: popIn 0.8s ease;
                            }
                            h1 {
                                color: #4CAF50;
                                font-size: 2em;
                                margin-bottom: 10px;
                            }
                            p {
                                font-size: 1.1em;
                                color: #555;
                            }
                            @keyframes fadeIn {
                                from {opacity: 0; transform: translateY(20px);}
                                to {opacity: 1; transform: translateY(0);}
                            }
                            @keyframes popIn {
                                from {opacity: 0; transform: scale(0.8);}
                                to {opacity: 1; transform: scale(1);}
                            }
                        </style>
                    </head>
                    <body>
                        <div class="card">
                            <img src="/budgie_logo.png" alt="Budgie Logo" />
                            <h1>Login Successful!</h1>
                            <p>You can now safely close this window and return to <strong>Budgie app</strong>.</p>
                        </div>
                    </body>
                </html>
                """

            
            else:
                # If no access token is found, display a login failure page
                html_content = """
                <html>
                    <head>
                        <meta charset="UTF-8">
                        <title>Login Failed - Budgie</title>
                        <style>
                            body {
                                background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
                                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                                display: flex;
                                flex-direction: column;
                                align-items: center;
                                justify-content: center;
                                height: 100vh;
                                color: #333;
                                margin: 0;
                            }
                            .card {
                                background: white;
                                padding: 40px 60px;
                                border-radius: 16px;
                                box-shadow: 0 6px 20px rgba(0,0,0,0.15);
                                text-align: center;
                                animation: fadeIn 1s ease-in-out;
                            }
                            img {
                                width: 120px;
                                height: 120px;
                                border-radius: 50%;
                                object-fit: cover;
                                margin-bottom: 20px;
                            }
                            h1 {
                                color: #d32f2f;
                                font-size: 2em;
                                margin-bottom: 10px;
                            }
                            p {
                                font-size: 1.1em;
                                color: #555;
                            }
                            @keyframes fadeIn {
                                from {opacity: 0; transform: translateY(20px);}
                                to {opacity: 1; transform: translateY(0);}
                            }
                        </style>
                    </head>
                    <body>
                        <div class="card">
                            <img src="/budgie_logo.png" alt="Budgie Logo" />
                            <h1>❌ Login Failed</h1>
                            <p>No access token found. Please try logging in again.</p>
                        </div>
                    </body>
                </html>
                """

            # Send the HTML content (either sucess or failuer) as the response
            self.wfile.write(html_content.encode("utf-8"))
        else:
            # For any other unrecognized URL, return a 404 Not Found response
            self.send_response(404)
            self.end_headers()


def start_callback_server(port=5000):
    """
    Starts an HTTP Server to handle OAuthe callback requests.

    This function creates an HTTP server instance that listens for incomming GET requests,
    specifically targeting the '/callback' route. The server is set to run in the background , 
    in a swprate thread so the main program can continue executing.

    The server will process OAuth callback URLs, extract the access token and display a 
    sucess ot gailure page accordingly.

    :param port: The port noumber the server  will listen on. Default is 5000.
    :return: The HTTPServer instance that is running in the background.
    """

     # Set up and configure the HTTP server to listen on localhost (127.0.0.1) and the specified port
    server = HTTPServer(("127.0.0.1", port), OAuthCallbackHandler)

    # Start the server in a separate thread to handle incoming requests without blocking the main program
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = False   # Daemonize the thread, so it won't block the program from exiting
    thread.start()

    # Return the server instance in case additional control is needed
    return server


