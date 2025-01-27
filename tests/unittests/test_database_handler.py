import os
import shutil

import pytest

from gemtest.report.database_handler import DatabaseHandler, _join_values  # noqa
from gemtest.report.execution_report import GeneralMTCExecutionReport


@pytest.fixture(scope="module")
def setup_teardown_db():
    # Ensure `app/test_results/tests` is created in the current directory
    current_dir = os.getcwd()
    test_dir = os.path.join(current_dir, "gemtest_results", "tests")

    os.makedirs(test_dir, exist_ok=True)

    # Create a path for the test database
    db_path = os.path.join(test_dir, "test_database")

    # Set up the test database
    database_handler = DatabaseHandler(run_id=db_path)

    # Yield the database connection and handler
    yield database_handler

    # Clean up: close the database connection and remove the test database
    database_handler.close()

    # Remove all files in `app/test_results/` and its subdirectories
    shutil.rmtree("gemtest_results/tests")


def test_database_handler_create_table(setup_teardown_db):
    database_handler = setup_teardown_db

    # Verify that the "mtc_results" table exists in the test database
    cursor = database_handler.conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='mtc_results'")
    result = cursor.fetchone()
    assert result is not None


def test_database_handler_insert_and_retrieve(setup_teardown_db):
    database_handler = setup_teardown_db

    # Create an instance of GeneralMTCExecutionReport
    result = GeneralMTCExecutionReport()
    result.mtc_name = "Test MTC"
    result.mr_name = "Test MR"
    # use default for rest of attributes

    # Insert the dictionary into the database
    database_handler.insert([result])

    # Retrieve the inserted data from the database
    cursor = database_handler.conn.cursor()
    cursor.execute("SELECT * FROM mtc_results")
    row = cursor.fetchone()

    # Verify that the retrieved data matches the inserted data
    assert row[1] == result.date
    assert row[2] == result.mtc_name
    assert row[3] == result.mr_name


def test_shorten_join():
    values = ["This is a very long string value", "this not"]
    result = _join_values(values)
    expected = 'This is a very long string value__\n\r__this not'
    assert result == expected
