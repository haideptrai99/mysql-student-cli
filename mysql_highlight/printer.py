import re

from rich.console import Console

console = Console()

# Map keyword -> style (update SELECT, FROM, WHERE đậm hơn)
SQL_STYLES = {
    # DML
    "SELECT": "bold bright_blue",
    "INSERT": "bold #E48E00",
    "UPDATE": "bold yellow",
    "DELETE": "bold red",
    # DDL
    "CREATE": "bold green",
    "ALTER": "bold magenta",
    "DROP": "bold red",
    "TRUNCATE": "bold red",
    # Keywords khác
    "FROM": "bold bright_blue",
    "WHERE": "bold bright_blue",
    "AND": "bold cyan",
    "OR": "bold cyan",
    "JOIN": "bold #00BFFF",
    "INNER": "bold #00BFFF",
    "LEFT": "bold #00BFFF",
    "RIGHT": "bold #00BFFF",
    "ON": "bold bright_blue",
    "VALUES": "bold #E48E00",
    "INTO": "bold #E48E00",
    "SET": "bold yellow",
    "AS": "italic",
    "ORDER": "bold cyan",
    "BY": "bold cyan",
    "GROUP": "bold cyan",
    "LIMIT": "bold magenta",
    "TABLE": "bold green",
}

# Style riêng
TABLE_STYLE = "bold underline #00BFFF"
COLUMN_STYLE = "#E48E00"
FUNC_STYLE = "bold #800080"  # tím đậm cho function


def print_query(query: str) -> None:
    """In MySQL query với highlight keyword + bảng + cột + function."""
    tokens = re.split(r"(\s+|,|\(|\))", query)  # giữ lại dấu , ( )

    styled_tokens = []
    prev_token = ""
    in_column_list = False

    for token in tokens:
        upper_token = token.upper()

        # --- Highlight keyword ---
        if upper_token in SQL_STYLES:
            styled_tokens.append(f"[{SQL_STYLES[upper_token]}]{token}[/]")

            # Sau các keyword này → bảng
            if upper_token in {"FROM", "JOIN", "INTO", "UPDATE", "TABLE"}:
                prev_token = "EXPECT_TABLE"
            # Sau SELECT hoặc UPDATE SET → column list
            elif upper_token in {"SELECT", "SET"}:
                in_column_list = True
            else:
                in_column_list = False

        # --- Highlight bảng ---
        elif prev_token == "EXPECT_TABLE" and token.strip():
            styled_tokens.append(f"[{TABLE_STYLE}]{token}[/]")
            prev_token = ""

        # --- Highlight function (NOW, COUNT, SUM, ...) ---
        elif re.match(r"^[A-Z_][A-Z0-9_]*$", upper_token) and token.isalpha():
            # Nếu là function MySQL phổ biến
            if upper_token in {
                "NOW",
                "COUNT",
                "AVG",
                "MIN",
                "MAX",
                "SUM",
                "LENGTH",
                "UPPER",
                "LOWER",
                "SUBSTRING",
                "ROUND",
            }:
                styled_tokens.append(f"[{FUNC_STYLE}]{token}[/]")
            else:
                styled_tokens.append(token)

        # --- Highlight cột ---
        elif in_column_list and token.strip() not in {"", ",", "(", ")"}:
            styled_tokens.append(f"[{COLUMN_STYLE}]{token}[/]")

        else:
            styled_tokens.append(token)

    console.print("".join(styled_tokens))
