from typing import Annotated
import typer
import psp.client as client
import psp.output as output

app = typer.Typer()


@app.command("list")
def list_solvers(json_output: Annotated[bool, typer.Option("--json")] = False):
    data = client.get("/solvers").json()["solvers"]
    if json_output:
        output.as_json(data)
    else:
        output.table(data, ["id", "name", "image_name", "image_path"], title="Solvers")


@app.command()
def get(
    solver_id: int,
    json_output: Annotated[bool, typer.Option("--json")] = False,
):
    data = client.get(f"/solvers/{solver_id}").json()
    if json_output:
        output.as_json(data)
    else:
        output.record(data, title=f"Solver {solver_id}")


@app.command()
def register(
    image_name: str,
    image_url: str,
    names: Annotated[str, typer.Option(help="Comma-separated solver names, e.g. 'chuffed,gecode'")],
    json_output: Annotated[bool, typer.Option("--json")] = False,
):
    data = client.post("/solvers", data={"image_name": image_name, "image_url": image_url, "names": names}).json()
    if json_output:
        output.as_json(data)
    else:
        output.record(data, title="Solver Registered")


@app.command("update-image")
def update_image(
    image_name: str,
    image_url: str,
    json_output: Annotated[bool, typer.Option("--json")] = False,
):
    data = client.patch(f"/solvers/images/{image_name}", data={"image_url": image_url}).json()
    if json_output:
        output.as_json(data)
    else:
        output.record(data, title=f"Solver Image {image_name} Updated")
