create or replace function checkTeamBeforeDelete()
returns trigger
language plpgsql
as $$
declare
    newTeam team = (new::team);
    teams cursor is select * from team where country = newTeam.country and id != newTeam.id;
    minimumTotalPrice integer = 100;
    totalPrice integer = newTeam.price;
begin
    for team in teams
        loop
            totalPrice := totalPrice + team.price;
        end loop;

    if totalPrice < minimumTotalPrice then
        raise exception 'Total minimun price of teams in one country is 100';
    end if;

    return new;
end;
$$;

drop trigger beforeUpdate on team;

create trigger beforeUpdate before update on team
    for each row execute procedure checkTeamBeforeDelete();

insert into team(price, name, country)
values
    (50, 'foo', 'simple country'),
    (100, 'bar', 'simple country');

update team
set price = 60
where name = 'bar' and country = 'simple country';

update team
set price = 40
where name = 'bar' and country = 'simple country';

select * from team where country = 'simple country';