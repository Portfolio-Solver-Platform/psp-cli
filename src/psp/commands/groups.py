from typing import Annotated, Optional
import typer
import psp.client as client
import psp.output as output

app = typer.Typer()


@app.command("list")
def list_groups(json_output: Annotated[bool, typer.Option("--json")] = False):
    data = client.get("/groups").json()
    if json_output:
        output.as_json(data)
    else:
        output.table(data, ["id", "name", "description", "solver_ids"], title="Groups")


@app.command()
def create(
    name: str,
    description: Annotated[Optional[str], typer.Option()] = None,
    json_output: Annotated[bool, typer.Option("--json")] = False,
):
    body = {"name": name}
    if description:
        body["description"] = description
    data = client.post("/groups", json=body).json()
    if json_output:
        output.as_json(data)
    else:
        output.record(data, title="Group Created")


@app.command()
def get(
    group_id: int,
    json_output: Annotated[bool, typer.Option("--json")] = False,
):
    data = client.get(f"/groups/{group_id}").json()
    if json_output:
        output.as_json(data)
    else:
        output.record(data, title=f"Group {group_id}")


@app.command()
def update(
    group_id: int,
    name: Annotated[Optional[str], typer.Option()] = None,
    description: Annotated[Optional[str], typer.Option()] = None,
    solver: Annotated[Optional[list[int]], typer.Option("--solver", "-s")] = None,
    json_output: Annotated[bool, typer.Option("--json")] = False,
):
    body = {}
    if name is not None:
        body["name"] = name
    if description is not None:
        body["description"] = description
    if solver is not None:
        body["solver_ids"] = solver
    data = client.patch(f"/groups/{group_id}", json=body).json()
    if json_output:
        output.as_json(data)
    else:
        output.record(data, title=f"Group {group_id} Updated")


@app.command()
def delete(
    group_id: int,
    yes: Annotated[bool, typer.Option("--yes", "-y")] = False,
):
    if not yes:
        typer.confirm(f"Delete group {group_id}?", abort=True)
    client.delete(f"/groups/{group_id}")
    typer.echo("Deleted.")
