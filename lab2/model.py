import psycopg2
from pprint import pprint


class Model:
    def __init__(self):
        self.conn = psycopg2.connect("dbname='kpi' user='admin'"
                                     "host='localhost' password='admin'")
        self.cursor = self.conn.cursor()

    def create_tables(self):
        command = open('create.sql').read()
        self.cursor.execute(command)
        self.conn.commit()

    def insert(self, tname, **kwargs):
        cols = kwargs.keys()
        vals = [f"'{val}'" for val in kwargs.values()]
        comand = f'insert into {tname} ({", ".join(cols)}) ' + \
            f'values ({", ".join(vals)})'
        self.cursor.execute(comand)
        self.conn.commit()

    def get(self, tname, **kwargs):
        comand = f'select * from {tname}'

        if kwargs:
            conditions = [f"{col}='{kwargs[col]}'" for col in kwargs]
            comand = f'{comand} where {" and ".join(conditions)}'

        self.cursor.execute(comand)
        return self.cursor.fetchall()

    def update(self, tname, condition, **kwargs):
        column, value = condition
        updates = ', '.join([f"{col} = '{kwargs[col]}'" for col in kwargs])
        comand = f'update {tname} set {updates} where {column}={value}'

        self.cursor.execute(comand)
        self.conn.commit()

    def delete(self, tname, **kwargs):
        conditions = [f"{col}='{kwargs[col]}'" for col in kwargs]
        comand = f'delete from {tname} where {" and ".join(conditions)}'

        self.cursor.execute(comand)
        self.conn.commit()

    def get_teams_by_sporttype(self, sporttypes):
        sporttypes = [f"'{stype}'" for stype in sporttypes]
        comand = 'select name from team '\
            'inner join score on team.id=score.teamid '\
            'inner join game on game.id=score.gameid ' + \
            f'where sporttype in ({", ".join(sporttypes)})'

        self.cursor.execute(comand)
        return self.cursor.fetchall()

    def get_games_by_stadium_hascover(self, hascover):
        comand = 'select * from game '\
            'where id in (select gameid from event '\
            'inner join stadium on stadium.id=event.stadiumid ' + \
            f'where hascover={hascover})'

        self.cursor.execute(comand)
        return self.cursor.fetchall()

    def __del__(self):
        self.cursor.close()
        self.conn.close()


m = Model()
