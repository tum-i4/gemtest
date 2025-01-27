import pytest

from gemtest.decorator import (
    transformation,
    general_transformation,
    relation,
    general_relation
)
from gemtest.metamorphic_test_case import MetamorphicTestCase
from gemtest.metamorphic_test_suite import MetamorphicTestSuite
from gemtest.register import create_metamorphic_relation
from gemtest.testing_strategy import TestingStrategy

NAME = 'test'
DATA = range(100)


@pytest.fixture
def mts():
    # create singelton object for all tests
    mts = MetamorphicTestSuite()
    yield mts
    # reset singelton object after each test
    mts.get_metamorphic_relations().clear()


def get_id(name):
    return f'test_decorator.{name}'


def dummy_transformation(source_input):
    followup_input = source_input
    return followup_input


def dummy_transformation_2(source_input):
    followup_input = source_input
    return followup_input


def dummy_general_transformation(mtc: MetamorphicTestCase):
    followup_input = mtc.source_inputs[0]
    return followup_input


def dummy_general_transformation_2(mtc: MetamorphicTestCase):
    followup_input = mtc.source_inputs[0]
    return followup_input


def dummy_relation(source_output, followup_output):
    return source_output == followup_output


def dummy_relation_2(source_output, followup_output):
    return source_output == followup_output


def dummy_general_relation(mtc: MetamorphicTestCase):
    return mtc.source_outputs[0] == mtc.followup_outputs[0]


def dummy_general_relation_2(mtc: MetamorphicTestCase):
    return mtc.source_outputs[0] == mtc.followup_outputs[0]


def dummy_sut(x):
    return x + 42


def dummy_sut_2(x):
    return x + 42


def dummy_valid_input(x):
    return x in [0, 1]


def test_create_metamorphic_relation(mts):
    create_metamorphic_relation(name=NAME,
                                data=DATA,
                                testing_strategy=TestingStrategy.SAMPLE,
                                number_of_sources=1,
                                number_of_test_cases=10)
    assert mts.get_metamorphic_relation(get_id(NAME))
    assert mts.get_metamorphic_relation(get_id(NAME)).mr_id == get_id(NAME)
    assert mts.get_metamorphic_relation(get_id(NAME)).data == DATA
    assert mts.get_metamorphic_relation(get_id(NAME)).testing_strategy \
           == TestingStrategy.SAMPLE
    assert mts.get_metamorphic_relation(get_id(NAME)).number_of_sources == 1
    assert mts.get_metamorphic_relation(get_id(NAME)).number_of_test_cases == 10


def test_create_metamorphic_relation_missing_name(mts):
    with pytest.raises(TypeError):
        create_metamorphic_relation(data=DATA,
                                    number_of_sources=1,
                                    number_of_test_cases=10)


def test_create_metamorphic_relation_missing_data(mts):
    with pytest.raises(TypeError):
        create_metamorphic_relation(name=NAME,
                                    number_of_sources=1,
                                    number_of_test_cases=10)


def test_create_metamorphic_relation_default_testing_strategy(mts):
    create_metamorphic_relation(name=NAME, data=DATA)

    assert mts.get_metamorphic_relation(get_id(NAME)).testing_strategy \
           == TestingStrategy.EXHAUSTIVE


def test_create_metamorphic_relation_default_number_of_sources(mts):
    create_metamorphic_relation(name=NAME, data=DATA)

    assert mts.get_metamorphic_relation(get_id(NAME)).number_of_sources == 1


def test_create_metamorphic_relation_default_number_of_test_cases(mts):
    create_metamorphic_relation(name=NAME, data=DATA)

    assert mts.get_metamorphic_relation(get_id(NAME)).number_of_test_cases == 1


def test_create_metamorphic_relation_with_transformation(mts):
    create_metamorphic_relation(name=NAME,
                                data=DATA,
                                transform=dummy_transformation)

    assert mts.get_metamorphic_relation(get_id(NAME)).transform == dummy_transformation


