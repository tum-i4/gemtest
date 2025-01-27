from typing import TypeVar, Callable, List, Union

import pytest
from pytest import MonkeyPatch

from .conftest import get_conftest_config
from .generator import MetamorphicGenerator
from .metamorphic_error import InvalidInputError, SkippedMTC
from .metamorphic_test_case import MetamorphicTestCase
from .metamorphic_test_suite import MetamorphicTestSuite
from .testcase_queue import InputQueue, InputQueueItem
from .types import Input, System, Transform, GeneralTransform, Relation, GeneralRelation, MR_ID
from .utils.sut_loader import get_sut
from .utils.wrong_skip_method_used import wrong_skip_method_used

A = TypeVar('A')

TransformWrapper = Callable[[Transform], Transform]
GeneralTransformWrapper = Callable[[GeneralTransform], GeneralTransform]
RelationWrapper = Callable[[Relation], Relation]
GeneralRelationWrapper = Callable[[GeneralRelation], GeneralRelation]
InputWrapper = Callable[[Input], Input]
SystemWrapper = Callable[[System], System]


def _get_metamorphic_relation_ids(*mr_ids: MR_ID) -> List[MR_ID]:
    """
    Generates a list of metamorphic relation ids on which a decorated function is
    registered. If metamorphic relation ids are explicitly specified, the decorated
    function is registered on these ids. If no Ids are specified, the decorated function is
    registered on all metamorphic relations of the test module that it is defined in.

    Parameters
    ----------
    *mr_ids:
        A variable number of MR_IDs.

    Returns
    -------
        A list of MR_IDs.
    """
    if mr_ids:
        return list(mr_ids)

    module_name = MetamorphicTestSuite().get_caller_module()
    return [mr_id for mr_id in MetamorphicTestSuite().get_metamorphic_relations() if
            module_name in mr_id]  # type: ignore # noqa


def transformation(*mr_ids: MR_ID) -> TransformWrapper:
    """
    Registers the decorated function as a transformation for a pre-defined metamorphic
    relation. A transformation takes a single source input and creates a single source
    output.

    Parameters
    ----------
    <mr1_name, mr2_name, …>:
        The names of the metamorphic relations to which this transformation is applied.

    Returns
    -------
    follow-up input:
        A follow-up input, derived by applying the transformation function
        to the source inputs.
        Source inputs are specified in the metamorphic relations.

    Example
    -------
    >>> @gmt.transformation(<mr1_name, mr2_name, ... >)
    >>> def example_transformation(source_input: int):
    >>>    # <Apply custom transformation to source input>
    >>>    return followup_input

    See Also
    --------
    general_transformation:
        Registers a general transformation function for a
        metamorphic relation.
    suite:
        The object that holds all the metamorphic relations.
    """

    # Developer Documentation

    #     Parameters
    #     ----------
    #     mr_ids : Union[MR_ID, List[MR_ID]]
    #         Id of the metamorphic relation that is supposed to use the decorated function
    #         as transformation.

    #     Returns
    #     -------
    #     wrapper : TransformWrapper
    #         A function which would ultimately register the transformation defined
    #         in the function decorated with this decorator to the suite.

    #     See Also
    #     --------
    #     general_transformation: Registers a general transformation function for a
    #         Metamorphic Relation.
    #     suite: The object that holds all the metamorphic relations.

    def wrapper(transform: Transform) -> Transform:
        for mr_id in _get_metamorphic_relation_ids(*mr_ids):
            MetamorphicTestSuite().get_metamorphic_relation(mr_id).transform = transform
        return transform

    return wrapper


