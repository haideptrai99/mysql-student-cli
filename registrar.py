import typer
from database import add_a_new_course, add_a_prerequisite, add_a_student, reset
from rich.console import Console

app = typer.Typer()
console = Console()


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
def reset_database():
    answer = input("This will delete all the data. Are you sure? (y/n): ")

    if answer.strip().lower() == "y":
        reset()
        typer.echo("Database reset successfully.")
    else:
        typer.echo("Database reset aborted.")


def run():
    try:
        app()
    except Exception as e:
        # Xử lý lỗi toàn cục
        console.print(f"[bold red]❌ Lỗi:[/bold red] {e}")
        # raise typer.Exit(code=1)  # Thoát CLI


if __name__ == "__main__":
    run()
