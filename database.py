from os import environ as env
from typing import Any

from dotenv import load_dotenv
from mysql.connector import Error, connect

import data
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


def query(connection, sql, data=None, fetch=False, manyQuery=False, showQuery=False):
    cursor = connection.cursor(dictionary=True)

    if manyQuery:
        cursor.executemany(sql, data)
    else:
        cursor.execute(sql, data)

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
        query(connection=conn, sql=sql, data=data, showQuery=True)


def add_a_new_course(moniker, name, department):
    with get_connection() as conn:
        sql = "INSERT INTO courses (moniker, name, department) VALUES (%s, %s, %s);"
        data = (moniker, name, department)
        query(connection=conn, sql=sql, data=data, showQuery=True)


def add_a_prerequisite(course, prereq, min_grade):
    with get_connection() as conn:
        sql = (
            "INSERT INTO prerequisites (course, prereq, min_grade) VALUES (%s, %s, %s);"
        )
        data = (course, prereq, min_grade)
        query(connection=conn, sql=sql, data=data, showQuery=True)


def initialize_data():
    with get_connection() as conn:
        query(
            connection=conn,
            sql="INSERT INTO students (first_name, last_name, unix_id) VALUES (%s, %s, %s);",
            data=data.students,
            manyQuery=True,
        )
        query(
            connection=conn,
            sql="INSERT INTO courses (moniker, name, department) VALUES (%s, %s, %s);",
            data=data.courses,
            manyQuery=True,
        )
        query(
            connection=conn,
            sql="INSERT INTO prerequisites (course, prereq, min_grade) VALUES (%s, %s, %s);",
            data=data.prerequisites,
            manyQuery=True,
        )
        query(
            connection=conn,
            sql="INSERT INTO student_course (student, course, year,grade) VALUES (%s, %s, %s,%s);",
            data=data.student_course,
            manyQuery=True,
        )
        query(
            connection=conn,
            sql="INSERT INTO letter_grade (grade, letter) VALUES (%s, %s);",
            data=data.letter_grades,
            manyQuery=True,
        )


def show_prerequisites_for(course):
    with get_connection() as conn:
        sql = "SELECT prereq, min_grade FROM prerequisites WHERE course = %s"
        data = (course,)

        return query(connection=conn, sql=sql, data=data, fetch=True, showQuery=True)


def show_students_by(last_name):
    with get_connection() as conn:
        sql = "SELECT first_name, last_name, unix_id FROM students WHERE last_name like %s;"
        data = ("%" + last_name + "%",)

        return query(connection=conn, sql=sql, data=data, fetch=True, showQuery=True)


def show_courses_by(department):
    with get_connection() as conn:
        sql = "SELECT moniker, name, department FROM courses WHERE department = %s;"
        data = (department,)

        return query(connection=conn, sql=sql, data=data, fetch=True, showQuery=True)


def check_prerequisites(student, course):
    with get_connection() as conn:
        sql = """
                SELECT p.prereq,p.min_grade
                FROM prerequisites AS p
                WHERE p.course = %s
                AND p.prereq NOT in (
                    SELECT sc.course
                    FROM student_course AS sc
                    WHERE sc.student = %s
                        AND sc.grade > p.min_grade
                )
                -- LIMIT 1;
            """
        data = (course, student)

        return query(connection=conn, sql=sql, data=data, fetch=True, showQuery=True)


def enroll_student(student, course, year):
    with get_connection() as conn:
        sql = "INSERT INTO student_course (student, course, year) VALUES (%s, %s, %s);"
        data = (student, course, year)

        return query(connection=conn, sql=sql, data=data)


def set_grade(student, course, grade, year):
    with get_connection() as conn:
        sql = "UPDATE student_course SET grade = %s WHERE student = %s AND course = %s AND year = %s;"
        data = (grade, student, course, year)

        return query(connection=conn, sql=sql, data=data, showQuery=True)


def unenroll_student(student, course, year):
    with get_connection() as conn:
        sql = "DELETE FROM student_course WHERE student = %s AND course = %s AND year = %s;"
        data = (student, course, year)
        return query(connection=conn, sql=sql, data=data, showQuery=True)


def show_courses_a_student_is_currently_taking(student):
    with get_connection() as conn:
        sql = "SELECT course, year FROM student_course WHERE student = %s AND grade IS NULL;"
        data = (student,)

        return query(connection=conn, sql=sql, data=data, fetch=True, showQuery=True)


def get_transcript_for(student: str) -> list[Any] | None:
    with get_connection() as conn:
        sql = """
            SELECT course, year, grade, (select letter
                from letter_grade as lg
                where lg.grade <= sc.grade
                order by lg.grade desc limit 1
            ) as letter FROM student_course as sc WHERE student = %s AND grade IS NOT NULL ORDER BY year;
        """
        data = (student,)

        return query(connection=conn, sql=sql, data=data, fetch=True, showQuery=True)


def get_courses_with_most_enrolled_students(n):
    with get_connection() as conn:
        sql = """
            SELECT course, c.name, count(*) AS enrolled_students
            FROM student_course AS sc
            JOIN courses c on sc.course = c.moniker
            GROUP BY course
            ORDER BY enrolled_students DESC
            LIMIT %s
         """
        data = (n,)

        return query(connection=conn, sql=sql, data=data, fetch=True, showQuery=True)


def get_top_performing_students(n):
    with get_connection() as conn:
        sql = """
            SELECT student, s.first_name, s.last_name, count(*) as courses_taken, avg(grade) as average_grade
            FROM student_course AS sc
                JOIN students s on sc.student = s.unix_id
            WHERE grade IS NOT NULL
            GROUP BY student
            ORDER BY average_grade DESC
            LIMIT %s
        """
        data = (n,)

        return query(connection=conn, sql=sql, data=data, fetch=True, showQuery=True)
