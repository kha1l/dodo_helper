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
            SELECT restName 
            from orders 
            where restName=%s
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

    def get_name(self):
        sql = '''
            SELECT restName 
            from orders
        '''
        return self.execute(sql, fetchall=True)

    def add_settings(self, user: str, mail: str, rest: str, login: str,
                     password: str, code: str, request: str, status: str, rest_id: int,
                     uuid: str):
        sql = '''
            insert into orders (username, email, restname, userlogs, userpass, 
                countrycode, requestid, status, restid, restuuid)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
        '''
        params = (user, mail, rest, login, password, code, request, status, rest_id, uuid)
        self.execute(sql, parameters=params, commit=True)

    def select_all_user_on_groups(self, post: str):
        sql = 'SELECT DISTINCT name, chat, post FROM users WHERE post=%s'
        parameters = (post,)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_birthday(self, rest: str):
        sql = 'SELECT person, post, age FROM Birthday WHERE name_rest=%s'
        parameters = (rest,)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_metrics(self, rest: str):
        sql = '''
            SELECT date, revenue, productivity, product, orders_hour, 
                    delivery, certificatess 
            from metrics 
            where name_rest=%s
        '''
        parameters = (rest, )
        return self.execute(sql, parameters, fetchone=True)

    def delete_prom(self, chat: str):
        sql = '''
            delete from users 
            where chat=%s
        '''
        parameters = (chat,)
        self.execute(sql, parameters=parameters, commit=True)

    def select_prom(self, chat: str):
        sql = '''
            SELECT name, post 
            FROM users 
            WHERE chat=%s
        '''
        parameters = (chat,)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_row_on_wait(self, date: str, rest: str):
        sql = '''
            SELECT person, number, meat, queue, delivery, orders 
            FROM wait 
            WHERE date=%s and name_rest=%s
        '''
        parameters = (date, rest)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_row_on_pause(self, date: str, rest: str):
        sql = '''
            SELECT person, begin, duration 
            FROM pause 
            WHERE date=%s and name_rest=%s
        '''
        parameters = (date, rest)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_row_on_later(self, date: str, rest: str):
        sql = '''
            SELECT person, duration 
            FROM later 
            WHERE date=%s and name_rest=%s
        '''
        parameters = (date, rest)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_row_on_over(self, date: str, n_date: str, rest: str):
        sql = '''
            SELECT person, type, date 
            FROM over 
            WHERE date between %s and %s and name_rest=%s
        '''
        parameters = (n_date, date, rest)
        return self.execute(sql, parameters=parameters, fetchall=True)