def general_transformation(*mr_ids: MR_ID) -> GeneralTransformWrapper:
    """
    Registers the decorated function as a general transformation for a pre-defined
    metamorphic relation. A general transformation uses a metamorphic test case as
    parameter to allow the tester to specify any form of transformation using multiple
    source inputs and outputs to create multiple followup inputs.

    Parameters
    ----------
    <mr1_name, mr2_name, …>:
        The names of the metamorphic relations to which this transformation is applied.

    Returns
    -------
    multiple follow-up inputs:
        A single follow-up input, is derived by applying
        the general transformation function to a source input.
        Source inputs are specified in the metamorphic relations.\n
        The general transformation takes multiple source inputs
        and returns multiple follow-up inputs.

    Example
    -------
    >>> @gmt.general_transformation(<mr1_name, mr2_name, ... >)
    >>> def example_general_transformation(mtc: MetamorphicTestCase) -> Input:
    >>>     # <access single source_input>
    >>>     input = mtc.source_input

    >>>     # <access multiple source_inputs>
    >>>     input_list = mtc.source_inputs

    >>>     # <apply custom transformation to Input>
    >>>     return followup_input_1, followup_input_2, ... , followup_input_n

    See Also
    --------
    transformation:
        Registers a transformation function for a metamorphic relation.
    suite:
        The object that holds all the metamorphic relations.
    """

    # Developer Documentation

    #     Parameters
    #     ----------s
    #     mr_ids : Union[MR_ID, List[MR_ID]]
    #         Id of the metamorphic relation that is supposed to use the decorated function
    #         as general transformation.

    #     Returns
    #     -------
    #     wrapper : GeneralTransformWrapper
    #         A function which would ultimately register the general transformation defined
    #         in the function decorated with this decorator to the suite.

    #     See Also
    #     --------
    #     transformation: Registers a  transformation function for a metamorphic relation.
    #     suite: The object that holds all the metamorphic relations.

    def wrapper(general_transform: GeneralTransform) -> GeneralTransform:
        for mr_id in _get_metamorphic_relation_ids(*mr_ids):
            MetamorphicTestSuite().get_metamorphic_relation(
                mr_id).general_transform = general_transform
        return general_transform

    return wrapper


def relation(*mr_ids: MR_ID) -> RelationWrapper:
    """
    Registers the decorated function as a relation for a pre-defined metamorphic
    relation. A relation takes a single source output and followup output to evaluate if
    the metamorphic relation holds for a specific metamorphic test case.

    Parameters
    ----------
    <mr1_name, mr2_name, …>:
        The names of the metamorphic relations to which this relation is applied.

    Returns
    -------
    Boolean:
        The output of the relation indicates whether the specified relation holds or not.

    Example
    -------
    >>> @gmt.relation(<mr1_name, mr2_name, ... >)
    >>> def example_relation(source_output: Output, followup_output: Output) -> bool:
    >>>     #<apply custom relation to Outputs>

    See Also
    --------
    general_relation:
        Registers a general relation function for a metamorphic relation.
    suite:
        The object that holds all the metamorphic relations.
    """

    # Developer Documentation

    #     Parameters
    #     ----------
    #     mr_ids : Union[MR_ID, List[MR_ID]]
    #         Id of the metamorphic relation that is supposed to use the decorated function
    #         as relation.

    #     Returns
    #     -------
    #     wrapper : RelationWrapper
    #         A function which would ultimately register the relation defined
    #         in the function decorated with this decorator to the suite.

    #     See Also
    #     --------
    #     general_relation: Registers a general relation function for a metamorphic relation.
    #     suite: The object that holds all the metamorphic relations.

    def wrapper(relation_inner: Relation) -> Relation:
        for mr_id in _get_metamorphic_relation_ids(*mr_ids):
            MetamorphicTestSuite().get_metamorphic_relation(mr_id).relation = relation_inner
        return relation_inner

    return wrapper


def general_relation(*mr_ids: MR_ID) -> GeneralRelationWrapper:
    """
    Registers the decorated function as a general relation for a pre-defined metamorphic
    relation. A general relation takes a metamorphic test case as parameter to
    evaluate if the metamorphic relation holds for a specific metamorphic test case.

    Parameters
    ----------
    <mr1_name, mr2_name, …>:
        The names of the metamorphic relations to which this relation is applied.

    Returns
    -------
    Boolean:
        The output of the relation indicates whether the specified relation holds or not.

    Example
    -------
    >>> @gmt.general_relation(<mr1_name, mr2_name, ... >)
    >>> def general_relation_example(mtc: MetamorphicTestCase) -> bool:
    >>>     #<apply custom relation to attributes of MetamorphicTestCase>

    See Also
    --------
    relation:
        Registers a relation function for a metamorphic relation.
    suite:
        The object that holds all the metamorphic relations.
    """

    # Developer Documentation

    #     Parameters
    #     ----------
    #     mr_ids : Union[MR_ID, List[MR_ID]]
    #         Id of the metamorphic relation that is supposed to use the decorated function
    #         as general relation.

    #     Returns
    #     -------
    #     wrapper : RelationWrapper
    #         A function which would ultimately register the general relation defined
    #         in the function decorated with this decorator to the suite.

    #     See Also
    #     --------
    #     relation: Registers a relation function for a metamorphic relation.
    #     suite: The object that holds all the metamorphic relations.

    def wrapper(general_relation_inner: GeneralRelation) -> GeneralRelation:
        for mr_id in _get_metamorphic_relation_ids(*mr_ids):
            MetamorphicTestSuite().get_metamorphic_relation(
                mr_id).general_relation = general_relation_inner
        return general_relation_inner

    return wrapper


