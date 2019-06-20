from typing import List, Dict

import mysql.connector as mysql
from core.config import DB_CONFIG
# from backend.database.manager import db, get_cursor


class BaseDao:
    def __init__(self, table_name: str, columns: List[str]):
        self.table_name: str = table_name
        self.columns = columns
        # self.db = mysql.connect(**DB_CONFIG)

    def get_cursor(self):
        db = mysql.connect(**DB_CONFIG)
        return db, db.cursor(dictionary=True, buffered=True)

    def comma_seperate(self, lst: List) -> str:
        return ",".join(lst)

    def list_to_in_param(self, lst: List) -> str:
        return "({})".format(",".join([str(l) for l in lst]))

    def insert(self, rows: List[Dict]) -> int:
        if rows is None:
            return -1

        cols = self.comma_seperate(list(rows[0].keys()))
        vals = [d.values() for d in rows]
        placeholders = ",".join(["%s" for ign in rows[0].keys()])
        sql = "insert into {} ({}) values ({})".format(self.table_name, cols, placeholders)
        print(sql)

        db, cursor = self.get_cursor()
        cursor.executemany(sql, vals)
        db.commit()
        id = cursor.lastrowid
        cursor.close()
        # db.cursor.close()
        return id

    def fetch_sql(self, sql: str) -> List[Dict]:
        _, cursor = self.get_cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results

    def get(self, clause: str="", cols=None) -> List[Dict]:
        cols = self.columns if cols is None else cols
        cols = self.comma_seperate(cols)
        if clause is not "":
            clause = "where {}".format(clause)
        sql = "select {} from {} {}".format(cols, self.table_name, clause)
        return self.fetch_sql(sql)
