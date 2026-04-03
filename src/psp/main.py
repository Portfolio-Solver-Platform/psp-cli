import typer
from psp.commands import auth, cfg, groups, instances, problems, projects, resources, solvers

app = typer.Typer()

app.add_typer(auth.app, name="auth")
app.add_typer(projects.app, name="projects")
app.add_typer(problems.app, name="problems")
app.add_typer(instances.app, name="instances")
app.add_typer(groups.app, name="groups")
app.add_typer(solvers.app, name="solvers")
app.add_typer(resources.app, name="resources")
app.add_typer(cfg.app, name="config")

if __name__ == "__main__":
    app()
