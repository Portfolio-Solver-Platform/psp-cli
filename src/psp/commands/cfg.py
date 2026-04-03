from typing import Annotated
import typer
import psp.config as config
import psp.output as output

app = typer.Typer()


@app.command("show")
def show(json_output: Annotated[bool, typer.Option("--json")] = False):
    cfg = config.load()
    if json_output:
        output.as_json(cfg)
    else:
        output.record(cfg, title="Configuration")


@app.command("set")
def set_value(key: str, value: str):
    cfg = config.load()
    if key not in cfg:
        typer.echo(f"Unknown key '{key}'. Valid keys: {', '.join(cfg.keys())}", err=True)
        raise typer.Exit(1)
    cfg[key] = value
    config.save(cfg)
    typer.echo(f"Set {key} = {value}")
