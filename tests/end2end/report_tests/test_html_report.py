import os
from datetime import datetime
from pathlib import Path

import pytest

def get_most_recent_run_name(folder_path):
    # Get the most recent test_run database name
    test_runs = [f for f in os.listdir(folder_path) if
                 os.path.isfile(os.path.join(folder_path, f))]
    return max(test_runs, key=lambda f: extract_datetime_from_filename(f))


def extract_datetime_from_filename(file_name):
    # function to extract the datetime of the test execution from the database filename
    file_name = file_name.replace("metamorphic_test_run_", "").replace(".db", "")
    return datetime.strptime(file_name, "%Y-%m-%d_%H-%M-%S")


@pytest.fixture(scope="function")
def remove_db():
    yield

    test_results_dir = os.path.join(os.getcwd(), "gemtest_results")

    if os.path.exists(test_results_dir):
        most_recent_run = get_most_recent_run_name(test_results_dir)
        db_path = os.path.join(test_results_dir, most_recent_run)
        os.remove(db_path)


def test_example_string_report(remove_db):
    """
    This test checks if there is an error when executing a test file with the framework
    with the --html-report commandline argument. The test does not test the functionality
    of the html report, which is done in an unittest.
    """
    result = pytest.main([
        str(Path(__file__).parent / "test_example.py"),
        '--html-report'
    ])

    # perform assertions based on the outcome of the called pytest
    assert result == pytest.ExitCode.OK
