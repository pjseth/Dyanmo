#PJ's Code
# import http.server
# import socketserver

# PORT = 8000

# Handler = http.server.SimpleHTTPRequestHandler

# httpd = socketserver.TCPServer(("", PORT), Handler)

# print("Serving at port", PORT)
# httpd.serve_forever()

import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving HTTP on port {PORT} ...")
    httpd.serve_forever()