import subprocess
import pytest
import os
import shutil

# Path to the test result directory
CURRENT_DIR = os.getcwd()
TEST_RESULT_DIR = os.path.join(CURRENT_DIR, "gemtest_results")

def run_pytest_with_flags(flags=""):
    """
    Runs pytest with the given flags and returns the result.
    """
    command = f"poetry run pytest tests/end2end/report_tests/test_example.py {flags}"
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    return result

def cleanup_test_results():
    """
    Deletes all files in the test result directory after test execution.
    This ensures that further tests are not affected by these files.
    """
    if os.path.exists(TEST_RESULT_DIR):
        shutil.rmtree(TEST_RESULT_DIR)
        os.makedirs(TEST_RESULT_DIR)

@pytest.fixture(scope="module", autouse=True)
def cleanup_after_test():
    """
    Pytest fixture that runs after each test to clean up test result files.
    """
    yield
    cleanup_test_results()

def test_pytest_without_flags():
    """
    Test pytest execution without any flags.
    """
    result = run_pytest_with_flags()
    assert result.returncode == 0
    assert "40 xpassed" in result.stdout and "1 skipped" in result.stdout

def test_pytest_with_valid_flags():
    """
    Test pytest execution with various flags. Should not cause an error. 
    """
    flags = "--html-report --string-report --sut_filepath="""
    result = run_pytest_with_flags(flags)
    assert result.returncode == 0
    assert "40 xpassed" in result.stdout and "1 skipped" in result.stdout
    assert (
        "A data exporter was detected but intentionally not run. To also run the exporter, use the command line flag --export-data"
        in result.stdout
    )

    assert "This test was run with the command line flag --html-report." in result.stdout
    assert "To visualize test results in the webapp, install the webapp by running:" in result.stdout
    assert "pip install gemtest-webapp" in result.stdout
    assert "Launch the webapp by running:" in result.stdout
    assert "gemtest-webapp --results-dir <path-to-gemtest-results-folder>" in result.stdout
    assert " ------ test_dummy_sut ----->" in result.stdout


    # Verify that the report files were created
    assert os.path.exists(TEST_RESULT_DIR), "Test result directory not found"
    assert len(os.listdir(TEST_RESULT_DIR)) > 0, "No files generated in test result directory"

def test_pytest_with_spelling_error_flag():
    """
    Test pytest execution with a misspelled flag.
    """
    flags = "--htlm-report"
    result = run_pytest_with_flags(flags)

    assert result.returncode != 0
    assert "error: unrecognized arguments: --htlm-report" in result.stderr

def test_pytest_with_missing_argument_flag():
    """
    Test pytest execution with a flag that requires an argument but is missing it.
    """
    flags = "--batch_size"  # Missing argument "= x" 
    result = run_pytest_with_flags(flags)

    assert result.returncode != 0
    assert "error: argument --batch_size: expected one argument" in result.stderr

def test_pytest_with_incorrect_argument_type():
    """
    Test pytest execution with batchsize flag set. Input is a list but SUT expects a real number
    """
    flags = "--batch_size=1"
    
    result = run_pytest_with_flags(flags)
    
    assert result.returncode == 3
    
    # Check stdout for SystemExit and the Messages returned 
    assert "SystemExit" in result.stdout  
    assert "A TypeError occurred" in result.stdout  
    assert "must be real number, not list" in result.stdout