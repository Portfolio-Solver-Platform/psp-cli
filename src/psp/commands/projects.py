import json
from pathlib import Path
from typing import Annotated, Optional
import typer
import psp.client as client
import psp.output as output

app = typer.Typer()


@app.command("list")
def list_projects(json_output: Annotated[bool, typer.Option("--json")] = False):
    data = client.get("/projects").json()
    if json_output:
        output.as_json(data)
    else:
        output.table(data, ["id", "name", "created_at", "is_queued"], title="Projects")


@app.command()
def create(
    config_file: Annotated[Path, typer.Argument(help="JSON file with project configuration")],
    json_output: Annotated[bool, typer.Option("--json")] = False,
):
    data = client.post("/projects", json=json.loads(config_file.read_text())).json()
    if json_output:
        output.as_json(data)
    else:
        output.record(data, title="Project Created")


@app.command()
def status(
    project_id: str,
    json_output: Annotated[bool, typer.Option("--json")] = False,
):
    data = client.get(f"/projects/{project_id}/status").json()
    if json_output:
        output.as_json(data)
    else:
        output.record(data, title=f"Project {project_id[:8]}… Status")


@app.command()
def config_get(
    project_id: str,
    json_output: Annotated[bool, typer.Option("--json")] = False,
):
    data = client.get(f"/projects/{project_id}/config").json()
    if json_output:
        output.as_json(data)
    else:
        output.record(data, title=f"Project {project_id[:8]}… Config")


@app.command()
def results(
    project_id: str,
    output_file: Annotated[Optional[Path], typer.Option("--output", "-o")] = None,
):
    r = client.get(f"/projects/{project_id}/solution", stream=True)
    if output_file:
        with open(output_file, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        typer.echo(f"Saved to {output_file}")
    else:
        for line in r.iter_lines():
            typer.echo(line.decode())


@app.command()
def delete(
    project_id: str,
    yes: Annotated[bool, typer.Option("--yes", "-y")] = False,
):
    if not yes:
        typer.confirm(f"Delete project {project_id}?", abort=True)
    client.delete(f"/projects/{project_id}")
    typer.echo("Deleted.")