def sut_wrapper(sut_function: System, test_mtc, *mr_ids, **kwargs) -> System:
    metamorphic_relation_ids = _get_metamorphic_relation_ids(*mr_ids)
    sut_id = sut_function.__name__

    def get_mtcs_for_mr_sut(
            mr_id_inner: MR_ID,
            sut_id_inner: str,
    ) -> List[MetamorphicTestCase]:
        metamorphic_relation = MetamorphicTestSuite().get_metamorphic_relation(mr_id_inner)
        return metamorphic_relation.test_cases[sut_id_inner]

    for mr_id in metamorphic_relation_ids:
        mr = MetamorphicTestSuite().get_metamorphic_relation(mr_id)
        mr.system_under_test = sut_function
        mr.q_ready[sut_id] = InputQueue(
            InputQueueItem(tc, i, is_source=True)
            for tc in get_mtcs_for_mr_sut(mr_id, sut_id)
            for i, _ in enumerate(tc.source_inputs)
        )
        batch_size = kwargs.get("batch_size") if kwargs.get("batch_size") \
            else get_conftest_config().get("batch_size")
        mr.sut_batch_size[sut_id] = int(batch_size) if batch_size is not None else None

        for mtc in get_mtcs_for_mr_sut(mr_id, sut_id):
            mtc.data_loader = kwargs.get("data_loader", None)

    # Prepare the parameterized markers for pytest
    markers = [
        pytest.param(sut_id, mr_id, mtc,
                     id=f"sut_id={sut_id}, mr_id={mr_id}, mtc=mtc_{index}")
        for mr_id in metamorphic_relation_ids
        for index, mtc in enumerate(get_mtcs_for_mr_sut(mr_id, sut_id), start=1)
    ]

    return pytest.mark.metamorphic_relation(
        visualize_input=kwargs.get('visualize_input', None),
        visualize_output=kwargs.get('visualize_output', None),
        data_exporter=kwargs.get('data_exporter', None),
        data_loader=kwargs.get('data_loader', None),
    )(
        pytest.mark.parametrize(("sut_id", "mr_id", "mtc"), markers)(test_mtc)
    )


def system_under_test(*mr_ids: MR_ID, **kwargs) -> SystemWrapper:
    """
    Registers the decorated function as a system under test for a pre-defined metamorphic
    relation. A system under test takes a single source or follow-up input and creates a
    source / followup output. The metamorphic relation is used to test if a system under
    test works as expected. Additionally, creates and executes the metamorphic test cases
    for the metamorphic relations passed as parameter.

    Parameters
    ----------
    <mr1_name, mr2_name, …>:
        The names of the metamorphic relations to which this system under test is applied.

    batch_size:
        The batch size for batch execution of the system under test.
        System under test function will need a list of inputs!

    visualize_input:
        A function to visualize an individual input to the system under test.

        Note:
        If you are using the Web Application, use this parameter
        if your input data can benefit from visual representation (e.g., images).
        If your data is already simple and easily interpretable (e.g., small numerical arrays),
        a visualizer might not be necessary.

    visualize_output:
        A function to visualize the output of the system under test.

        Note:
        If you are using the Web Application, use this parameter
        if your output data can benefit from visual representation (e.g., images).
        For straightforward outputs, the default string representation might suffice.

    data_loader:
        Loads an image resource from a file path. Enables Lazy Loading.
        The data loader returns a numpy array of the image.

    data_exporter:
        A function that exports data. The data should be stored under assets/data.

    Returns
    -------
    SUT Output:
        A function registered as System Under Test will take a single source or follow-up input
        and return the source or follow-up outputs.

    Example
    -------
    >>> @gmt.system_under_test(<mr1_name, mr2_name, ... >, batch_size)
    >>> def test_system_name(input: Input) -> Output:
    >>>     #<apply custom system functionality to Input>

    See Also
    --------
    MetamorphicRelation:
        The object used to hold the system under test, as well as the
        (general) transformation and (general) relation.
    Suite:
        The object that holds all the metamorphic relations.
    """

    # Developer Documentation

    #     Parameters
    #     ----------
    #     mr_ids : MR_ID
    #         Id of the Metamorphic Relation that is supposed to use the decorated function
    #         as system under test

    #     Returns
    #     -------
    #     wrapper : SystemWrapper
    #         A function which would ultimately register the system under test defined
    #         in the function decorated with this decorator to the suite.

    #     See Also
    #     --------
    #     MetamorphicRelation: The object used to hold the system under test, as well as the
    #         (general) transformation and (general) relation.
    #     Suite: The object that holds all the metamorphic relations.

    if get_conftest_config().get("is_sut_dynamic_active"):
        return lambda *_, **__: lambda: pytest.skip("sut_dynamic is set.")

    def test_mtc(sut_id: str, mr_id: MR_ID, mtc: MetamorphicTestCase):
        """
        The actual test function that is executed for each Metamorphic Test Case
        """
        mr = MetamorphicTestSuite().get_metamorphic_relation(mr_id)
        with MonkeyPatch().context() as monkeypatch:
            monkeypatch.setattr(pytest, "skip", wrong_skip_method_used)
            mr.execute_test_case(mtc, sut_id)

        if mtc.error and isinstance(mtc.error, (InvalidInputError, SkippedMTC)):
            pytest.skip(mtc.error.message)

        try:
            assert mtc.relation_result
        except AssertionError:
            pytest.fail("The Metamorphic Relation does not hold for this "
                        "Metamorphic Test Case", pytrace=False)

    def wrapper(sut_function: System) -> System:
        return sut_wrapper(sut_function, test_mtc, *mr_ids, **kwargs)

    return wrapper


