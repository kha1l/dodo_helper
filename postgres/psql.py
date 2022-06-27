import psycopg2
from config.conf import Config


class Database:
    @property
    def connection(self):
        cfg = Config()
        return psycopg2.connect(
            database=cfg.dbase,
            user=cfg.user,
            password=cfg.password,
            host=cfg.host,
            port='5432'
        )

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    def check_rest(self, name_rest: str):
        sql = '''
            SELECT name_rest from auto where name_rest=%s
        '''
        params = (name_rest,)
        return self.execute(sql, parameters=params, fetchone=True)

    def add_client(self, name: str, chat: str, post: str):
        sql = '''
            INSERT INTO users (name, chat, post) 
            VALUES (%s, %s, %s)
        '''
        parameters = (name, chat, post)
        self.execute(sql, parameters=parameters, commit=True)

