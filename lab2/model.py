import psycopg2

conn = psycopg2.connect("dbname='kpi' user='admin'"
                        "host='localhost' password='admin'")
cursor = conn.cursor()

TABLES = {
    'Game': ('Id', 'TicketSold', 'SportType', 'Date'),
    'Stadium': ('Id', 'Country', 'Seats', 'Hascover'),
    'Team': ('Id', 'Price', 'Country', 'Name'),
    'Score': ('GamedId', 'TeamId', 'Points'),
    'Event': ('GameId', 'StadiumId')
}


def create_tables():
    command = open('create.sql').read()
    cursor.execute(command)
    conn.commit()


def insert(tname, opts):
    cols = opts.keys()
    vals = [f"'{val}'" for val in opts.values()]
    comand = f'insert into {tname} ({", ".join(cols)}) ' + \
        f'values ({", ".join(vals)})'
    cursor.execute(comand)
    conn.commit()


def get(tname, opts=None):
    comand = f'select * from {tname}'

    if opts:
        conditions = [f"{col}='{opts[col]}'" for col in opts]
        comand = f'{comand} where {" and ".join(conditions)}'

    cursor.execute(comand)
    return cursor.fetchall()


def update(tname, condition, opts):
    try:
        column, value = condition
        updates = ', '.join([f"{col} = '{opts[col]}'" for col in opts])
        comand = f'update {tname} set {updates} where {column}={value}'

        cursor.execute(comand)
        conn.commit()
    except Exception as e:
        raise e
    finally:
        conn.commit()


def delete(tname, opts):
    try:
        conditions = [f"{col}='{opts[col]}'" for col in opts]
        comand = f'delete from {tname} where {" and ".join(conditions)}'

        cursor.execute(comand)
    except Exception as e:
        raise e
    finally:
        conn.commit()


def get_teams_by_sporttype(sporttypes):
    sporttypes = [f"'{stype}'" for stype in sporttypes]
    comand = 'select name from team '\
        'inner join score on team.id=score.teamid '\
        'inner join game on game.id=score.gameid ' + \
        f'where sporttype in ({", ".join(sporttypes)})'

    cursor.execute(comand)
    return cursor.fetchall()


def get_games_by_stadium_hascover(hascover):
    comand = 'select * from game '\
        'where id in (select gameid from event '\
        'inner join stadium on stadium.id=event.stadiumid ' + \
        f'where hascover={hascover})'

    cursor.execute(comand)
    return cursor.fetchall()
