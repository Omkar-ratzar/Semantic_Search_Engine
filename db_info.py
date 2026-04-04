import mysql.connector
from datetime import datetime
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="search_engine"
    )
