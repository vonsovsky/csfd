import sqlite3


class ConnManager:
    def __init__(self, file_name):
        self.file_name = file_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.file_name)
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


class CustomConnection:
    def __init__(self, file_name):
        self.file_name = file_name

    def cursor(self):
        return ConnManager(self.file_name)
