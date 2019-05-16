from typing import List, Dict, Tuple

import numpy as np
import cv2 as cv

from backend.database.manager import mysql, db
from backend.detection.detector import Detector
from core.scan_request import ScanRequest

DB_NAME = "tray_system"

UNSIGNED_INT = "integer unsigned not null"
ID = "id " + UNSIGNED_INT + " auto_increment primary key"
PRIMARY_KEY = "primary key ({})"
FOREIGN_KEY = "foreign key ({}) references {}(id)"

QUERIES = [
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
        "detections json," +
        PRIMARY_KEY.format(",".join(["scan_id", "ingredient_id"])) + "," +
        FOREIGN_KEY.format("scan_id", "scans") + "," +
        FOREIGN_KEY.format("ingredient_id", "ingredients") + ");"
]


def create_db_and_tables():
    cursor = db.cursor()
    for q in QUERIES:
        try:
            print(q)
            cursor.execute(q)
        except mysql.Error as e:
            print(e)


def create_menu_items():
    # Note this is run as main so can't use relative imports
    from backend.database.daos.ingredients_dao import IngredientsDao
    from backend.database.daos.menu_items_dao import MenuItemsDao
    from core.dao_models.menu_item import MenuItem
    from core.dao_models.ingredient import Ingredient

    id = IngredientsDao()
    print(id.get_ingredients())

    mid = MenuItemsDao()

    menu_item1 = MenuItem("Chicken Pasta", [Ingredient(i) for i in ["Chicken", "Pasta"]])
    menu_item2 = MenuItem("Tofu Pasta", [Ingredient(i) for i in ["Tofu", "Pasta"]])
    mid.insert_menu_items([menu_item1, menu_item2])

    menu_items: List[MenuItem] = mid.get_menu_items(names=["Chicken Pasta", "Pasta"])


def create_scan():
    img: np.ndarray = cv.imread("../../test.jpg")
    depth_map = np.random.rand(img.shape[0], img.shape[1])
    detector = Detector()
    scan_req = ScanRequest(img, depth_map, 2, 1)

    from tray_system.data_pusher import DataPusher
    dp = DataPusher()
    dp.push_scan(scan_req)
    # detector.handle_scan(scan_req)


if __name__ == "__main__":
    # create_db_and_tables()
    # create_menu_items()
    create_scan()

