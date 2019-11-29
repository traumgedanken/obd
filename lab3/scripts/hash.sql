create index id_index on team using hash(id);

drop index id_index;

delete from team;

select count(*) from team;

select * from team where id = 15000;
