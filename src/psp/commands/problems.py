import re
from pathlib import Path
from typing import Annotated, Optional
import typer
import psp.client as client
import psp.output as output

app = typer.Typer()


@app.command("list")
def list_problems(
    group: Annotated[Optional[int], typer.Option("--group", "-g")] = None,
    json_output: Annotated[bool, typer.Option("--json")] = False,
):
    params = {"group_id": group} if group is not None else {}
    data = client.get("/problems", params=params).json()
    if json_output:
        output.as_json(data)
    else:
        output.table(data, ["id", "name", "filename", "file_size", "uploaded_at"], title="Problems")


@app.command()
def create(
    name: str,
    group: Annotated[list[int], typer.Option("--group", "-g")],
    json_output: Annotated[bool, typer.Option("--json")] = False,
):
    data = client.post("/problems", json={"name": name, "group_ids": group}).json()
    if json_output:
        output.as_json(data)
    else:
        output.record(data, title="Problem Created")


@app.command()
def get(
    problem_id: int,
    json_output: Annotated[bool, typer.Option("--json")] = False,
):
    data = client.get(f"/problems/{problem_id}").json()
    if json_output:
        output.as_json(data)
    else:
        output.record(data, title=f"Problem {problem_id}")


@app.command()
def update(
    problem_id: int,
    name: Annotated[Optional[str], typer.Option()] = None,
    group: Annotated[Optional[list[int]], typer.Option("--group", "-g")] = None,
    json_output: Annotated[bool, typer.Option("--json")] = False,
):
    body = {}
    if name is not None:
        body["name"] = name
    if group is not None:
        body["group_ids"] = group
    data = client.patch(f"/problems/{problem_id}", json=body).json()
    if json_output:
        output.as_json(data)
    else:
        output.record(data, title=f"Problem {problem_id} Updated")


@app.command("upload-file")
def upload_file(
    problem_id: int,
    file: Annotated[Path, typer.Argument()],
):
    with open(file, "rb") as f:
        client.put(f"/problems/{problem_id}/file", files={"file": f})
    typer.echo(f"Uploaded {file.name} to problem {problem_id}.")


@app.command("download-file")
def download_file(
    problem_id: int,
    output_file: Annotated[Optional[Path], typer.Option("--output", "-o")] = None,
):
    r = client.get(f"/problems/{problem_id}/file")
    if output_file is None:
        cd = r.headers.get("content-disposition", "")
        match = re.search(r'filename="?([^";\r\n]+)"?', cd)
        output_file = Path(match.group(1)) if match else Path(f"problem_{problem_id}.mzn")
    output_file.write_bytes(r.content)
    typer.echo(f"Saved to {output_file}")


@app.command()
def delete(
    problem_id: int,
    yes: Annotated[bool, typer.Option("--yes", "-y")] = False,
):
    if not yes:
        typer.confirm(f"Delete problem {problem_id} and all its instances?", abort=True)
    client.delete(f"/problems/{problem_id}")
    typer.echo("Deleted.")
