import copy
import math
import random
from dataclasses import dataclass, field
from itertools import product, combinations
from typing import List, Dict, Optional, Sequence, Any

from .logger import logger
from .metamorphic_error import MetamorphicRelationError, SUTExecutionError, \
    TransformationError, RelationError, InvalidInputError, SkippedMTC
from .metamorphic_test_case import MetamorphicTestCase, UninitializedValue
from .report.execution_report import GeneralMTCExecutionReport
from .testcase_queue import InputQueue, InputQueueItem
from .testing_strategy import TestingStrategy
from .types import Input, Transform, GeneralTransform, Relation, GeneralRelation, MR_ID


@dataclass
class MetamorphicRelation:
    """
    Holds a single metamorphic relation object and provides
    the functionality to create metamorphic test cases and execute them.
    """
    mr_id: MR_ID
    data: Sequence
    testing_strategy: str
    number_of_test_cases: int
    number_of_sources: int
    _system_under_test: Dict = field(default_factory=dict)
    _transform: Optional[Transform] = None
    _general_transform: Optional[GeneralTransform] = None
    _relation: Optional[Relation] = None
    _general_relation: Optional[GeneralRelation] = None
    mtc_templates: List[MetamorphicTestCase] = field(default_factory=list)
    test_cases: Dict = field(default_factory=dict)
    valid_input: List[Input] = field(default_factory=list)
    sut_parameters: Dict = field(default_factory=dict)
    sut_function_kwargs: Dict = field(default_factory=dict)

    sut_batch_size: Dict = field(default_factory=dict)
    """ Mapping between a sut_id and it's batch size """
    q_ready: Dict[str, InputQueue] = field(default_factory=dict)
    """ Queue for each SUT containing testcase inputs that are ready to be processed """

    def create_parameter_permutations(self) -> List[Dict[str, Any]]:
        """
        Create all possible parameter permutations from a dictionary
        of parameters and their possible values. Returns [{}] if no parameters are passed
        to the sut.

        Returns
        -------
        permutations : List[Dict[str, Any]]:
            A list of dictionaries representing all possible parameter permutations.
        """
        param_names = list(self.sut_parameters.keys())
        param_values = list(self.sut_parameters.values())
        param_combinations = product(*param_values)
        permutations = [dict(zip(param_names, combination)) for combination in
                        param_combinations]
        return permutations

    def generate_test_cases(self) -> None:
        """
        Generates metamorphic test cases for the metamorphic relation. Raises a ValueError
        if the number of test cases requested is larger than the number of elements
        in the provided data, if the provided data is empty, if the number of test cases
        requested is less than or equal to 0, or if the number of sources requested is
        less than or equal to 0.
        """
        if not self.data:
            raise ValueError(f"The provided data for {self.mr_id} is empty")
        if self.number_of_test_cases > self._calculate_possible_sources():
            raise ValueError(f"You want to run more test cases for {self.mr_id} than there "
                             f"are elements in the provided data")
        if self.number_of_test_cases <= 0:
            raise ValueError(f"Number of test cases for {self.mr_id} must be at least 1")
        if self.number_of_sources <= 0:
            raise ValueError(f"Number of sources for {self.mr_id} must be at least 1")
        if self.number_of_sources > len(self.data):
            raise ValueError(f"Number of sources for {self.mr_id} is larger than the number "
                             f"of elements in the provided dataset")

        parameter_permutations = self.create_parameter_permutations()

        if self.testing_strategy is TestingStrategy.SAMPLE:
            # create a specified number of sample MTCs from the provided data.
            for _ in range(self.number_of_test_cases):
                source_input = random.sample(self.data, self.number_of_sources)
                for parameter_permutation in parameter_permutations:
                    mtc = MetamorphicTestCase()
                    mtc.source_inputs = source_input
                    mtc.parameters = parameter_permutation
                    self.mtc_templates.append(mtc)

        elif self.testing_strategy is TestingStrategy.EXHAUSTIVE:
            # create an MTC for all possible n-tuples from the provided data.
            source_inputs = [list(x) for x in combinations(self.data, self.number_of_sources)]
            for source_input in source_inputs:
                for parameter_permutation in parameter_permutations:
                    mtc = MetamorphicTestCase()
                    mtc.source_inputs = source_input
                    mtc.parameters = parameter_permutation
                    self.mtc_templates.append(mtc)

    def _calculate_possible_sources(self) -> float:
        """
        Calculate `C(n, r) = n! / (r! * (n - r)!)` with n as the number of elements in the
        data and r as the number of sources.

        Returns
        -------
        float
            The number of possible sources.
        """
        n = len(self.data)
        r = self.number_of_sources
        if r == 1:
            return n
        return math.factorial(n) / (math.factorial(r) * math.factorial(n - r))

    def check_valid_input(self, test_case: MetamorphicTestCase):
        """
        Tests if at least one of the valid_input functions evaluates to true for
        all source_outputs of the MTC. If not, this MTC is skipped.
        """
        if test_case.validated or test_case.error:
            return

        assert all(x is not UninitializedValue for x in test_case.source_outputs)
        test_case.validated = True

        if len(self.valid_input) == 0:
            return

        valid_function_found = False
        for fun in self.valid_input:
            all_outputs_valid = True
            for source_output in test_case.source_outputs:
                all_outputs_valid = all_outputs_valid and fun(source_output)
            valid_function_found = valid_function_found or all_outputs_valid

        valid_input_function_names = [fun.__name__ for fun in self.valid_input]

        if not valid_function_found:
            invalid_input_error = InvalidInputError(
                f"An error occurred on metamorphic relation {self.mr_id}. "
                f"The input of the current metamorphic test case is not valid. "
                f"source inputs: {test_case.source_inputs}, "
                f"source outputs: {test_case.source_outputs}. "
                f"The input must satisfy (at least) one of the condition(s) "
                f"set in the valid input function(s): "
                f'{", ".join(valid_input_function_names)}'
            )
            test_case.error = invalid_input_error

    def run_sut_batches(self, test_case: MetamorphicTestCase, sut_id: str, is_source: bool):
        batch_size = self.sut_batch_size[sut_id] if self.sut_batch_size[sut_id] else 1

        q = self.q_ready[sut_id]
        ran_items = []

        while batch := q.get_all_with_testcase(test_case, is_source, batch_size):
            while len(q) and len(batch) < batch_size:
                batch.append(q.popleft())

            try:
                if self.sut_batch_size[sut_id]:
                    assert not any(pa.test_case.parameters for pa in batch)
                    input_batch = [pa.get_input() for pa in batch]
                    sut_kwargs = self.sut_function_kwargs
                    results = self.system_under_test[sut_id](input_batch, **sut_kwargs)
                else:
                    input_batch = batch[0].get_input()
                    sut_kwargs = self.sut_function_kwargs
                    results = [self.system_under_test[sut_id](input_batch, **sut_kwargs)]

                for queue_item, result in zip(batch, results):
                    queue_item.set_output(value=result)

                ran_items.extend(batch)

            # Check specifically for a TypeError and add informative Error Message
            except TypeError as e:
                sut_error = SUTExecutionError(
                    f"A TypeError occurred on metamorphic relation {self.mr_id} "
                    f"while applying the system under test {sut_id} to the source input. "
                    f"Potential Issue: The SUT expects a different input type! "
                    f"Ensure that the @gmt.system_under_test() "
                    f"arguments are correctly used, "
                    f"and that the transformation {self.transform.__name__} "
                    f"returns the correct type! "
                    f"Original error message: {e}"
                )
                for queue_item in batch:
                    queue_item.test_case.error = sut_error
                raise SystemExit(sut_error) from e

            except Exception as e:
                sut_error = SUTExecutionError(
                    f"An error occurred on metamorphic relation"
                    f" {self.mr_id} while applying the system under "
                    f"test {sut_id} to the source input. Original "
                    f"error message: {e}",
                    e,
                )

                for queue_item in batch:
                    queue_item.test_case.error = sut_error
                raise SystemExit(sut_error) from e

        for queue_item in ran_items:
            if queue_item.test_case.missing_source_outputs > 0:
                continue
            self.check_valid_input(queue_item.test_case)
            self.apply_transformation(queue_item.test_case, sut_id)

    def create_source_outputs(self, test_case: MetamorphicTestCase, sut_id: str):
        """
        Executes the system under test for the given source inputs of the metamorphic test
        case and registers the source outputs.
        """
        if test_case.missing_source_outputs == 0:
            return

        try:
            self.run_sut_batches(test_case, sut_id, is_source=True)
        except Exception as e:
            sut_error = SUTExecutionError(
                f"An error occurred on metamorphic relation"
                f" {self.mr_id} while applying the system under "
                f"test {sut_id} to the source input. Original "
                f"error message: {e}",
                e,
            )
            test_case.error = sut_error
            raise SystemExit(sut_error) from e

    def create_followup_outputs(self, test_case: MetamorphicTestCase, sut_id: str):
        """
        Executes the system under test for the given followup inputs of the metamorphic test
        case and registers the followup outputs.
        """
        if test_case.error or test_case.missing_followup_outputs == 0:
            return

        try:
            self.run_sut_batches(test_case, sut_id, is_source=False)
        except Exception as e:
            sut_error = SUTExecutionError(
                f"An error occurred on metamorphic relation"
                f" {self.mr_id} while applying the system under "
                f"test {sut_id} to the follow-up input. Original "
                f"error message: {e}",
                e,
            )
            test_case.error = sut_error
            raise SystemExit(sut_error) from e

    @staticmethod
    def is_wrapped_result(result):
        """
        Verifies whether the passed transformation/relation
        result is a triplet of parameterized form.
        """
        return (
            isinstance(result, tuple)
            and len(result) == 3
            and isinstance(result[2], bool)
        )

    def _unpack_result(self, result):
        """
        Recursively unpack the result to get the most inner triplet.
        Enables us to handle any amount of parameters set in randomized and fixed decorators.
        The result will be of form (value, dict, is_parameterized).
        When using multiple parameters the value will be another triplet,
        where the most inner dict is carrying all parameters!
        """
        if not self.is_wrapped_result(result):
            return result

        transformation_result, _, _ = result

        if not self.is_wrapped_result(transformation_result):
            return result

        return self._unpack_result(transformation_result)

    def _update_transformation_results(self, test_case: MetamorphicTestCase, result):
        """
        Updates the test_case followup_inputs and transformation_args,
        based on the result provided by the Transformation function.
        Extracts the followup inputs and transformation args depending on parameterization
        using fixed, randomized or both decorators.
        """
        if test_case.parameters is None:
            test_case.parameters = {}

        # Unpack the result to get the most inner triplet
        unpacked_result = self._unpack_result(result)

        if not self.is_wrapped_result(unpacked_result):
            test_case.followup_inputs = unpacked_result
            return

        transformation_result, transformation_args, is_parameterized = unpacked_result

        test_case.followup_inputs = transformation_result

        if not is_parameterized:
            return

        # Handle the case where is_parameterized is True
        duplicate_keys = set(test_case.parameters).intersection(transformation_args)

        if duplicate_keys:
            raise SystemExit(
                f"Duplicate keys found in transformation_args: {duplicate_keys}. "
                f"Please rename one of the duplicate parameters. "
                f"Metamorphic relation affected: {self.mr_id}"
            )

        # Create a new dictionary that combines both
        combined_parameters = {**test_case.parameters, **transformation_args}
        test_case.parameters = combined_parameters

    def apply_transformation(self, test_case: MetamorphicTestCase, sut_id: str = ""):
        """
        Executes the (general) transformation for the given source inputs of the metamorphic
        test case and registers the followup inputs.
        If sut_id is supplied, the followup_inputs are added to the processing queue
        of that system under test.
        """
        if test_case.error or test_case.followup_inputs:
            return

        if not (self.transform or self.general_transform):
            raise ValueError(f"No transformation registered on MR: {self.mr_id}")
        if self.transform and len(test_case.source_inputs) != 1:
            raise ValueError(f"Can only use @transformation for a 1 to 1 transformation "
                             f"on MR: {self.mr_id}")
        if self.transform and self.sut_parameters:
            raise ValueError(f"Can't add parameters for SUT when using @transformation "
                             f"on MR: {self.mr_id}")

        try:
            if self.transform:
                result = self.transform(test_case.source_input)  # noqa
                self._update_transformation_results(test_case, result)

            if self.general_transform:
                result = self.general_transform(test_case)  # noqa
                self._update_transformation_results(test_case, result)

            if sut_id:
                for i, _ in enumerate(test_case.followup_inputs):
                    self.q_ready[sut_id].append(InputQueueItem(test_case, i, is_source=False))
        except SkippedMTC as e:
            test_case.error = e
        except Exception as e:
            test_case.error = TransformationError(
                f"An error occurred on metamorphic "
                f"relation {self.mr_id} while applying "
                f"the transformation "
                f"{self.transform.__name__}. "
                f"Original error message: {e}",
                e,
            )
            raise SystemExit(test_case.error) from e

    def _update_relation_result(self, test_case: MetamorphicTestCase, result):
        """
        Updates the test_case.relation_result based on the result
        provided by the Relation function.
        Extracts the test results depending on parameterization using
        fixed, randomized or both decorators.
        """
        # Unpack the result to get the most inner triplet
        unpacked_result = self._unpack_result(result)

        # Update relation_result based on whether unpacked_result is a parameterized triplet
        if not self.is_wrapped_result(unpacked_result):
            test_case.relation_result = unpacked_result
        else:
            test_case.relation_result = unpacked_result[0]

    def apply_relation(self, test_case: MetamorphicTestCase):
        """
        Executes the (general) relation for the given metamorphic test case and registers the
        relation result.
        """
        if test_case.error:
            return

        if not (self.relation or self.general_relation):
            raise ValueError(f"No relation registered on MR: {self.mr_id}")
        if self.relation and len(test_case.source_outputs) != 1:
            raise ValueError(f"Can only use @relation for a single source output "
                             f"on MR: {self.mr_id}")
        if self.relation and len(test_case.followup_outputs) != 1:
            raise ValueError(f"Can only use @relation for a single followup output "
                             f"on MR: {self.mr_id}")
        if self.relation and self.sut_parameters:
            raise ValueError(f"Can't add parameters for SUT when using @relation "
                             f"on MR: {self.mr_id}")

        try:
            if self.relation:
                relation_result = self.relation(  # noqa
                    test_case.source_outputs[0],
                    test_case.followup_outputs[0]
                )

                self._update_relation_result(test_case, relation_result)

            if self.general_relation:
                result = self.general_relation(test_case)  # noqa
                self._update_relation_result(test_case, result)

        except Exception as e:
            relation_error = RelationError(f'An error occurred on metamorphic relation'
                                           f' {self.mr_id} while applying the relation. '
                                           f'Original error message: {e}')
            test_case.error = relation_error
            raise SystemExit(relation_error) from e

    def create_execution_report(self, test_case: MetamorphicTestCase) \
            -> GeneralMTCExecutionReport:
        """
        Creates an execution report that contains the information for a string or html
        report.
        """
        try:
            execution_report = GeneralMTCExecutionReport()
            execution_report.source_inputs = test_case.source_inputs
            execution_report.followup_inputs = test_case.followup_inputs
            execution_report.source_outputs = test_case.source_outputs
            execution_report.followup_outputs = test_case.followup_outputs
            execution_report.relation_result = test_case.relation_result
            execution_report.transformation_name = self.transform.__name__ if self.transform \
                else self.general_transform.__name__
            execution_report.relation_name = self.relation.__name__ if self.relation \
                else self.general_relation.__name__
            execution_report.parameters = test_case.parameters
        except Exception as e:
            execution_report_error = SUTExecutionError(
                f"An error occurred while creating the execution report. "
                f"Original Error Message: {e}"
            )
            raise SystemExit(execution_report_error) from e
        return execution_report

    def execute_test_case(self, mtc: MetamorphicTestCase, sut_id: str):
        """
        Executes a metamorphic test case.
        """
        try:
            self.create_source_outputs(mtc, sut_id)
            self.create_followup_outputs(mtc, sut_id)
            self.apply_relation(mtc)

            if mtc.error:
                raise mtc.error from mtc.error.original_exception
        except InvalidInputError as e:
            logger.info(e)
        except MetamorphicRelationError as e:
            logger.error(e)
        finally:
            mtc.report = self.create_execution_report(mtc)

    @property
    def system_under_test(self):
        return self._system_under_test

    @system_under_test.setter
    def system_under_test(self, sut_function):
        # set the system under test function
        sut_id = sut_function.__name__
        if sut_id in self._system_under_test:
            raise ValueError(f"System under test {sut_id} has already been set for "
                             f"metamorphic relation {self.mr_id}.")
        self._system_under_test[sut_id] = sut_function

        # create a copy of the mtc_templates for the newly added sut
        self.test_cases[sut_id] = copy.deepcopy(self.mtc_templates)

    @property
    def transform(self):
        return self._transform

    @transform.setter
    def transform(self, value):
        if self._transform is not None:
            raise ValueError(f"Transform has already been set "
                             f"on metamorphic relation {self.mr_id}")
        if self._general_transform is not None:
            raise ValueError(f"Cannot set transform when general_transform is already set "
                             f"on metamorphic relation {self.mr_id}.")
        self._transform = value

    @property
    def general_transform(self):
        return self._general_transform

    @general_transform.setter
    def general_transform(self, value):
        if self._general_transform is not None:
            raise ValueError(f"General transform has already been set "
                             f"on metamorphic relation {self.mr_id}.")
        if self._transform is not None:
            raise ValueError(f"Cannot set general_transform when transform is already set on "
                             f"metamorphic relation {self.mr_id}.")
        self._general_transform = value

    @property
    def relation(self):
        return self._relation

    @relation.setter
    def relation(self, value):
        if self._relation is not None:
            raise ValueError(f"Relation  has already been set on "
                             f"metamorphic relation {self.mr_id}.")
        if self._general_relation is not None:
            raise ValueError(f"Cannot set relation when general_relation is already set on "
                             f"metamorphic relation {self.mr_id}.")
        self._relation = value

    @property
    def general_relation(self):
        return self._general_relation

    @general_relation.setter
    def general_relation(self, value):
        if self._general_relation is not None:
            raise ValueError(f"General relation has already been set on "
                             f"metamorphic relation {self.mr_id}.")
        if self._relation is not None:
            raise ValueError(f"Cannot set general_relation when relation is already set "
                             f"on metamorphic relation {self.mr_id}.")
        self._general_relation = value
