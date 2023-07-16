import json
from operator import itemgetter
import os
from pathlib import Path
import sqlite3
from argparse import ArgumentParser
import sys
from time import time_ns
from typing import Any

import pkg_resources

cachedir = os.getenv('XDG_DATA_HOME', os.path.expanduser('~/.local/share')) + '/vocabularium'
if not os.path.isdir(cachedir):
    os.makedirs(cachedir, exist_ok=True)

ap = ArgumentParser('vocabularium', description='A program serving an HTTP API for a vocabulary database.', epilog='The database is stored in a SQLite file. The default location is "$XDG_DATA_HOME/vocabularium/en.db". The database is created if it does not exist.')
ap.add_argument('--database', '-db', type=Path, default=f'{cachedir}/en.db')
ap.add_argument('input', nargs='?', type=Path, default=sys.stdin, help='A per-line listing of individual JSON objects, each representing a word. If not specified, read from stdin.')
args = ap.parse_args()

def _insert_word(cur: sqlite3.Cursor, data: Any):
    cur.execute('insert or ignore into word values (?,?);', (data['lang_code'], data['word']))
    cur.execute('insert into etymology values (?,?,?,?);', (data['lang_code'], data['word'], data.get('etymology_number'), data.get('text')))
    eid = cur.lastrowid
    for tmpl in data.get('etymology_templates', []):
        cur.execute('insert into etymology_template values (?,?,?);', (eid, tmpl['expansion'], tmpl['name']))
        tid = cur.lastrowid
        for k, v in tmpl.get('args', {}).items():
            cur.execute('insert into template_arg values (?,?,?);', (tid, k, v))
    for sense in data.get('senses', []):
        cur.execute('insert into sense values (?,?);', (eid, data['pos']))
        sid = cur.lastrowid
        for gloss in set(sense.get('glosses', [])):
            cur.execute('insert into sense_gloss values (?,?);', (sid, gloss))
        for text, type_ in {x['text']: x.get('type') for x in sense.get('examples', [])}.items():
            cur.execute('insert into sense_example values (?,?,?);', (sid, text, type_))
        for nym in ('holonyms','meronyms','hypernyms','hyponyms','antonyms','synonyms','related'):
            for word in set(map(itemgetter('word'), sense.get(nym, []))):
                cur.execute(f'insert into sense_{nym.rstrip("s")} values (?,?);', (sid, word))

def _main():
    with sqlite3.connect(str(args.database)) as con:
        cur = con.cursor()
        with open(pkg_resources.resource_filename('vocabularium.res', 'schema.sql'), encoding='U8') as f:
            schema = f.read()
        cur.executescript(schema)
        w, _ = os.get_terminal_size()
        t0 = time_ns()
        for i,x in enumerate(map(json.loads, args.input)):
            txt = f'\r{i:,} {x["word"][-20:]}'
            dur = f'{(time_ns() - t0) / 1e9:.2f}s'
            print(txt + ' ' * (w - len(txt) - len(dur)) + dur, end='', flush=True)
            _insert_word(cur, x)
        con.commit()

if __name__ == '__main__':
    _main()
