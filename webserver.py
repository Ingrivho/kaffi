#! python3

import socket
import http.server
import socketserver


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
ip = s.getsockname()[0]
s.close()

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer((ip, PORT), Handler)

print("serving at", ip, PORT)
httpd.serve_forever()
