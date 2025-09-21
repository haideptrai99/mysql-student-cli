from datetime import datetime

import typer
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from database import (
    add_a_new_course,
    add_a_prerequisite,
    add_a_student,
    enroll_student,
    initialize_data,
    reset,
    show_courses_by,
    show_prerequisites_for,
    show_students_by,
)

app = typer.Typer()
console = Console()


def pretty_table(with_headers, data, in_color):
    table = Table(*with_headers, show_header=True, header_style=f"bold {in_color}")

    for row in data:
        table.add_row(*map(str, row))

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
    pretty_table(
        ["Prerequisites", "Minimum Grade"],
        data=show_prerequisites_for(course),
        in_color="yellow",
    )


@app.command()
def show_students(last_name: str):
    data = show_students_by(last_name)

    pretty_table(["First Name", "Last Name", "UnixID"], data=data, in_color="blue")


@app.command()
def show_courses(department: str):
    data = show_courses_by(department)

    pretty_table(["Moniker", "Name", "Department"], data=data, in_color="green")


@app.command()
def enroll(student: str, course: str, year: int = datetime.now().year):
    enroll_student(student, course, year)


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
