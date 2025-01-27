import collections
import inspect

import pytest

test_results = collections.defaultdict(dict)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call) -> None:
    """
    The actual wrapper that gets called before and after every test. Used to record the
    outcome of the Pytests executed by the framework. These results can then be used for
    meta system tests of the framework, testing the expected number of passed / failed
    test cases i.e. which test cases in particular passed / failed. Possibility to extend
    to more metrics, look at item and rep object.
    """
    global test_results
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        test_module_name = item.path.name.split(".py")[0]
        test_case_name = item.name.split('[')[-1].split(']')[0]

        test_results[test_module_name][test_case_name] = rep.outcome

        test_results[test_module_name]['number_of_passed_tests'] = \
            sum(1 for test_case_outcome in test_results[test_module_name].values() if
                test_case_outcome == 'passed')

        test_results[test_module_name]['number_of_failed_tests'] = \
            sum(1 for test_case_outcome in test_results[test_module_name].values() if
                test_case_outcome == 'skipped')


def get_test_file_name() -> str:
    """
    Returns the name of the pyton file from which a system test is executed.
    """
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    if module is not None:
        return module.__name__.split(".")[-1]
    raise ValueError('Internal Error: no calling module found.')
