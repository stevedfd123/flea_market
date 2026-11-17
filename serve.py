#!/usr/bin/env python3
"""Local preview server for the single-file Ceylon Flea Market demo.

Usage:  python3 serve.py [port]      (default port 8000)

Serves index.html for every route so client-side routes such as /events,
/sell and /about work on a hard refresh, and binds to 0.0.0.0 so the
sandbox preview proxy can reach it.
"""
import http.server
import os
import posixpath
import socketserver
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


class Handler(http.server.SimpleHTTPRequestHandler):
    # HTTP/1.1 keeps reverse proxies happy and avoids connection churn
    protocol_version = "HTTP/1.1"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def send_head(self):
        # SPA fallback: extension-less paths that don't exist on disk -> index.html
        path = urllib.parse.urlparse(self.path).path
        if not os.path.exists(super().translate_path(path)) and "." not in posixpath.basename(path):
            self.path = "/index.html"
        return super().send_head()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True
    request_queue_size = 64


if __name__ == "__main__":
    with Server(("0.0.0.0", PORT), Handler) as httpd:
        print(f"serving {ROOT} on http://0.0.0.0:{PORT}", flush=True)
        httpd.serve_forever()
