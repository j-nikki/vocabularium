'''Logic for serving an HTTP API for a vocabulary database.'''

from argparse import Namespace
from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from operator import itemgetter
import sqlite3
from urllib.parse import parse_qs, unquote, urlparse

import pkg_resources

_LIMIT = 50

with open(pkg_resources.resource_filename('vocabularium.res', 'query.sql'), encoding='U8') as f:
    _qry = f.read().replace('limit ?', f'limit {_LIMIT}')

class Handler(BaseHTTPRequestHandler):
    def __init__(self, cur: sqlite3.Cursor, *args, **kwargs):
        self.cur = cur
        super().__init__(*args, **kwargs)
    def do_GET(self):
        qry = urlparse(self.path)
        comps = parse_qs(qry.query)
        path = list(map(unquote, qry.path.split('/')[1:]))
        [word,*_] = path
        offset = int(comps.get('page', [0])[0]) * _LIMIT
        res = f'[{",".join(map(itemgetter(0), self.cur.execute(_qry, (word, offset))))}]'
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(res.encode('U8'))

def serve(con: sqlite3.Connection, args: Namespace):
    '''Serves an HTTP API for a vocabulary database.'''

    server = HTTPServer((args.host, args.port), partial(Handler, con.cursor()))
    print(f'listening on http://{args.host}:{args.port}/')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print('server closed')
