import mysql.connector as mysql

db = mysql.connect(
    host="localhost",
    user="tray_system",
    passwd="tray_system",
)

DB_NAME = "tray_system"

UNSIGNED_INT = "integer unsigned not null"
ID = "id " + UNSIGNED_INT + " auto_increment primary key"
FOREIGN_KEY = "foreign key ({}) references {}(id)"

queries = [
    "create database {};".format(DB_NAME),
    "use {};".format(DB_NAME),
    "create table images ({}, path varchar(100) not null);".format(ID),

    "create table ingredients ({}, name varchar(100) not null);".format(ID),
    "create table menu_items ({}, name varchar(100) not null);".format(ID),
    "create table menu_item_ingredient (" +
        "menu_item_id {},".format(UNSIGNED_INT) +
        "ingredient_id {},".format(UNSIGNED_INT) +
        "primary key (menu_item_id, ingredient_id)," +
        FOREIGN_KEY.format("menu_item_id", "menu_items") + "," +
        FOREIGN_KEY.format("ingredient_id", "ingredients") + ");",

    "create table scans ({}, ".format(ID) +
        "menu_item_id {}, ".format(UNSIGNED_INT) +
        "image_id {}, ".format(UNSIGNED_INT) +
        "user_id integer unsigned default null, " +
        "time datetime default current_timestamp not null," +
        FOREIGN_KEY.format("menu_item_id", "menu_items") + "," +
        FOREIGN_KEY.format("image_id", "images") + ");",
    
    "create table detected_ingredients (" +
        "scan_id {},".format(UNSIGNED_INT) +
        "ingredient_id {},".format(UNSIGNED_INT) +
        "detection json," +
        FOREIGN_KEY.format("scan_id", "scans") + "," +
        FOREIGN_KEY.format("ingredient_id", "ingredients") + ");",
]

cursor = db.cursor()

for q in queries:
    try:
        print(q)
        cursor.execute(q)
    except mysql.Error as e:
        print(e)
3