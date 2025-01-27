from pathlib import Path

import pytest
import logging

from gemtest import logger


@pytest.fixture(autouse=True)
def disable_logger(request):
    disable_logger = request.config.getoption('--disable-logger')

    if disable_logger:
        logger.setLevel(logging.WARNING)


def test_example_string_report():
    """
    This test checks if there is an error when executing a test file with the framework
    with the --string-report commandline argument. The test does not test the functionality
    of the string report which is done in an unittest.
    """
    result = pytest.main([
        str(Path(__file__).parent / "test_example.py"),
        '--string-report'
    ])
    # perform assertions based on the outcome of the called pytest
    assert result == pytest.ExitCode.OK
