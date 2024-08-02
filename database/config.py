import pymysql

CONNECTION = {
    "host": "localhost",
    "user": "root",
    "password": "1520528a",
    "database": "lotto",
    "charset":"utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor  # json 형식으로 데이터가 전달되는 경우가 많다
}