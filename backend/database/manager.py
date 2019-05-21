import mysql.connector as mysql

from core.config import DB_CONFIG

db = mysql.connect(**DB_CONFIG)

cursor = db.cursor(dictionary=True)
