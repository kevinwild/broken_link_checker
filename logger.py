import sqlite3
from datetime import datetime


class Logger:
    conn = None
    indentifier = None

    def initDB(self, conn):
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS requests "
                  "(id INTEGER PRIMARY KEY, "
                  "`domain` TEXT NOT NULL,"
                  "full_url TEXT NOT NULL,"
                  "status TEXT NOT NULL,"
                  "request_time TEXT NOT NULL,"
                  "msg TEXT, "
                  "date_rec REAL)")
        c.execute("CREATE TABLE IF NOT EXISTS errors "
                  "(id INTEGER PRIMARY KEY, "
                  "`domain` TEXT NOT NULL,"
                  "status TEXT,"
                  "date_rec REAL)")
        conn.commit()

    def closeDB(self):
        self.conn.close()

    def __init__(self, conn=None, db_name='logs.db'):
        if db_name == '':
            db_name = 'logs_db'
        if not conn:
            conn = sqlite3.connect(f"output/{db_name}")

        self.initDB(conn)
        self.conn = conn

    def log(self, payload=dict()):
        domain = payload.get('domain')
        full_url = payload.get('full_url')
        request_time = payload.get('request_time')
        status = payload.get('status')
        msg = payload.get('msg')
        c = self.conn.cursor()
        c.execute('INSERT INTO requests (domain,full_url,status,request_time, msg,date_rec) '
                  'VALUES (?,?,?,?,?,?)', (domain, full_url, status, request_time, msg, datetime.now()))
        self.conn.commit()
        return c.lastrowid

    def error(self, payload=dict()):
        domain = payload.get('domain')
        status = payload.get('status')

        c = self.conn.cursor()
        c.execute('INSERT INTO errors (domain, status, date_rec) '
                  'VALUES (?, ?, ?)', (domain, status, datetime.now()))
        self.conn.commit()
        return c.lastrowid
