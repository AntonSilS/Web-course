import os
import re
import time
import sqlite3

import create_db
import fill_data

def prepare_path(path):
    list_skr = [file for file in os.listdir(path) if file.split('.')[1] == 'sql']
    list_skr.sort(key=lambda x: int(re.match('^\d+', x).group()))
    list_path_skrs = [os.path.join(path, file_skr) for file_skr in list_skr]
    return list_path_skrs

def executer_skrips(list_path_skrs, path):
    with sqlite3.connect(path) as con:
        cur = con.cursor()
        n=0
        for skr_file in list_path_skrs:
            with open (skr_file, 'r') as sqls:
                text = sqls.readline()
                task_text = re.sub("[-|<|>]","", text).strip()
                sql = sqls.read()
                n = n+1
                time.sleep(1)
                print(f'\nЗавдання {n}: {task_text}\n')
                time.sleep(4)
                cur.execute(sql)
                res = cur.fetchall()
                print(res)

def main():
    db_name = 'univer_book_2.db'
    path_db = os.path.join(os.getcwd(), db_name)
    if not os.path.exists(path_db):
        create_db.crt_db(path_db)
        while True:
            try:
                fill_data.fill_db(path_db)
                break
            except sqlite3.IntegrityError:
                continue
    dir_skripts = os.path.join(os.getcwd(),'skripts')
    list_path_skrs = prepare_path(dir_skripts)
    executer_skrips(list_path_skrs, path_db)

if __name__ == "__main__":
    main()