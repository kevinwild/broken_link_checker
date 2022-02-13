import sqlite3
from datetime import datetime
import config


class Logger:
    conn = None
    indentifier = None

    def initDB(self, conn):
        header_cols = self.build_header_columns()
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS requests "
                  "(id INTEGER PRIMARY KEY, "
                  "`domain` TEXT NOT NULL,"
                  "batch INTEGER NOT NULL,"
                  "full_url TEXT NOT NULL,"
                  "status TEXT NOT NULL,"
                  "request_time TEXT NOT NULL,"
                  f"{header_cols}"
                  "msg TEXT, "
                  "date_rec REAL)")
        c.execute("CREATE TABLE IF NOT EXISTS errors "
                  "(id INTEGER PRIMARY KEY, "
                  "`domain` TEXT NOT NULL,"
                  "batch integer NOT NULL,"
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
        self.batch = self.set_batch_num()

    def log(self, payload=dict()):
        domain = payload.get('domain')
        full_url = payload.get('full_url')
        request_time = payload.get('request_time')
        from_cache = payload.get('from_cache')
        brand = payload.get('brand')
        theme = payload.get('theme')

        status = payload.get('status')
        msg = payload.get('msg')
        c = self.conn.cursor()
        c.execute(
            'INSERT INTO requests (domain,batch,full_url,status,request_time,from_cache,brand,theme, msg,date_rec) '
            'VALUES (?,?,?,?,?,?,?,?,?,?)',
            (domain, self.batch, full_url, status, request_time, from_cache, brand, theme, msg, datetime.now()))
        self.conn.commit()
        return c.lastrowid

    def error(self, payload=dict()):
        domain = payload.get('domain')
        status = payload.get('status')

        c = self.conn.cursor()
        c.execute('INSERT INTO errors (domain, batch, status, date_rec) '
                  'VALUES (?,?, ?, ?)', (domain, self.batch, status, datetime.now()))
        self.conn.commit()
        return c.lastrowid

    def set_batch_num(self):
        c = self.conn.cursor()
        c.execute("SELECT batch FROM requests ORDER BY batch DESC LIMIT 1")
        result = c.fetchone()
        print(result)
        if result is None:
            return 0
        else:
            return result[0] + 1

    def build_header_columns(self):
        headers = config.RSP_HEADERS
        rtn = ''
        for head in headers:
            rtn += f"{head.split('-')[2]} TEXT NOT NULL,"
        return rtn
