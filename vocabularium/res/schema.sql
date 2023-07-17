begin;
create table if not exists word (
    id integer primary key,
    lang_code text not null,
    word text not null,
    unique (lang_code, word)
);
create table if not exists etymology (
    id integer primary key,
    word_id text references word(id) on delete cascade,
    number number not null,
    text text,
    unique (word_id, number)
);
create table if not exists etymology_template (
    id integer primary key,
    etymology_id integer references etymology(id) on delete cascade,
    expansion text not null,
    name text not null,
    unique (etymology_id, expansion, name)
);
create table if not exists template_arg (
    template_id integer references etymology_template(id) on delete cascade,
    key text not null,
    value text not null,
    primary key (template_id, key)
) without rowid;
create table if not exists sense (
    id integer primary key,
    etymology_id integer references etymology(id) on delete cascade,
    wiki_id text not null,
    pos text,
    unique (etymology_id, wiki_id)
);
create table if not exists sense_gloss (
    sense_id integer references sense(id) on delete cascade,
    gloss text not null,
    primary key(sense_id, gloss)
) without rowid;
create table if not exists sense_example (
    sense_id integer references sense(id) on delete cascade,
    example text not null,
    type text,
    primary key(sense_id, example)
) without rowid;
create table if not exists sense_holonym (
    sense_id integer references sense(id) on delete cascade,
    word text not null,
    primary key(sense_id, word)
) without rowid;
create table if not exists sense_meronym (
    sense_id integer references sense(id) on delete cascade,
    word text not null,
    primary key(sense_id, word)
) without rowid;
create table if not exists sense_hypernym (
    sense_id integer references sense(id) on delete cascade,
    word text not null,
    primary key(sense_id, word)
) without rowid;
create table if not exists sense_hyponym (
    sense_id integer references sense(id) on delete cascade,
    word text not null,
    primary key(sense_id, word)
) without rowid;
create table if not exists sense_antonym (
    sense_id integer references sense(id) on delete cascade,
    word text not null,
    primary key(sense_id, word)
) without rowid;
create table if not exists sense_synonym (
    sense_id integer references sense(id) on delete cascade,
    word text not null,
    primary key(sense_id, word)
) without rowid;
create table if not exists sense_related (
    sense_id integer references sense(id) on delete cascade,
    word text not null,
    primary key(sense_id, word)
) without rowid;
create view if not exists sense_all as
select s.id as sense_id,
    json_object(
        'glosses',
        (
            select json_group_array(sg.gloss)
            from sense_gloss sg
            where s.id = sg.sense_id
        ),
        'examples',
        (
            select json_group_array(se.example)
            from sense_example se
            where s.id = se.sense_id
        ),
        'holonyms',
        (
            select json_group_array(sh.word)
            from sense_holonym sh
            where s.id = sh.sense_id
        ),
        'meronyms',
        (
            select json_group_array(sm.word)
            from sense_meronym sm
            where s.id = sm.sense_id
        ),
        'hyponyms',
        (
            select json_group_array(shy.word)
            from sense_hyponym shy
            where s.id = shy.sense_id
        ),
        'hypernyms',
        (
            select json_group_array(shp.word)
            from sense_hypernym shp
            where s.id = shp.sense_id
        ),
        'antonyms',
        (
            select json_group_array(sa.word)
            from sense_antonym sa
            where s.id = sa.sense_id
        ),
        'synonyms',
        (
            select json_group_array(ss.word)
            from sense_synonym ss
            where s.id = ss.sense_id
        ),
        'related',
        (
            select json_group_array(sr.word)
            from sense_related sr
            where s.id = sr.sense_id
        )
    ) as json
from sense s;
commit;
