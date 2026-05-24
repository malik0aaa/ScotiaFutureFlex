from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
Handler = partial(SimpleHTTPRequestHandler, directory=str(ROOT))


class Server(ThreadingHTTPServer):
    allow_reuse_address = True


with Server(("127.0.0.1", 3000), Handler) as httpd:
    host, port = httpd.server_address
    print(f"Serving {ROOT} on http://{host}:{port}/", flush=True)
    httpd.serve_forever()
