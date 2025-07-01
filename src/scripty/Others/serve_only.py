import os
import ssl
from http.server import HTTPServer, SimpleHTTPRequestHandler
from functools import partial

# --- SETTINGS ---
BASE_DIR      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_DIR      = os.path.join(BASE_DIR, "medium_ready_articles")
STORAGE_STATE = os.path.join(BASE_DIR, "storageState.json")

# Paths to SSL certificate/key for HTTPS
CERT_DIR   = os.path.join(BASE_DIR, "certs")
CERT_FILE  = os.path.join(CERT_DIR, "localhost.pem")
KEY_FILE   = os.path.join(CERT_DIR, "localhost-key.pem")

def main():
    PORT = 12345
    handler = partial(SimpleHTTPRequestHandler, directory=HTML_DIR)
    httpd    = HTTPServer(("localhost", PORT), handler)
    ctx      = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(CERT_FILE, KEY_FILE)
    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
    print(f"🚀 HTTPS server running at https://localhost:{PORT}/ serving {HTML_DIR}")
    httpd.serve_forever()

if __name__ == "__main__":
    main()