def systems_under_test_dynamic(*mr_ids: MR_ID, **kwargs) -> SystemWrapper:
    """
    Registers the decorated function as a system under test for a pre-defined metamorphic
    relation. A system under test takes a single source or follow-up input and creates a
    source / followup output. The metamorphic relation is used to test if a system under
    test works as expected. Additionally, creates and executes the metamorphic test cases
    for the metamorphic relations passed as parameter.

    Parameters
    ----------
    sut_filepath:
        The absolute path of the file containing the SUT class.

    sut_class:
        The class name of the SUT inside the file as defined by sut_filepath.
        The only limitation is that the SUT class
        can be instantiated using an empty constructor, e.g., SUT().

    <mr1_name, mr2_name, …>:
        The names of the metamorphic relations to which this system under test is applied.

    batch_size:
        The batch size for batch execution of the system under test.
        System under test function will need a list of inputs!

    visualize_input:
        A function to visualize an individual input to the system under test.

        Note:
        If you are using the Web Application, use this parameter
        if your input data can benefit from visual representation (e.g., images).
        If your data is already simple and easily interpretable (e.g., small numerical arrays),
        a visualizer might not be necessary.

    visualize_output:
        A function to visualize the output of the system under test.

        Note:
        If you are using the Web Application, use this parameter
        if your output data can benefit from visual representation (e.g., images).
        For straightforward outputs, the default string representation might suffice.

    data_loader:
        Loads an image resource from a file path. Enables Lazy Loading.
        The data loader returns a numpy array of the image.

    data_exporter:
        A function that exports data. The data should be stored under assets/data.

    Returns
    -------
    SUT Output:
        The Dynamic System Under Test will take a single source or follow-up input
        and return the source or follow-up outputs.

    See Also
    --------
    MetamorphicRelation:
        The object used to hold the system under test, as well as the
        (general) transformation and (general) relation.
    Suite:
        The object that holds all the metamorphic relations.
    """

    # Developer Documentation

    #     Parameters
    #     ----------
    #     mr_ids : MR_ID
    #         Id of the metamorphic relation that is supposed to use the decorated function
    #         as system under test.

    #     Returns
    #     -------
    #     wrapper : SystemWrapper
    #         A function which would ultimately register the system under test defined
    #         in the function decorated with this decorator to the suite.

    #     See Also
    #     --------
    #     MetamorphicRelation: The object used to hold the system under test, as well as the
    #         (general) transformation and (general) relation.
    #     Suite: The object that holds all the metamorphic relations.

    if not get_conftest_config().get("is_sut_dynamic_active"):
        return lambda *_, **__: lambda: pytest.skip("No sut_dynamic is set.")

    sut_dynamic = get_sut()

    def test_mtc(sut_id: str, mr_id: MR_ID, mtc: MetamorphicTestCase):
        """
        The actual test function that is executed for each Metamorphic Test Case
        """
        mr = MetamorphicTestSuite().get_metamorphic_relation(mr_id)
        mr.sut_function_kwargs["dynamic_sut"] = sut_dynamic
        with MonkeyPatch().context() as monkeypatch:
            monkeypatch.setattr(pytest, "skip", wrong_skip_method_used)
            mr.execute_test_case(mtc, sut_id)

        if mtc.error and isinstance(mtc.error, (InvalidInputError, SkippedMTC)):
            pytest.skip(mtc.error.message)

        try:
            assert mtc.relation_result
        except AssertionError:
            pytest.fail("The Metamorphic Relation does not hold for this "
                        "Metamorphic Test Case", pytrace=False)

    def wrapper(sut_function: System) -> System:
        return sut_wrapper(sut_function, test_mtc, *mr_ids, **kwargs)

    return wrapper


