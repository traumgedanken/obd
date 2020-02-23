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
declare
    words text[] = array ['love', 'peace', 'sun', 'cloud', 'blue', 'red', 'pink', 'yellow', 'dog', 'girl', 'boy'];
    res text = '';
begin
    loop
        exit when length < 1;
        res := res || ' ' || words[random_range(0, 10)];
        length := length - 1;
    end loop;
    return res;
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
            random_text_simple(3),
            random_text_simple(1));
        number := number - 1;
    end loop;
end;
$$;

select randomteam(100000);
