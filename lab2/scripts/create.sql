create table stadium (
    id serial primary key,
    country varchar(20),
    seats integer,
    hascover boolean
);

create table team (
    id serial primary key,
    price integer,
    country varchar(20),
    name varchar(20)
);

create table game (
    id serial primary key,
    ticketsold integer,
    sporttype varchar(20),
    date timestamp
);

create table event (
    stadiumid integer not null,
    gameid integer not null,
    foreign key (stadiumid) references stadium(id),
    foreign key (gameid) references game(id),
    constraint pk_event primary key (stadiumid, gameid)
);

create table score (
    gameid integer not null,
    teamid integer not null,
    points integer,
    foreign key (gameid) references game(id),
    foreign key (teamid) references team(id),
    constraint pk_table primary key (gameid, teamid)
);