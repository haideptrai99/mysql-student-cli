from os import environ as env

from dotenv import load_dotenv
from mysql.connector import Error, connect
from mysql_highlight import print_query

load_dotenv()


def get_connection():
    # Nếu lỗi kết nối → raise luôn để không trả về None cho khối with
    try:
        cnx = connect(
            user=env.get("MYSQL_USER"),
            password=env.get("MYSQL_PASSWORD"),
            host=env.get("MYSQL_HOST", "127.0.0.1"),
            port=int(env.get("MYSQL_PORT", "3306")),
            database=env.get("MYSQL_DATABASE"),
        )
        # cnx.ping(reconnect=True, attempts=1, delay=0)
        return cnx
    except Error as e:
        raise RuntimeError(f"DB connect failed: {e}") from e


def query(connection, q, data=None, fetch=None, showQuery=True):
    cursor = connection.cursor()

    cursor.execute(q, data)
    if showQuery:
        print_query(cursor.statement)

    if fetch:
        return cursor.fetchall()
    else:
        connection.commit()

    cursor.close()


def reset(sql_path: str = "ddl.sql") -> None:
    cnx = get_connection()  # có thể raise nếu kết nối lỗi
    try:
        # Dùng 1 with cho nhiều context (cursor + file)
        with cnx.cursor() as cursor, open(sql_path, encoding="utf-8") as f:
            sql = f.read()
            # 9.2+ cho phép execute nhiều statements trong 1 lần gọi
            cursor.execute(sql)

            # KHÔNG lặp trên giá trị trả về của execute (vì nó không phải iterator)
            # Thay vào đó, duyệt các result-set bằng fetchsets()/nextset()
            for _, _ in cursor.fetchsets():
                pass

        cnx.commit()
    finally:
        cnx.close()


def reset_cu(sql_path: str = "ddl.sql") -> None:
    cnx = get_connection()
    with cnx.cursor() as cursor, open(sql_path, encoding="utf-8") as f:
        sql = f.read()
        cursor.execute(sql)


def add_a_student(first_name, last_name, unix_id):
    with get_connection() as conn:
        sql = (
            "INSERT INTO students (first_name, last_name, unix_id) VALUES (%s, %s, %s);"
        )
        data = (first_name, last_name, unix_id)
        query(conn, sql, data)


def add_a_new_course(moniker, name, department):
    with get_connection() as conn:
        sql = "INSERT INTO courses (moniker, name, department) VALUES (%s, %s, %s);"
        data = (moniker, name, department)
        query(conn, sql, data)


def add_a_prerequisite(course, prereq, min_grade):
    with get_connection() as conn:
        sql = (
            "INSERT INTO prerequisites (course, prereq, min_grade) VALUES (%s, %s, %s);"
        )
        data = (course, prereq, min_grade)
        query(conn, sql, data)
