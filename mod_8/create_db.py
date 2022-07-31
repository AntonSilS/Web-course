import os
import sqlite3
import time

def crt_db(path):
    with open ("create_table.sql", "r") as f:
        sql = f.read()

    with sqlite3.connect(path) as con:
        cur = con.cursor()
        cur.executescript(sql)
        print(f'\nDatebase: {os.path.split(path)[1]} was succesfully created\n')
        time.sleep(2)
        #return con
