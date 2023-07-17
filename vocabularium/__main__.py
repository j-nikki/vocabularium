'''Entry point for the vocabularium command-line interface.'''

import os
import sys
from argparse import ArgumentParser
from pathlib import Path

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

_args = _ap.parse_args()

if _args.command:
    if not os.path.isdir(_datadir):
        os.makedirs(_datadir, exist_ok=True)

if _args.command == 'insert':
    from vocabularium.insert import insert
    insert(_args)
