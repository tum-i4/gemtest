import json
import os
import os.path
import sqlite3
from typing import List

from .execution_report import GeneralMTCExecutionReport


def _join_values(values: List[str]):
    str_values = []
    for value in values:
        value = str(value)
        str_values.append(value)
    separator = "__\n\r__"
    return separator.join(str_values)


class DatabaseHandler:
    """
    A class for handling a SQLite database.

    Attributes
    ----------
    run_id : str
        The run ID for the database.
    conn : sqlite3.Connection
        Connection object to the database.
    """

    def __init__(self, run_id: str):
        self.run_id = run_id
        self.conn = self.open_connection()

    @staticmethod
    def create_table():
        """
        Returns the SQL statement for creating the 'mtc_results' table.
        """
        return """
                    CREATE TABLE mtc_results (
                        _id INTEGER PRIMARY KEY,
                        date DATETIME NOT NULL,
                        mtc_name TEXT NOT NULL,
                        mr_name TEXT NOT NULL,
                        sut_name TEXT NOT NULL,
                        source_inputs TEXT NOT NULL,
                        source_outputs TEXT NOT NULL,
                        followup_inputs TEXT NOT NULL,
                        followup_outputs TEXT NOT NULL,
                        transformation_name TEXT NOT NULL,
                        relation_name TEXT NOT NULL,
                        test_result TEXT NOT NULL,
                        relation_result TEXT NOT NULL,
                        parameters TEXT NOT NULL,
                        stdout TEXT NOT NULL,
                        stderr TEXT NOT NULL,
                        duration REAL NOT NULL
                    )
                """

    def open_connection(self):
        """
        Opens a connection to the SQLite database.

        Returns
        -------
        sqlite3.Connection
            Connection object to the database.
        """
        # Get the current working directory
        current_dir = os.getcwd()

        # Define the path to the `test_results` folder within the current directory
        test_results_dir = os.path.join(current_dir, "gemtest_results")

        if not os.path.exists(test_results_dir):
            os.makedirs(test_results_dir)

        db_path = os.path.join(test_results_dir, f"{self.run_id}.db")
        # Set up a connection to the database
        conn = sqlite3.connect(db_path)
        if os.path.isfile(db_path):
            # overwrite db if it already exists - should never be the case
            cursor = conn.cursor()
            table_name = 'mtc_results'
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

        conn.execute(DatabaseHandler.create_table())
        return conn

    def insert(self, results: List[GeneralMTCExecutionReport]):
        """
        Inserts results into the 'mtc_results' table.

        Parameters
        ----------
        results : list
            List of result objects to be inserted.
        """
        for result in results:
            self.conn.execute(
                """
                INSERT INTO mtc_results (
                    date,
                    mtc_name,
                    mr_name,
                    sut_name,
                    source_inputs,
                    source_outputs,
                    followup_inputs,
                    followup_outputs,
                    transformation_name,
                    relation_name,
                    test_result,
                    relation_result,
                    parameters,
                    stdout,
                    stderr,
                    duration
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    result.date,
                    result.mtc_name,
                    result.mr_name,
                    result.sut_name,
                    _join_values(result.source_inputs),
                    _join_values(result.source_outputs),
                    _join_values(result.followup_inputs),
                    _join_values(result.followup_outputs),
                    result.transformation_name,
                    result.relation_name,
                    result.test_result,
                    str(result.relation_result),
                    json.dumps(result.parameters),
                    result.stdout,
                    result.stderr,
                    result.duration
                ),
            )

        self.conn.commit()

    def close(self):
        """
        Closes the connection to the SQLite database.
        """
        self.conn.close()
