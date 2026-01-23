import nox

@nox.session(python=["3.10", "3.11", "3.12"])
def tests(session):
    """Run the test suite."""
    session.install(".")
    session.install("pytest")
    session.run("pytest")

@nox.session
def lint(session):
    """Run linting and type checking."""
    session.install("ruff", "mypy")
    session.run("ruff", "check", ".")
    session.run("mypy", "src")
