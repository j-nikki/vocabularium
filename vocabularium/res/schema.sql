begin;
create table if not exists word (
    lang_code text not null,
    word text not null,
    primary key (lang_code, word)
) without rowid;
create table if not exists etymology (
    lang_code text not null,
    word text not null,
    number number,
    text text,
    foreign key (lang_code, word) references word(lang_code, word) on delete cascade
);
create table if not exists etymology_template (
    etymology_id references etymology(rowid) on delete cascade,
    expansion text not null,
    name text not null
);
create table if not exists template_arg (
    template_id references etymology_template(rowid) on delete cascade,
    key text not null,
    value text not null,
    primary key (template_id, key)
) without rowid;
create table if not exists sense (
    etymology_id references etymology(rowid) on delete cascade,
    pos text
);
create table if not exists sense_gloss (
    sense_id references sense(rowid) on delete cascade,
    gloss text not null,
    primary key(sense_id, gloss)
) without rowid;
create table if not exists sense_example (
    sense_id references sense(rowid) on delete cascade,
    example text not null,
    type text,
    primary key(sense_id, example)
) without rowid;
create table if not exists sense_holonym (
    sense_id references sense(rowid) on delete cascade,
    word text not null,
    primary key(sense_id, word)
) without rowid;
create table if not exists sense_meronym (
    sense_id references sense(rowid) on delete cascade,
    word text not null,
    primary key(sense_id, word)
) without rowid;
create table if not exists sense_hypernym (
    sense_id references sense(rowid) on delete cascade,
    word text not null,
    primary key(sense_id, word)
) without rowid;
create table if not exists sense_hyponym (
    sense_id references sense(rowid) on delete cascade,
    word text not null,
    primary key(sense_id, word)
) without rowid;
create table if not exists sense_antonym (
    sense_id references sense(rowid) on delete cascade,
    word text not null,
    primary key(sense_id, word)
) without rowid;
create table if not exists sense_synonym (
    sense_id references sense(rowid) on delete cascade,
    word text not null,
    primary key(sense_id, word)
) without rowid;
create table if not exists sense_related (
    sense_id references sense(rowid) on delete cascade,
    word text not null,
    primary key(sense_id, word)
) without rowid;
commit;
