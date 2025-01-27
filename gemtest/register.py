from typing import Sequence, Optional, Dict

from .metamorphic_test_suite import MetamorphicTestSuite
from .testing_strategy import TestingStrategy
from .types import System, Transform, GeneralTransform, Relation, GeneralRelation, \
    Input, MR_ID


def create_metamorphic_relation(  # noqa - too many arguments
        name: str,
        data: Sequence,
        testing_strategy: str = TestingStrategy.EXHAUSTIVE,
        number_of_test_cases: int = 1,
        number_of_sources: int = 1,
        parameters: Optional[Dict] = None,
        system_under_test: Optional[System] = None,
        transform: Optional[Transform] = None,
        general_transform: Optional[GeneralTransform] = None,
        relation: Optional[Relation] = None,
        general_relation: Optional[GeneralRelation] = None,
        valid_input: Optional[Input] = None
) -> MR_ID:
    """
    Registers a new metamorphic relation.

    Registering the (general) transform, (general) relation and system under test can be
    done during registration, or later by decorating the appropriate functions.

    Parameters
    ----------
    name : str
        Name of the metamorphic test.
    data : Sequence
        Dataset from which the source inputs to the metamorphic test cases is selected.
    testing_strategy : TestingStrategy
        Strategy for metamorphic test case creation.
    number_of_test_cases : int
        Number of metamorphic test cases that are executed when testing this metamorphic
        relation.
    number_of_sources : int
        Number of source inputs used by the transformation.
    parameters : Optional[Dict]
        Optional list of test parameters. Can be used to define multiple similar tests with
        different parameters.
    system_under_test : Optional[System]
        The system under test whose functionality is to be verified. Defaults to None.
    transform : Optional[Transform]
        Optional transformation function. Defaults to None.
    general_transform: Optional[GeneralTransform]
        Optional general transformation function. Default to None.
    relation : Optional[Relation]
        Optional relation function. Defaults to None.
    general_relation : Optional[GeneralRelation]
        Optional general relation function. Defaults to None.
    valid_input : Optional[Input]
        Optional valid input function. Defaults to None.

    Returns
    -------
    mr_id : MR_ID
        The unique identifier of the metamorphic relation. Can be used to register
        decorated functions to the specified metamorphic relation.
    """

    mr_id = MetamorphicTestSuite().add_metamorphic_relation(name, data, testing_strategy,
                                                            number_of_test_cases,
                                                            number_of_sources)

    if parameters is not None:
        MetamorphicTestSuite().get_metamorphic_relation(mr_id).sut_parameters = parameters
    if system_under_test is not None:
        MetamorphicTestSuite().get_metamorphic_relation(
            mr_id).system_under_test = system_under_test
    if transform is not None:
        MetamorphicTestSuite().get_metamorphic_relation(mr_id).transform = transform
    if general_transform is not None:
        MetamorphicTestSuite().get_metamorphic_relation(
            mr_id).general_transform = general_transform
    if relation is not None:
        MetamorphicTestSuite().get_metamorphic_relation(mr_id).relation = relation
    if general_relation is not None:
        MetamorphicTestSuite().get_metamorphic_relation(
            mr_id).general_relation = general_relation
    if valid_input is not None:
        MetamorphicTestSuite().get_metamorphic_relation(mr_id).valid_input.append(
            valid_input)

    # generate the metamorphic test cases for the metamorphic relation
    MetamorphicTestSuite().get_metamorphic_relation(mr_id).generate_test_cases()

    return mr_id
