create or replace function random_range(integer, integer)
    returns integer
    language sql
    as $$
        select ($1 + floor(($2 - $1 + 1) * random() ))::integer;
    $$;

create or replace function random_text_simple(length integer)
    returns text
    language plpgsql
    as $$
    declare
        possible_chars text := '0123456789abcdefghijklmnopqrstuvwxyz';
        output text := '';
        i int4;
        pos int4;
    begin

        for i in 1..length loop
            pos := random_range(1, length(possible_chars));
            output := output || substr(possible_chars, pos, 1);
        end loop;

        return output;
    end;
    $$;

create or replace function randomteam(number int) returns void as $$
    begin
        loop
            exit when number < 0;
            insert into team(price, name, country)
            values (random_range(100, 10000), random_text_simple(20),  random_text_simple(20));
            number := number - 1;
        end loop;
    end;
$$ language plpgsql;
select randomteam(10000);
select * from team;
