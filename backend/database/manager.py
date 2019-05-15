import mysql.connector as mysql

db = mysql.connect(
    host="localhost",
    user="tray_system",
    passwd="tray_system",
    database="tray_system"
)

cursor = db.cursor(dictionary=True)
