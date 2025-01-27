import pytest
from _pytest.outcomes import Skipped

import gemtest as gmt
from gemtest.metamorphic_error import SkippedMTC
from gemtest.metamorphic_relation import MetamorphicRelation
from gemtest.metamorphic_test_case import MetamorphicTestCase
from gemtest.metamorphic_test_suite import MetamorphicTestSuite
from gemtest.testing_strategy import TestingStrategy

DATA = range(100)


def test_transformation_gmt_skip():
    mr = MetamorphicRelation(mr_id="mr_gmt_skip", data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=1)

    def _transform(_):
        gmt.skip("Test has been skipped")

    mr.transform = _transform
    test_case = MetamorphicTestCase()
    test_case.source_inputs = [0]
    mr.apply_transformation(test_case)
    assert isinstance(test_case.error, SkippedMTC)


def dummy_transformation(_):
    pytest.skip("Test has been skipped")


def dummy_sut(*_, **__):
    return 1


def test_transformation_pytest_skip():
    mr_id = gmt.create_metamorphic_relation(name="mr_pytest_skip",
                                            data=range(10),
                                            relation=gmt.equality,
                                            testing_strategy=gmt.TestingStrategy.EXHAUSTIVE,
                                            number_of_test_cases=1,
                                            transform=dummy_transformation)
    sut_name = dummy_sut.__name__
    try:
        with pytest.raises(SystemExit):
            sut = gmt.system_under_test(mr_id)(dummy_sut)
            mr_name = "tests.end2end.test_gmt_skip.mr_pytest_skip"
            metamorphic_relation = MetamorphicTestSuite().get_metamorphic_relation(mr_name)
            tcs = metamorphic_relation.test_cases[sut_name]
            tc = tcs[0]
            sut(sut_name, mr_id, tc)
    except Skipped:
        raise Exception("pytest.skip() does not get blocked.")
