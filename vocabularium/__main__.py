'''Entry point for the vocabularium command-line interface.'''

import os
import sqlite3
import sys
from argparse import ArgumentParser
from pathlib import Path

import pkg_resources

_datadir = os.getenv('XDG_DATA_HOME', os.path.expanduser('~/.local/share')) + '/vocabularium'
_ap = ArgumentParser('vocabularium',
                     description='serve an HTTP API for a vocabulary database',
                     epilog='The default database path is "$XDG_DATA_HOME/vocabularium/db".')
_ap.add_argument('--database', '-db', type=Path, default=f'{_datadir}/db')
_ap.add_argument('--verbose', '-v', action='store_true', help='print verbose output')

_subs = _ap.add_subparsers(dest='command', required=True)
_pins = _subs.add_parser('insert', help='insert words into the database')
_pins.add_argument('input', nargs='?', type=Path, default=sys.stdin,
                   help='a per-line listing of JSON objects, defaults to stdin')

_psrv = _subs.add_parser('serve', help='serve an HTTP API for a vocabulary database')
_psrv.add_argument('--host', '-H', default='localhost', help='the host to listen on')
_psrv.add_argument('--port', '-p', type=int, default=8080, help='the port to listen on')

_args = _ap.parse_args()

if _args.command:
    if not os.path.isdir(_datadir):
        os.makedirs(_datadir, exist_ok=True)
    con = sqlite3.connect(str(_args.database))
    with con:
        cur = con.cursor()
        with open(pkg_resources.resource_filename('vocabularium.res', 'schema.sql'), encoding='U8') as f:
            schema = f.read()
        cur.executescript(schema)
    with con:
        if _args.command == 'insert':
            from vocabularium.insert import insert
            insert(con.cursor(), _args)
        elif _args.command == 'serve':
            from vocabularium.serve import serve
            serve(con, _args)
