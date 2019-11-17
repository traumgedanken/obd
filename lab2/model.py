import psycopg2

conn = psycopg2.connect("dbname='kpi' user='admin'"
                        "host='localhost' password='admin'")
cursor = conn.cursor()

TABLES = {
    'Game': ('Id', 'TicketSold', 'SportType', 'Date'),
    'Stadium': ('Id', 'Country', 'Seats', 'Hascover'),
    'Team': ('Id', 'Price', 'Country', 'Name'),
    'Score': ('GameId', 'TeamId', 'Points'),
    'Event': ('GameId', 'StadiumId')
}


def create_tables():
    with open('scripts/create.sql') as file:
        command = file.read()
        cursor.execute(command)
        conn.commit()


def insert(tname, opts):
    try:
        cols = opts.keys()
        vals = [f"'{val}'" for val in opts.values()]
        comand = f'insert into {tname} ({", ".join(cols)}) ' + \
            f'values ({", ".join(vals)})'
        cursor.execute(comand)
    finally:
        conn.commit()


def get(tname, opts=None):
    comand = f'select * from {tname}'

    if opts:
        conditions = [f"{col}='{opts[col]}'" for col in opts]
        comand = f'{comand} where {" and ".join(conditions)}'

    cursor.execute(comand)
    return cursor.fetchall(), TABLES[tname]


def update(tname, condition, opts):
    try:
        column, value = condition
        updates = ', '.join([f"{col} = '{opts[col]}'" for col in opts])
        comand = f'update {tname} set {updates} where {column}={value}'

        cursor.execute(comand)
        conn.commit()
    finally:
        conn.commit()


def delete(tname, opts):
    try:
        conditions = [f"{col}='{opts[col]}'" for col in opts]
        comand = f'delete from {tname} where {" and ".join(conditions)}'
        cursor.execute(comand)
    finally:
        conn.commit()


def get_teams_by_sporttype(sporttypes):
    sporttypes = [f"'{stype}'" for stype in sporttypes]
    comand = f'''
    select name from team
    join score on team.id=score.teamid
    join game on game.id=score.gameid
    where lower(sporttype) in ({", ".join(sporttypes)})'''

    cursor.execute(comand)
    return cursor.fetchall(), ('TeamName',)


def get_games_by_stadium_hascover(hascover):
    comand = f'''
    select * from game
    where id in (select gameid from event
    join stadium on stadium.id=event.stadiumid
    where hascover={hascover})'''

    cursor.execute(comand)
    return cursor.fetchall(), TABLES['Game']


def fts(query, contains):
    sql = f'''
    select gameid, name, sporttype from (
        select
            gameid,
            name,
            sporttype,
            to_tsvector(name) ||
            to_tsvector(sporttype) as document
        from score
        join game g on score.gameid = g.id
        join team t on score.teamid = t.id) search
    where search.document @@ to_tsquery('{'' if contains else '!'}{query}')'''
    cursor.execute(sql)
    return cursor.fetchall(), ('GameId', 'TeamName', 'SportType')


def create_random_teams():
    try:
        with open('scripts/random.sql', 'r') as file:
            sql = file.read()
            cursor.execute(sql)
    finally:
        conn.commit()


def execute(sql):
    try:
        cursor.execute(sql)
        return cursor.fetchall(), [desc[0] for desc in cursor.description]
    finally:
        conn.commit()
