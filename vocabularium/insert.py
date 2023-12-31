'''Database population logic for vocabularium.'''

import json
import sqlite3
import sys
from argparse import Namespace
from operator import itemgetter
from typing import Any, Callable

import pkg_resources


def _insert(tbl: str, *cols: str, nuniq: int | None = None):
    stmt = f'insert or ignore into {tbl} ({",".join(cols)}) values ({",".join("?"*len(cols))});'
    nuniq = nuniq or len(cols)
    idqry = f'select id from {tbl} where {" and ".join(f"{col}=?" for col in cols[:nuniq])};'
    def query(cur: sqlite3.Cursor, data: tuple) -> Callable[[], int]:
        cur.execute(stmt, data)
        return lambda: cur.execute(idqry, data[:nuniq]).fetchone()[0]
    return query

_insword = _insert('word', 'lang_code', 'word')
_insetym = _insert('etymology', 'word_id', 'number', 'text', nuniq=2)
_instmpl = _insert('etymology_template', 'etymology_id', 'expansion', 'name')
_inssense = _insert('sense', 'etymology_id', 'wiki_id', 'pos', nuniq=2)

def _insert_word(cur: sqlite3.Cursor, data: Any):
    wid = _insword(cur, (data['lang_code'], data['word']))()
    eid = _insetym(cur, (wid, data.get('etymology_number', 0), data.get('etymology_text')))()
    
    for tmpl in data.get('etymology_templates', []):
        tid = _instmpl(cur, (eid, tmpl['expansion'], tmpl['name']))()
        for k, v in tmpl.get('args', {}).items():
            cur.execute('insert or ignore into template_arg values (?,?,?);', (tid, k, v))

    for sense in data.get('senses', []):
        sid = _inssense(cur, (eid, sense['id'], data['pos']))()
        for gloss in set(sense.get('glosses', [])):
            cur.execute('insert or ignore into sense_gloss values (?,?);', (sid, gloss))
        for text, type_ in {x['text']: x.get('type') for x in sense.get('examples', [])}.items():
            cur.execute('insert or ignore into sense_example values (?,?,?);', (sid, text, type_))
        for nym in ('holonyms','meronyms','hypernyms','hyponyms','antonyms','synonyms','related'):
            for word in set(map(itemgetter('word'), sense.get(nym, []))):
                cur.execute(f'insert or ignore into sense_{nym.rstrip("s")} values (?,?);', (sid, word))

def insert(cur: sqlite3.Cursor, args: Namespace):
    '''Inserts words into the database.'''
    for i, x in enumerate(map(json.loads, args.input)):
        if args.verbose:
            sys.stderr.write(f'\r{i+1:,} {x["word"][-20:]:20}')
        _insert_word(cur, x)
