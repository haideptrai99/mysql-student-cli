import questionary
import typer
from rich.console import Console

app = typer.Typer()
console = Console()


def reset() -> None:
    console.print("[yellow]⚠️ Resetting database...[/yellow]")


def initialize_data() -> None:
    console.print("[cyan]✨ Inserting sample data...[/cyan]")


@app.command()
def reset_database() -> None:
    """
    Reset database:
    - Chọn bằng arrow (↑ ↓ + Enter).
    - Sau đó confirm Yes/No.
    - Nếu No thì quay lại menu ban đầu.
    """

    options = [
        "1. ⚠️ Reset data",
        "2. ✨ Reset and insert data",
        "3. ❌ Cancel",
    ]

    while True:
        # --- Menu arrow ---
        choice = questionary.select(
            "👉 Please choose your input:",
            choices=options,
            qmark="➡️",
            pointer="👉",
        ).ask()

        # Nếu user thoát (ESC hoặc Ctrl+C)
        if choice is None:
            console.print("[bold red]❌ Database reset aborted.[/bold red]")
            return

        # --- Confirm Yes/No ---
        confirm = questionary.confirm(
            f"Are you sure you want to execute: {choice} ?",
            default=False,
        ).ask()

        if not confirm:
            console.print("[cyan]↩ Returning to menu...[/cyan]")
            continue  # quay lại menu

        # --- Xử lý khi Yes ---
        if choice.startswith("1"):
            reset()
            console.print("[bold green]✅ Database reset successfully.[/bold green]")
            break

        elif choice.startswith("2"):
            reset()
            console.print("[bold green]✅ Database reset successfully.[/bold green]")
            initialize_data()
            console.print("[bold cyan]✨ Data initialized successfully.[/bold cyan]")
            break

        elif choice.startswith("3"):
            console.print("[bold red]❌ Database reset aborted.[/bold red]")
            break


if __name__ == "__main__":
    app()
