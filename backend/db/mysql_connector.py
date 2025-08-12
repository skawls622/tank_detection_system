# backend/db/mysql_connector.py
import pymysql

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='acorn1234',
        db='daenamjin',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
