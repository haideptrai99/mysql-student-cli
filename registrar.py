from datetime import datetime

import typer
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from database import (
    add_a_new_course,
    add_a_prerequisite,
    add_a_student,
    check_prerequisites,
    enroll_student,
    get_courses_with_most_enrolled_students,
    get_top_performing_students,
    get_transcript_for,
    initialize_data,
    reset,
    set_grade,
    show_courses_a_student_is_currently_taking,
    show_courses_by,
    show_prerequisites_for,
    show_students_by,
    unenroll_student,
)

app = typer.Typer()
console = Console()


def pretty_table_old(with_headers, data, in_color):
    table = Table(*with_headers, show_header=True, header_style=f"bold {in_color}")

    for row in data:
        table.add_row(*map(str, row))

    console.print(table)


def pretty_table_new1(with_headers, data, in_color):
    """
    Hiển thị dữ liệu dạng bảng một cách đẹp mắt bằng thư viện Rich.

    Hàm này được thiết kế để làm việc với dữ liệu từ mysql-connector-python
    khi curseor được khởi tạo với dictionary=True.

    Args:
        headers (List[str]): Một danh sách các chuỗi tương ứng với tiêu đề cột.
                             Thứ tự của các tiêu đề này sẽ quyết định thứ tự
                             các cột trong bảng.
        data (List[Dict[str, Any]]): Dữ liệu cần hiển thị, là một danh sách
                                     các dictionary. Mỗi dictionary đại diện
                                     cho một hàng.
        color (str): Màu sắc cho phần header của bảng (ví dụ: "magenta", "cyan").
    """
    if not data:
        console.print("[bold red]Không có dữ liệu để hiển thị.[/bold red]")
        return

    # Tạo bảng với các header được cung cấp
    table = Table(*with_headers, show_header=True, header_style=f"bold {in_color}")

    # Lặp qua mỗi hàng (là một dictionary) trong dữ liệu
    for row_dict in data:
        print(row_dict)
        # Xây dựng một danh sách các giá trị từ dictionary
        # theo đúng thứ tự của `headers`
        # Điều này đảm bảo các giá trị được đưa vào đúng cột
        row_values = [str(row_dict.get(header, "")) for header in with_headers]
        table.add_row(*row_values)

    # In bảng ra console
    console.print(table)


def pretty_table(header_map, data, in_color):
    """
    Hiển thị dữ liệu dạng bảng với header tùy chỉnh, không phụ thuộc vào tên cột.

    Hàm này cho phép bạn định nghĩa một ánh xạ giữa tên cột trong dữ liệu
    và header sẽ được hiển thị ra màn hình.

    Args:
        header_map (Dict[str, str]): Dictionary ánh xạ.
                                     - key: Tên cột trong dữ liệu (VD: 'letter_grade').
                                     - value: Header muốn hiển thị (VD: 'Điểm Chữ').
                                     Thứ tự các cột sẽ dựa trên thứ tự của dictionary này.
        data (List[Dict[str, Any]]): Dữ liệu từ database (list of dictionaries).
        color (str): Màu sắc cho phần header của bảng.
    """
    if not data:
        console.print("[bold red]Không có dữ liệu để hiển thị.[/bold red]")
        return

    # Lấy danh sách các key của dữ liệu gốc (tên cột SQL)
    data_keys = list(header_map.keys())

    # Lấy danh sách các header tùy chỉnh để hiển thị
    display_headers = list(header_map.values())

    # Tạo bảng với các header tùy chỉnh
    table = Table(*display_headers, show_header=True, header_style=f"bold {in_color}")

    # Lặp qua mỗi hàng (là một dictionary) trong dữ liệu
    for row_dict in data:
        # Xây dựng một danh sách các giá trị bằng cách lặp qua các `data_keys`
        # để lấy giá trị từ `row_dict` theo đúng thứ tự.
        row_values = [str(row_dict.get(key, "")) for key in data_keys]
        table.add_row(*row_values)

    # In bảng ra console
    console.print(table)


@app.command()
def add_student(first_name: str, last_name: str, unix_id: str):
    add_a_student(first_name, last_name, unix_id)
    console.print("Adding a student successfull")


@app.command()
def add_course(moniker: str, name: str, department: str):
    add_a_new_course(moniker, name, department)
    console.print("Adding a course successfull")


@app.command()
def add_prereq(course: str, prereq: str, min_grade: int = 50):
    # python registrar.py add-prereq cs102 cs101 --min-grade 70
    add_a_prerequisite(course, prereq, min_grade)


