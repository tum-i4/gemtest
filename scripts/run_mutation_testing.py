import argparse
import os
import sys
from subprocess import CalledProcessError, run

_BASE_CONFIG_PATH: str = "gmt_mutation_config.toml"
_BASE_DATABASE_PATH: str = "gmt_mutation.sqlite"


def safe_run(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except CalledProcessError:
            print("Tests failed")
            sys.exit(1)
        except OSError as e:
            print(f"Could not operate on file.\n {e}")
            sys.exit(1)

    return wrapper


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", type=str, help="Path to config file")
    parser.add_argument("--database_path", type=str, help="Path to database file")

    return parser.parse_args()


@safe_run
def run_cosmic_ray() -> None:
    args = parse_arguments()
    if args.config_path is None:
        print(f'No configuration path provided, defaulting to {_BASE_CONFIG_PATH}')
        args.config_path = _BASE_CONFIG_PATH
    if args.database_path is None:
        print(f'No database path provided, defaulting to {_BASE_DATABASE_PATH}')
        args.database_path = _BASE_DATABASE_PATH

    if not os.path.exists(args.config_path):
        _create_new_config(args.config_path)

    if not os.path.exists(args.database_path):
        _init_new_session(args.config_path, args.database_path)

    _check_baseline(args.config_path)

    _execute(args.config_path, args.database_path)

    _create_report(args.database_path)

    _create_html_report(args.database_path)


def _create_new_config(config_path: str) -> None:
    run(args=["cosmic-ray", "new-config", config_path], check=True)


@safe_run
def create_new_config() -> None:
    args = parse_arguments()
    if args.config_path is None:
        raise ValueError("No config_path specified")

    _create_new_config(args.config_path)


def _init_new_session(config_path: str, database_path: str) -> None:
    run(args=["cosmic-ray", "init", config_path, database_path], check=True)


@safe_run
def init_new_session() -> None:
    args = parse_arguments()
    if args.config_path is None:
        raise ValueError("No config_path specified")
    if args.database_path is None:
        raise ValueError("No database_path specified")

    _init_new_session(args.config_path, args.database_path)


def _check_baseline(config_path: str) -> None:
    run(args=["cosmic-ray", "--verbosity=INFO", "baseline", config_path], check=True)


@safe_run
def check_baseline() -> None:
    args = parse_arguments()
    if args.config_path is None:
        raise ValueError("No config_path specified")

    _check_baseline(args.config_path)


def _execute(config_path: str, database_path: str) -> None:
    run(args=["cosmic-ray", "exec", config_path, database_path], check=True)


@safe_run
def execute() -> None:
    args = parse_arguments()
    if args.config_path is None:
        raise ValueError("No config_path specified")
    if args.database_path is None:
        raise ValueError("No database_path specified")

    _execute(args.config_path, args.database_path)


def _create_report(database_path: str) -> None:
    run(args=["cr-report", database_path, "--show-pending"], check=True)


@safe_run
def create_report() -> None:
    args = parse_arguments()
    if args.database_path is None:
        raise ValueError("No database_path specified")

    _create_report(args.database_path)


def _create_html_report(database_path: str) -> None:
    html_file_path = os.path.dirname(os.path.abspath(database_path))
    p = run(args=["cr-html", database_path], check=True, capture_output=True, encoding='utf-8')

    html_file = open(os.path.join(html_file_path, 'mutation_report.html'), 'w')
    html_file.write(p.stdout)
    html_file.close()


@safe_run
def create_html_report() -> None:
    args = parse_arguments()
    if args.database_path is None:
        raise ValueError("No database_path specified")

    _create_html_report(args.database_path)
