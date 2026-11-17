#!/usr/bin/env python3
"""Local preview server for the single-file Ceylon Flea Market demo.

Usage:  python3 serve.py [port]      (default port 8000)

- Serves index.html for every route, so /events, /sell, /about work on reload.
- Binds 0.0.0.0 so the sandbox preview proxy can reach it.
- Gzips the big single-file page when the client accepts it (~3.3 MB -> ~1.2 MB).
- Closes connections explicitly (Connection: close) to avoid keep-alive races
  with the reverse proxy in front of the sandbox.
"""
import gzip
import http.server
import io
import os
import posixpath
import socketserver
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

COMPRESSIBLE = (".html", ".htm", ".js", ".css", ".json", ".svg")
_gzip_cache = {}


def gzipped(path):
    """Return (data, mtime) for a gzip-compressed copy of a file, cached."""
    mtime = os.path.getmtime(path)
    cached = _gzip_cache.get(path)
    if cached and cached[1] >= mtime:
        return cached[0], cached[1]
    with open(path, "rb") as fh:
        raw = fh.read()
    data = gzip.compress(raw, 6)
    _gzip_cache[path] = (data, mtime)
    return data, mtime


class Handler(http.server.SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    timeout = 30

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def resolve(self, url_path):
        """Map a URL path to a file on disk, with SPA fallback to index.html."""
        fs = super().translate_path(url_path)
        if os.path.isdir(fs):
            fs = os.path.join(fs, "index.html")
        if not os.path.exists(fs) and "." not in posixpath.basename(url_path):
            fs = os.path.join(ROOT, "index.html")
        return fs

    def send_head(self):
        url_path = urllib.parse.urlparse(self.path).path
        target = self.resolve(url_path)
        ext = os.path.splitext(target)[1].lower()
        accepts_gzip = "gzip" in self.headers.get("Accept-Encoding", "").lower()
        if ext in COMPRESSIBLE and accepts_gzip and os.path.isfile(target):
            try:
                data, mtime = gzipped(target)
            except OSError:
                return self.send_error(404, "File not found")
            self.send_response(200)
            self.send_header("Content-Type", self.guess_type(target))
            self.send_header("Content-Encoding", "gzip")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Last-Modified", self.date_time_string(mtime))
            self.end_headers()
            return io.BytesIO(data)
        return super().send_head()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Connection", "close")
        self.close_connection = True
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
