from sqlite3 import Cursor
import psycopg2
def connect():
    conn = psycopg2.connect(
        database="postgres", user='postgres', password='123456', host='localhost', port= '5432'
    )
    return conn


conn=connect()
cursor=conn.cursor()
# cursor.execute('''select * from image_table''')
# for row in cursor.fetchall():
#     print(row)