@app.command()
def show_prereqs(course: str):
    custom_headers = {"prereq": "Minimum Grade", "min_grade": "Minimum Grade"}
    pretty_table(
        custom_headers,
        data=show_prerequisites_for(course),
        in_color="yellow",
    )


@app.command()
def show_students(last_name: str):
    data = show_students_by(last_name)
    custom_headers = {
        "first_name": "First Name",
        "last_name": "Last Name",
        "unix_id": "UnixID",
    }
    pretty_table(custom_headers, data=data, in_color="blue")


@app.command()
def show_courses(department: str):
    data = show_courses_by(department)
    custom_headers = {
        "moniker": "Moniker",
        "name": "Name",
        "department": "Department",
    }
    pretty_table(custom_headers, data=data, in_color="green")


@app.command()
def enroll(student: str, course: str, year: int = datetime.now().year):
    data = check_prerequisites(student, course)
    if data:
        console.print(data)
        detail = f"Student {student} cannot take course {course}. Prerequisite not met: {data}"
        console.print(detail)
    else:
        enroll_student(student, course, year)
        console.print("Add student to course successfull")


@app.command()
def grade(student: str, course: str, grade: int, year: int = datetime.now().year):
    set_grade(student, course, grade, year)


@app.command()
def unenroll(student: str, course: str, year: int = datetime.now().year):
    unenroll_student(student, course, year)


@app.command()
def current_courses(student: str):
    data = show_courses_a_student_is_currently_taking(student)
    custom_headers = {
        "course": "Course",
        "year": "Year",
    }
    pretty_table(custom_headers, data=data, in_color="green")


@app.command()
def transcript(student: str):
    data = get_transcript_for(student)
    custom_headers = {
        "course": "Course",
        "year": "Year",
        "grade": "Grade",
        "letter": "Letter Grade",
    }
    pretty_table(custom_headers, data=data, in_color="magenta")
    if data:
        total_score = 0
        for row_data in data:
            # row_data = typing.cast(dict, row_data)
            total_score += int(row_data["grade"])
        console.print(f"Average GPA: {total_score / len(data):.2f}", style="bold")


@app.command()
def most_enrolled(n: int = 10):
    # --n=3

    data = get_courses_with_most_enrolled_students(n)
    custom_headers = {
        "course": "Course",
        "name": "Name",
        "enrolled_students": "Enrollment",
    }
    pretty_table(custom_headers, data=data, in_color="blue")


@app.command()
def top_students(n: int = 10):
    data = get_top_performing_students(n)
    custom_headers = {
        "student": "UnixId",
        "first_name": "First Name",
        "last_name": "Last Name",
        "courses_taken": "Courses",
        "average_grade": "Cum. GPA",
    }
    pretty_table(
        custom_headers,
        data=data,
        in_color="green",
    )


@app.command()
def reset_database(with_data: bool = True):
    # --with-data
    # --no-with-data

    answer = input("This will delete all the data. Are you sure? (y/n): ")

    if answer.strip().lower() == "y":
        reset()
        typer.echo("Database reset successfully.")

        if with_data:
            initialize_data()
            typer.echo("Data initialized successfully.")
    else:
        typer.echo("Database reset aborted.")


@app.command()
def reset_database_new() -> None:
    """
    Reset lại database với menu có màu sắc.
    Người dùng chọn:
    1 = Reset data
    2 = Reset + Insert data
    3 = Cancel
    """

    while True:
        console.print("\n[bold white]Please choose your input:[/bold white]")
        console.print("[green]1.[/green] Reset data")
        console.print("[yellow]2.[/yellow] Reset and insert data")
        console.print("[red]3.[/red] Cancel")

        choice = Prompt.ask("Enter your choice (1-3)", choices=["1", "2", "3"])

        if choice == "1":
            reset()
            console.print("[bold green]Database reset successfully.[/bold green]")
            break

        elif choice == "2":
            reset()
            console.print("[bold green]Database reset successfully.[/bold green]")
            initialize_data()
            console.print("[bold cyan]Data initialized successfully.[/bold cyan]")
            break

        elif choice == "3":
            console.print("[bold red]Database reset aborted.[/bold red]")
            break


def run():
    try:
        app()
    except Exception as e:
        # Xử lý lỗi toàn cục
        console.print(f"[bold red]❌ Lỗi:[/bold red] {e}")
        # raise typer.Exit(code=1)  # Thoát CLI


if __name__ == "__main__":
    run()
