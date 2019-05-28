import mysql.connector as mysql

from core.config import DB_CONFIG



def get_db_connection():
    return mysql.connect(**DB_CONFIG)

def get_cursor():
    return get_db_connection().cursor(dictionary=True, buffered=True)
