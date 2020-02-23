update team set doc_tsvector = to_tsvector(concat(country, ' ', name));
create index doc_index on team using gin(doc_tsvector);

drop index doc_index;

delete from team;

select count(*) from team;

select * from team where doc_tsvector @@ phraseto_tsquery('love blue red');
