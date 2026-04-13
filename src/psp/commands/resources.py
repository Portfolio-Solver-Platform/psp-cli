from typing import Annotated, Optional
import typer
import psp.client as client
import psp.output as output

app = typer.Typer()
defaults_app = typer.Typer()
users_app = typer.Typer()
app.add_typer(defaults_app, name="defaults")
app.add_typer(users_app, name="users")


@defaults_app.command("get")
def get_defaults(json_output: Annotated[bool, typer.Option("--json")] = False):
    data = client.get("/resources/defaults").json()
    if json_output:
        output.as_json(data)
    else:
        output.record(data, title="Resource Defaults")


@defaults_app.command("set")
def set_defaults(
    per_user_cpu: Annotated[Optional[float], typer.Option()] = None,
    per_user_memory: Annotated[Optional[float], typer.Option()] = None,
    global_max_cpu: Annotated[Optional[float], typer.Option()] = None,
    global_max_memory: Annotated[Optional[float], typer.Option()] = None,
    json_output: Annotated[bool, typer.Option("--json")] = False,
):
    current = client.get("/resources/defaults").json()
    data = client.put("/resources/defaults", json={
        "per_user_cpu_cores": per_user_cpu if per_user_cpu is not None else current["per_user_cpu_cores"],
        "per_user_memory_gib": per_user_memory if per_user_memory is not None else current["per_user_memory_gib"],
        "global_max_cpu_cores": global_max_cpu if global_max_cpu is not None else current["global_max_cpu_cores"],
        "global_max_memory_gib": global_max_memory if global_max_memory is not None else current["global_max_memory_gib"],
    }).json()
    if json_output:
        output.as_json(data)
    else:
        output.record(data, title="Resource Defaults Updated")


@users_app.command("get")
def get_user(
    user_id: str,
    json_output: Annotated[bool, typer.Option("--json")] = False,
):
    data = client.get(f"/resources/users/{user_id}").json()
    if json_output:
        output.as_json(data)
    else:
        output.record(data, title=f"Resources: {user_id}")


@users_app.command("set")
def set_user(
    user_id: str,
    vcpus: Annotated[int, typer.Option()],
    memory: Annotated[float, typer.Option()],
    json_output: Annotated[bool, typer.Option("--json")] = False,
):
    data = client.put(f"/resources/users/{user_id}", json={"vcpus": vcpus, "memory_gib": memory}).json()
    if json_output:
        output.as_json(data)
    else:
        output.record(data, title=f"Resources Updated: {user_id}")


@users_app.command("delete")
def delete_user(
    user_id: str,
    yes: Annotated[bool, typer.Option("--yes", "-y")] = False,
):
    if not yes:
        typer.confirm(f"Remove resource override for {user_id}?", abort=True)
    client.delete(f"/resources/users/{user_id}")
    typer.echo("Deleted.")
