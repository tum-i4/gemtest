import sys
from subprocess import CalledProcessError, run  # nosec


def run_tests() -> None:
    try:
        run(
            [
                "poetry", "run", "pytest", "tests", "--capture=tee-sys",
                *sys.argv[1:]
            ],
            check=True
        )
    except CalledProcessError:
        print("Tests failed")
        sys.exit(1)
