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
commit;
