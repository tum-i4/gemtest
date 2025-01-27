import copy
import os
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Tuple, Callable, Any, TYPE_CHECKING

from .metamorphic_error import MetamorphicRelationError

if TYPE_CHECKING:
    from .report.execution_report import GeneralMTCExecutionReport


class UninitializedValueClass(Enum):
    token = 0


UninitializedValue = UninitializedValueClass.token


@dataclass
class MetamorphicTestCase:
    """
    Holds one concrete metamorphic test case of a metamorphic relation. PyTests are executed on
    instances of this class.

    Parameters
    ----------
    data_loader : Callable
        A function that takes a file path as input and returns the loaded resource.
    """
    _source_inputs: List = field(default_factory=list)
    _followup_inputs: List = field(default_factory=list)
    _source_outputs: List = field(default_factory=list)
    _followup_outputs: List = field(default_factory=list)
    _parameters: Dict = field(default_factory=dict)
    _relation_result: bool = False
    _report: Optional["GeneralMTCExecutionReport"] = None
    _error: Optional[MetamorphicRelationError] = None
    data_loader: Optional[Callable] = None
    validated = False

    def process_source_inputs(self):
        """
        Processes the source inputs by loading the specified image files and replacing the
        file paths with the loaded image data. This function iterates over the source
        inputs, checks if each input is a valid file, and if so, loads the resource using
        the data_loader. The loaded resources are stored in the `source_inputs`
        attribute of the object.
        """
        if not self.data_loader:
            return

        loaded_source_inputs = []
        for source_input in self._source_inputs:
            if not isinstance(source_input, str):
                return
            if not os.path.isfile(source_input):
                return

            loaded_resource = self.data_loader(source_input)
            loaded_source_inputs.append(loaded_resource)

        self.source_inputs = loaded_source_inputs
        self.data_loader = None

    @property
    def missing_source_outputs(self):
        return sum(1 for out in self._source_outputs if out is UninitializedValue)

    @property
    def missing_followup_outputs(self):
        return sum(1 for out in self._followup_outputs if out is UninitializedValue)

    @property
    def source_inputs(self):
        self.process_source_inputs()
        return copy.deepcopy(self._source_inputs)

    @source_inputs.setter
    def source_inputs(self, value):
        if isinstance(value, List):
            self._source_inputs = value
            self._source_outputs = [UninitializedValue for _ in value]
        elif isinstance(value, Tuple):
            self._source_inputs.extend(value)
            self._source_outputs.extend(UninitializedValue for _ in value)
        else:
            self._source_inputs.append(value)
            self._source_outputs.append(UninitializedValue)

    @property
    def source_input(self):
        if len(self._source_inputs) == 1:
            return copy.deepcopy(self._source_inputs[0])
        raise ValueError('This Metamorphic Test Case has multiple source inputs use '
                         'MetamorphicTestCase.source_inputs to access them.')

    @property
    def followup_inputs(self):
        return copy.deepcopy(self._followup_inputs)

    @followup_inputs.setter
    def followup_inputs(self, value):
        if isinstance(value, List):
            self._followup_inputs = value
            self._followup_outputs = [UninitializedValue for _ in value]
        elif isinstance(value, Tuple):
            self._followup_inputs.extend(value)
            self._followup_outputs.extend(UninitializedValue for _ in value)
        else:
            self._followup_inputs.append(value)
            self._followup_outputs.append(UninitializedValue)

    @property
    def followup_input(self):
        if len(self._followup_inputs) == 1:
            return copy.deepcopy(self._followup_inputs[0])
        raise ValueError('This Metamorphic Test Case has multiple followup inputs use '
                         'MetamorphicTestCase.followup_inputs to access them.')

    @property
    def source_outputs(self):
        return copy.deepcopy(self._source_outputs)

    @source_outputs.setter
    def source_outputs(self, value):
        if isinstance(value, List):
            self._source_outputs = value
        elif isinstance(value, Tuple):
            self._source_outputs.extend(value)
        else:
            self._source_outputs.append(value)

    def source_outputs_set_at(self, index: int, value: Any):
        self._source_outputs[index] = value

    @property
    def source_output(self):
        if len(self._source_outputs) == 1:
            return copy.deepcopy(self._source_outputs[0])
        raise ValueError('This Metamorphic Test Case has multiple source outputs use '
                         'MetamorphicTestCase.source_outputs to access them.')

    @property
    def followup_outputs(self):
        return copy.deepcopy(self._followup_outputs)

    @followup_outputs.setter
    def followup_outputs(self, value):
        if isinstance(value, List):
            self._followup_outputs = value
        elif isinstance(value, Tuple):
            self._followup_outputs.extend(value)
        else:
            self._followup_outputs.append(value)

    def followup_outputs_set_at(self, index: int, value: Any):
        self._followup_outputs[index] = value

    @property
    def followup_output(self):
        if len(self._followup_outputs) == 1:
            return copy.deepcopy(self._followup_outputs[0])
        raise ValueError('This Metamorphic Test Case has multiple follow-up outputs use '
                         'MetamorphicTestCase.followup_outputs to access them.')

    @property
    def relation_result(self):
        return copy.deepcopy(self._relation_result)

    @relation_result.setter
    def relation_result(self, value):
        if isinstance(value, bool):
            self._relation_result = value
        else:
            raise ValueError("relation_result must be a bool")

    @property
    def parameters(self):
        return self._parameters.copy()

    @parameters.setter
    def parameters(self, value):
        if isinstance(value, dict):
            self._parameters = value
        else:
            raise ValueError("parameters must be a dictionary")

    @property
    def report(self):
        return self._report

    @report.setter
    def report(self, value):
        self._report = value

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        self._error = value
