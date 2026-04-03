import re
from pathlib import Path
from typing import Annotated, Optional
import typer
import psp.client as client
import psp.output as output

app = typer.Typer()


@app.command("list")
def list_instances(
    problem_id: int,
    json_output: Annotated[bool, typer.Option("--json")] = False,
):
    data = client.get(f"/problems/{problem_id}/instances").json()
    if json_output:
        output.as_json(data)
    else:
        output.table(data, ["id", "filename", "file_size", "uploaded_at"], title=f"Instances of Problem {problem_id}")


@app.command()
def upload(
    problem_id: int,
    file: Annotated[Path, typer.Argument()],
    json_output: Annotated[bool, typer.Option("--json")] = False,
):
    with open(file, "rb") as f:
        data = client.post(f"/problems/{problem_id}/instances", files={"file": f}).json()
    if json_output:
        output.as_json(data)
    else:
        output.record(data, title="Instance Uploaded")


@app.command()
def get(
    problem_id: int,
    instance_id: int,
    json_output: Annotated[bool, typer.Option("--json")] = False,
):
    data = client.get(f"/problems/{problem_id}/instances/{instance_id}").json()
    if json_output:
        output.as_json(data)
    else:
        output.record(data, title=f"Instance {instance_id}")


@app.command()
def download(
    problem_id: int,
    instance_id: int,
    output_file: Annotated[Optional[Path], typer.Option("--output", "-o")] = None,
):
    r = client.get(f"/problems/{problem_id}/instances/{instance_id}/file")
    if output_file is None:
        cd = r.headers.get("content-disposition", "")
        match = re.search(r'filename="?([^";\r\n]+)"?', cd)
        output_file = Path(match.group(1)) if match else Path(f"instance_{instance_id}.dzn")
    output_file.write_bytes(r.content)
    typer.echo(f"Saved to {output_file}")


@app.command()
def delete(
    problem_id: int,
    instance_id: int,
    yes: Annotated[bool, typer.Option("--yes", "-y")] = False,
):
    if not yes:
        typer.confirm(f"Delete instance {instance_id} from problem {problem_id}?", abort=True)
    client.delete(f"/problems/{problem_id}/instances/{instance_id}")
    typer.echo("Deleted.")
