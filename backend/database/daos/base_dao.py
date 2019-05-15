from typing import List, Tuple, Dict

from manager import cursor, db

class BaseDao:
    def __init__(self, table_name: str, columns: List[str]):
        self.table_name:str = table_name
        self.columns = columns
        self.db = db
        self.cursor = cursor

    def comma_seperate(self, lst: List) -> str:
        return ",".join(lst)

    def list_to_in_param(self, lst: List) -> str:
        return "({})".format(",".join(lst))

    def insert(self, rows: List[Dict]) -> int:
        if rows is None:
            return -1

        cols = self.comma_seperate(list(rows[0].keys()))
        vals = [d.values() for d in rows]
        placeholders = ",".join(["%s" for ign in rows[0].keys()])
        sql = "insert into {} ({}) values ({})".format(self.table_name, cols, placeholders)
        print(sql)

        cursor.executemany(sql, vals)
        db.commit()
        return cursor.lastrowid

    def fetch_sql(self, sql: str) -> List[Dict]:
        cursor.execute(sql)
        return cursor.fetchall()

    def get(self, clause: str="", cols=None) -> List[Dict]:
        cols = self.columns if cols is None else cols
        cols = self.comma_seperate(cols)
        if clause is not "":
            clause = "where {}".format(clause)
        sql = "select {} from {} {}".format(cols, self.table_name, clause)
        print(sql)
        cursor.execute(sql)
        return cursor.fetchall()
