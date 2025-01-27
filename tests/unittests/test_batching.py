from gemtest.metamorphic_error import SUTExecutionError
from gemtest.metamorphic_relation import MetamorphicRelation, InvalidInputError
from gemtest.metamorphic_test_case import MetamorphicTestCase, UninitializedValue
from gemtest.testcase_queue import InputQueueItem, InputQueue
from gemtest.testing_strategy import TestingStrategy
import pytest

def test_testcase_source_setter():
    mtc = MetamorphicTestCase()
    mtc.source_inputs = 1

    assert len(mtc.source_outputs) == 1
    assert mtc.source_output is UninitializedValue


def test_input_queue_item():
    mtc1 = MetamorphicTestCase()
    mtc1.source_inputs = 1

    item = InputQueueItem(mtc1, 0, is_source=True)
    assert item.get_input() == 1

    item.set_output(42)
    assert mtc1.source_output == 42


def test_input_queue():
    class NotComparable:
        def __eq__(self, other):
            raise NotImplementedError()

    mtc1 = MetamorphicTestCase()
    mtc1.source_inputs = NotComparable()

    mtc2 = MetamorphicTestCase()
    mtc2.source_inputs = NotComparable()

    q = InputQueue([
        InputQueueItem(mtc1, 0, is_source=True),
        InputQueueItem(mtc2, 0, is_source=False),
    ])

    r = q.get_all_with_testcase(mtc1, is_source=False)
    assert len(r) == 0
    assert len(q) == 2

    r = q.get_all_with_testcase(mtc1, is_source=True)
    assert len(r) == 1
    assert len(q) == 1
    assert r[0].test_case is mtc1


def test_input_queue_max_len():
    mtc1 = MetamorphicTestCase()

    q = InputQueue(InputQueueItem(mtc1, i, is_source=True) for i in range(10))
    r = q.get_all_with_testcase(mtc1, is_source=True, max_items=3)
    assert len(r) == 3


def dummy_transform(x):
    return x


def _create_test_cases(count: int):
    test_cases = [MetamorphicTestCase() for _ in range(count)]
    for i, mtc in enumerate(test_cases):
        mtc.source_inputs = i
    return test_cases


def test_sut_batching():
    acc = []

    def sut_function(batch):
        assert isinstance(batch, list)
        acc.append(batch)
        return batch

    test_cases = _create_test_cases(64)

    mr = MetamorphicRelation(mr_id="mr1",
                             data=range(64),
                             testing_strategy=TestingStrategy.EXHAUSTIVE,
                             number_of_test_cases=1,
                             number_of_sources=1)

    mr.q_ready[sut_function.__name__] = InputQueue(
        InputQueueItem(mtc, i, is_source=True)
        for mtc in test_cases
        for i, _ in enumerate(mtc.source_inputs)
    )
    mr.transform = dummy_transform
    mr.system_under_test = sut_function
    mr.sut_batch_size[sut_function.__name__] = 16

    mr.create_source_outputs(test_cases[0], sut_function.__name__)

    assert all(mtc.error is None for mtc in test_cases)
    assert len(acc) == 1
    assert all(len(batch) == 16 for batch in acc)
    assert all(test_cases[i].missing_source_outputs == 0 for i in range(16))
    assert all(len(test_cases[i].followup_inputs) == 1 for i in range(16))

    # Nothing should happen here, this was included in the last batch
    mr.create_source_outputs(test_cases[1], sut_function.__name__)
    assert len(acc) == 1

    mr.create_source_outputs(test_cases[16], sut_function.__name__)
    assert len(acc) == 2
    assert all(len(batch) == 16 for batch in acc)


def test_sut_batching_error_propagation():
    """
    This function tests the propagation of errors when the System Under Test (SUT) raises an exception during batch processing.

    The sut_function is purposely designed to take a batch input and throw an error.

    We initialize a Metamorphic Relation (MR) and populate the Queue for the SUT Function with three test cases.
    These Test cases will be processed by the MR.

    Next, we configure the Transformation function, the sut function and the batch size (batch_size = 2) for the MR.

    We run the `create_source_outputs` function of the MR, which essentially applies the SUT to the first two source inputs.
    Given the sut_function throwing an Error that ends the Test Suite, we catch this SystemExit and verify the Errors for test cases 0 and 1.

    Given that the batch size is two and we executed the SUT only on the first and second test cases, we also verified that there is no error
    assigned to the third test case.
    """
    def sut_function(batch):
        raise ValueError()

    test_cases = _create_test_cases(3)

    mr = MetamorphicRelation(mr_id="mr1",
                             data=range(64),
                             testing_strategy=TestingStrategy.EXHAUSTIVE,
                             number_of_test_cases=1,
                             number_of_sources=1)

    mr.q_ready[sut_function.__name__] = InputQueue((
        InputQueueItem(test_cases[0], 0, is_source=True),
        InputQueueItem(test_cases[1], 0, is_source=True),
        InputQueueItem(test_cases[2], 0, is_source=True),
    ))

    mr.transform = dummy_transform
    mr.system_under_test = sut_function
    mr.sut_batch_size[sut_function.__name__] = 2

    # Handle SystemExit when Error is thrown
    with pytest.raises(SystemExit) as exc_info:
        mr.create_source_outputs(test_cases[0], sut_function.__name__)

    # Retrieve the Error that caused the SystemExit
    sut_error = exc_info.value.args[0]

    assert isinstance(sut_error, SUTExecutionError)

    assert isinstance(test_cases[0].error, SUTExecutionError)
    assert isinstance(test_cases[1].error, SUTExecutionError)

    assert isinstance(test_cases[0].error.original_exception, ValueError)
    assert isinstance(test_cases[1].error.original_exception, ValueError)

    assert test_cases[2].error is None


def test_sut_batching_validation():
    def validate(x):
        return x != 1

    def sut_function(batch):
        return batch

    test_cases = _create_test_cases(3)

    mr = MetamorphicRelation(mr_id="mr1",
                             data=range(64),
                             testing_strategy=TestingStrategy.EXHAUSTIVE,
                             number_of_test_cases=1,
                             number_of_sources=1)

    mr.q_ready[sut_function.__name__] = InputQueue(
        InputQueueItem(mtc, i, is_source=True)
        for mtc in test_cases
        for i, _ in enumerate(mtc.source_inputs)
    )

    mr.valid_input = [validate]
    mr.transform = dummy_transform
    mr.system_under_test = sut_function
    mr.sut_batch_size[sut_function.__name__] = 16

    mr.create_source_outputs(test_cases[0], sut_function.__name__)

    assert test_cases[0].error is None
    assert isinstance(test_cases[1].error, InvalidInputError)
    assert test_cases[2].error is None
