select json_object(
        'word',
        w.word,
        'etymology_text',
        e.text,
        'etymology_number',
        e.number,
        'etymologies',
        (
            select json_group_array(json(json))
            from (
                    select et.id,
                        json_patch(
                            json_object('expansion', et.expansion, 'name', et.name),
                            json_group_object(ta.key, ta.value)
                        ) as json
                    from etymology_template et
                        join template_arg ta on et.id = ta.template_id
                    where et.etymology_id = e.id
                )
            order by id
        ),
        'senses',
        (
            select json_group_array(json(json))
            from sense s
                join sense_all sa on sa.sense_id = s.id
            where s.etymology_id = e.id
        )
    ) as json
from word w
    join etymology e on e.word_id = w.id
where word regexp(?)
limit ? offset ?;