def test_create_metamorphic_relation_with_general_transformation(mts):
    create_metamorphic_relation(name=NAME,
                                data=DATA,
                                general_transform=dummy_general_transformation)

    assert mts.get_metamorphic_relation(get_id(NAME)).general_transform == \
           dummy_general_transformation


def test_create_metamorphic_relation_with_relation(mts):
    create_metamorphic_relation(name=NAME,
                                data=DATA,
                                relation=dummy_relation)

    assert mts.get_metamorphic_relation(get_id(NAME)).relation == dummy_relation


def test_create_metamorphic_relation_with_general_relation(mts):
    create_metamorphic_relation(name=NAME,
                                data=DATA,
                                general_relation=dummy_general_relation)

    assert mts.get_metamorphic_relation(
        get_id(NAME)).general_relation == dummy_general_relation


def test_create_metamorphic_relation_with_sut(mts):
    create_metamorphic_relation(name=NAME,
                                data=DATA,
                                system_under_test=dummy_sut)
    sut_name = dummy_sut.__name__
    assert mts.get_metamorphic_relation(get_id(NAME)).system_under_test[
               sut_name] == dummy_sut


def test_create_metamorphic_relation_with_parameters(mts):
    parameters = {"x": [1, 2], "y": [3, 4]}
    create_metamorphic_relation(name=NAME,
                                data=DATA,
                                parameters=parameters)

    assert mts.get_metamorphic_relation(get_id(NAME)).sut_parameters == parameters


def test_add_transformation_to_one_metamorphic_relation(mts):
    mr_id = create_metamorphic_relation(name=NAME, data=DATA)

    # Test that the TransformWrapper instance returned by the wrapper function updates
    # the suite object with the transform function for the Metamorphic Relation ID passed
    # to the wrapper function
    result = transformation(mr_id)
    result(dummy_transformation)
    assert mts.get_metamorphic_relation(mr_id).transform == dummy_transformation


def test_add_transformation_to_multiple_metamorphic_relations(mts):
    mr_id_1 = create_metamorphic_relation(name=NAME + "_1", data=DATA)
    mr_id_2 = create_metamorphic_relation(name=NAME + "_2", data=DATA)

    result = transformation(mr_id_1, mr_id_2)
    result(dummy_transformation)
    for mr_id in mts.get_metamorphic_relations().keys():
        assert mts.get_metamorphic_relations()[mr_id].transform == dummy_transformation


def test_add_transformation_to_one_of_multiple_metamorphic_relations(mts):
    mr_id_1 = create_metamorphic_relation(name=NAME + "_1", data=DATA)
    mr_id_2 = create_metamorphic_relation(name=NAME + "_2", data=DATA)

    result = transformation(mr_id_1)
    result(dummy_transformation)

    assert mts.get_metamorphic_relations()[mr_id_1].transform == dummy_transformation
    assert mts.get_metamorphic_relations()[mr_id_2].transform is None


def test_add_multiple_transformations_to_metamorphic_relation(mts):
    mr_id_1 = create_metamorphic_relation(name=NAME + "_1", data=DATA)

    result = transformation(mr_id_1)
    result(dummy_transformation)

    with pytest.raises(ValueError):
        result(dummy_transformation_2)


def test_add_general_transformation_to_one_metamorphic_relation(mts):
    mr_id = create_metamorphic_relation(name=NAME, data=DATA)

    result = general_transformation(mr_id)
    result(dummy_general_transformation)
    assert mts.get_metamorphic_relations()[mr_id].general_transform == \
           dummy_general_transformation


def test_add_general_transformation_to_multiple_metamorphic_relations(mts):
    mr_id_1 = create_metamorphic_relation(name=NAME + "_1", data=DATA)
    mr_id_2 = create_metamorphic_relation(name=NAME + "_2", data=DATA)

    result = general_transformation(mr_id_1, mr_id_2)
    result(dummy_general_transformation)
    for mr_id in mts.get_metamorphic_relations().keys():
        assert mts.get_metamorphic_relations()[mr_id].general_transform == \
               dummy_general_transformation


