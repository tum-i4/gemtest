import sys
import webbrowser
from os import getcwd
from subprocess import CalledProcessError, run  # nosec


def html_coverage() -> None:
    try:
        run(
            ["poetry", "run", "coverage", "run", "-m", "pytest", "tests"],
            check=True
        )
    except CalledProcessError:
        print("Tests failed")
        sys.exit(1)
    run(
        ["poetry", "run", "coverage", "html"],
        check=True
    )
    webbrowser.open(f"file://{getcwd()}/htmlcov/index.html")
