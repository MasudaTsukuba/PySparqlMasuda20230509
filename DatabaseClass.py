import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def execute(self, sql):
        return_list = self.cursor.execute(sql).fetchall()
        headers = [col[0] for col in self.cursor.description]
        results = [list(i) for i in return_list]
        return results, headers
