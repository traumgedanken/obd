create or replace function checkTeamBeforeDelete()
returns trigger
language plpgsql
as $$
begin
    if (old::team).price > 0 then
        return old;
    end if;
    raise exception 'Team should play some more games to earn money.';
end;
$$;

create trigger beforeDelete before delete on team
    for each row execute procedure checkTeamBeforeDelete();

drop trigger beforeDelete on team;

select * from team;
delete from team where price > 0;

delete from team where price <= 0;
