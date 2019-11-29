create or replace function random_range(integer, integer)
    returns integer
    language sql
    as $$
        select (random() * ($2 - $1) + $1)::integer;
    $$;

create or replace function random_text_simple(length integer)
    returns text
    language plpgsql
    as $$
    begin
        return substring(md5(random()::text), 1, length);
    end;
    $$;

create or replace function randomteam(number int)
    returns void
    language plpgsql
    as $$
    begin
        loop
            exit when number < 0;
            insert into team(price, name, country)
            values (
                random_range(100, 10000),
                random_text_simple(random_range(10, 20)), 
                random_text_simple(random_range(10, 20)));
            number := number - 1;
        end loop;
    end;
    $$;

select randomteam(10000);
