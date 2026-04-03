import json
import typer
from rich.console import Console
from rich.table import Table

console = Console()


def as_json(data) -> None:
    typer.echo(json.dumps(data, indent=2, default=str))


def table(rows: list[dict], columns: list[str], title: str | None = None) -> None:
    t = Table(title=title, show_header=True, header_style="bold")
    for col in columns:
        t.add_column(col)
    for row in rows:
        t.add_row(*[str(row.get(col, "")) for col in columns])
    console.print(t)


def record(data: dict, title: str | None = None) -> None:
    t = Table(title=title, show_header=False)
    t.add_column("Field", style="bold")
    t.add_column("Value")
    for k, v in data.items():
        t.add_row(k, str(v) if not isinstance(v, (dict, list)) else json.dumps(v, default=str))
    console.print(t)
