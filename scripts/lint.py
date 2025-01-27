import sys
from subprocess import CalledProcessError, run  # nosec


def lint() -> None:
    try:
        run(
            [
                "poetry", "run", "prospector", "gemtest", "-A", "-F",
                *sys.argv[1:]
            ],
            check=True
        )
    except CalledProcessError:
        print("Linting failed")
        sys.exit(1)
