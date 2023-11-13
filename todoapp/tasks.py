from invoke import task

@task
def start(ctx, campaign="testCampaign"):
    ctx.run("python src/game.py "+campaign)

@task
def test(ctx):
    ctx.run("pytest src")

@task
def coverage_report(ctx):
    ctx.run("coverage run --branch -m pytest src")
    ctx.run("coverage html")
    ctx.run("coverage report")

@task
def format(ctx):
    ctx.run("autopep8 --in-place --recursive src")