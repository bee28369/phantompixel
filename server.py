#!/usr/bin/env python3
"""
PhantomPixel — Local App Server (Desktop + iOS / Android Wi-Fi Preview)
"""
import http.server
import socket
import socketserver
import os

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        super().end_headers()


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    local_ip = get_local_ip()
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print("=" * 60)
        print("  PhantomPixel is running!")
        print(f"  • On this computer:      http://localhost:{PORT}")
        print(f"  • On your iPhone/Android: http://{local_ip}:{PORT}")
        print("=" * 60)
        httpd.serve_forever()
