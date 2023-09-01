"Noxfile"
import nox

REQUIREMENTS = "requirements.txt"


@nox.session
def pytest(session):
    "pytest"
    session.install("-r", REQUIREMENTS)
    session.run("pytest", ".")


@nox.session
def lint(session):
    "pylint"
    session.install("-r", REQUIREMENTS)
    session.install("pylint")
    session.run("pylint", "--recursive=y", "pat_rotate.py", "azure_app_auth", "tests")


@nox.session
def flake8(session):
    "flake8"
    session.install("flake8")
    session.run("flake8", "pat_rotate.py", "azure_app_auth", "tests")


@nox.session
def black(session):
    "Black"
    session.install("black")
    session.run("black", ".")


@nox.session
def coverage(session):
    "coverage"
    session.install("coverage")
    session.install("-r", REQUIREMENTS)
    session.run("coverage", "run", "--source=.", "-m", "pytest")
    session.run("coverage", "report", "-m")