def test_add_general_transformation_to_one_of_multiple_metamorphic_relations(mts):
    mr_id_1 = create_metamorphic_relation(name=NAME + "_1", data=DATA)
    mr_id_2 = create_metamorphic_relation(name=NAME + "_2", data=DATA)

    result = general_transformation(mr_id_1)
    result(dummy_general_transformation)

    assert mts.get_metamorphic_relations()[mr_id_1].general_transform == \
           dummy_general_transformation
    assert mts.get_metamorphic_relations()[mr_id_2].general_transform is None


def test_add_multiple_general_transformations_to_metamorphic_relation(mts):
    mr_id_1 = create_metamorphic_relation(name=NAME + "_1", data=DATA)

    result = general_transformation(mr_id_1)
    result(dummy_general_transformation)

    with pytest.raises(ValueError):
        result(dummy_general_transformation_2)


def test_add_relation_to_one_metamorphic_relation(mts):
    mr_id = create_metamorphic_relation(name=NAME, data=DATA)

    result = relation(mr_id)
    result(dummy_relation)
    assert mts.get_metamorphic_relations()[mr_id].relation == dummy_relation


def test_add_relation_to_multiple_metamorphic_relations(mts):
    mr_id_1 = create_metamorphic_relation(name=NAME + "_1", data=DATA)
    mr_id_2 = create_metamorphic_relation(name=NAME + "_2", data=DATA)

    result = relation(mr_id_1, mr_id_2)
    result(dummy_relation)
    for mr_id in mts.get_metamorphic_relations().keys():
        assert mts.get_metamorphic_relations()[mr_id].relation == dummy_relation


def test_add_relation_to_one_of_multiple_metamorphic_relations(mts):
    mr_id_1 = create_metamorphic_relation(name=NAME + "_1", data=DATA)
    mr_id_2 = create_metamorphic_relation(name=NAME + "_2", data=DATA)

    result = relation(mr_id_1)
    result(dummy_relation)

    assert mts.get_metamorphic_relations()[mr_id_1].relation == dummy_relation
    assert mts.get_metamorphic_relations()[mr_id_2].relation is None


def test_add_multiple_relations_to_metamorphic_relation(mts):
    mr_id_1 = create_metamorphic_relation(name=NAME + "_1", data=DATA)

    result = relation(mr_id_1)
    result(dummy_relation)

    with pytest.raises(ValueError):
        result(dummy_relation_2)


def test_add_general_relation_to_one_metamorphic_relation(mts):
    mr_id = create_metamorphic_relation(name=NAME, data=DATA)

    result = general_relation(mr_id)
    result(dummy_general_relation)
    assert mts.get_metamorphic_relations()[mr_id].general_relation == dummy_general_relation


def test_add_general_relation_to_multiple_metamorphic_relations(mts):
    mr_id_1 = create_metamorphic_relation(name=NAME + "_1", data=DATA)
    mr_id_2 = create_metamorphic_relation(name=NAME + "_2", data=DATA)

    result = general_relation(mr_id_1, mr_id_2)
    result(dummy_general_relation)
    for mr_id in mts.get_metamorphic_relations().keys():
        assert mts.get_metamorphic_relations()[
                   mr_id].general_relation == dummy_general_relation


def test_add_general_relation_to_one_of_multiple_metamorphic_relations(mts):
    mr_id_1 = create_metamorphic_relation(name=NAME + "_1", data=DATA)
    mr_id_2 = create_metamorphic_relation(name=NAME + "_2", data=DATA)

    result = general_relation(mr_id_1)
    result(dummy_general_relation)

    assert mts.get_metamorphic_relations()[mr_id_1].general_relation == dummy_general_relation
    assert mts.get_metamorphic_relations()[mr_id_2].general_relation is None


def test_add_multiple_general_relations_to_metamorphic_relation(mts):
    mr_id_1 = create_metamorphic_relation(name=NAME + "_1", data=DATA)

    result = general_relation(mr_id_1)
    result(dummy_general_relation)

    with pytest.raises(ValueError):
        result(dummy_general_relation_2)