def valid_input(*mr_ids: MR_ID) -> InputWrapper:
    """
    Registers a decorated function as a metamorphic valid input function for the
    metamorphic tests listed in names.

    Parameters
    ----------
    <mr1_name, mr2_name, …>:
        The names of the metamorphic relations to which this valid input function is applied.
        Please note there can be multiple names parameters separated by comma and in
        such cases the same input function is associated to different metamorphic tests.

    Returns
    -------
    Boolean:
        Valid_input returns True if the provided input is in
        the specified list of valid inputs provided.

    Example
    -------
    >>> @gmt.valid_input(<mr1_name, mr2_name, ... >)
    >>> def example_valid_input(input: Input) -> bool:
    >>>     <Specify valid inputs>
    >>>     return input in valid_inputs

    See Also
    --------
    suite:
        The object that holds all the metamorphic transformations and relations.
    transformation:
        Registers a decorated function as a transformation for a
        metamorphic relation.
    """

    # Developer Documentation

    #     Parameters
    #     ----------
    #     mr_ids : Union[TestID, List[TestID]]
    #         Name of the metamorphic relations for which the relation needs to be mapped.

    #     Returns
    #     -------
    #     wrapper : InputWrapper
    #         returns a function which would ultimately register the valid input function to
    #         suite and associate it with the metamorphic relations passed as input parameters
    #         to the decorated function with this decorator.

    #     See Also
    #     --------
    #     suite: The object that holds all the metamorphic transformations and relations.
    #     transformation: Registers a decorated function as a transformation for a
    #         metamorphic relation.

    def wrapper(valid_input_inner: Input) -> Input:
        for mr_id in mr_ids:
            MetamorphicTestSuite().get_metamorphic_relation(mr_id).valid_input.append(
                valid_input_inner)
        return valid_input_inner

    return wrapper


def randomized(arg: str, generator: MetamorphicGenerator[A]) \
        -> Union[TransformWrapper, GeneralTransformWrapper]:
    """
    Randomize the argument arg by the value generated by the generator by setting
    overriding the value of arg in the given kwargs.

    For the purpose of metamorphic testing transformations, it is recommended to
    apply this to all but the first argument.

    Parameters
    ----------
    arg : str
        The name of the argument in the transformer function to assign value to.
    generator : MetamorphicGenerator[A]
        An object of some concrete implementation of MetamorphicGenerator.

    Returns
    -------
    wrapper : Union[TransformWrapper, GeneralTransformWrapper]
        A function which will register the random generator to suite

    See Also
    --------
    fixed:
        Fix the argument arg to the given value.

    Examples
    --------
    >>> from gemtest import RandInt
    >>> import gemtest as gmt

    >>> mm_test = gmt.create_metamorphic_relation(
    >>>     "some_metamorphic_test_name", data=range(1, 10)
    >>> )

    >>> @gmt.transformation(mm_test)
    >>> @gmt.randomized('n', RandInt(1, 10))
    >>> def add(x, n):
    >>>     return x + n
    """

    def wrapper(transform: Union[Transform, GeneralTransform]) \
            -> Union[Transform, GeneralTransform]:
        return MetamorphicTestSuite().randomized_generator(transform, arg, generator)

    return wrapper


def fixed(arg: str, value: A) -> Union[TransformWrapper, GeneralTransformWrapper]:
    """
    Fix the argument arg to the given value overriding the value of arg
    in the given kwargs.

    Parameters
    ----------
    arg : str
        The name of the argument in the transformer function to assign value to.
    value : A
        Fixed value of the arg.

    Returns
    -------
    wrapper : Union[TransformWrapper, GeneralTransformWrapper]
        A function which will register the fixed value to suite and to the function
        decorated with his decorator.

    See Also
    --------
    randomized:
        Randomize the argument arg by the value generated by the generator.

    Examples
    --------
    >>> from gemtest import RandInt
    >>> import gemtest as gmt

    >>> mm_test = gmt.create_metamorphic_relation(
    >>>     "some_metamorphic_test_name", data=range(1, 10)
    >>> )

    >>> @gmt.transformation(mm_test)
    >>> @gmt.randomized('n', RandInt(1, 10))
    >>> @gmt.fixed('c', 0)
    >>> def shift(x, n, c):
    >>>     return x + 2 * n * math.pi + c
    """

    def wrapper(transform: Union[Transform, GeneralTransform]) \
            -> Union[Transform, GeneralTransform]:
        return MetamorphicTestSuite().fixed_generator(transform, arg, value)
    return wrapper
