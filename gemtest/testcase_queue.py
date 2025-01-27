from collections import deque
from typing import List

from .metamorphic_test_case import MetamorphicTestCase


class InputQueueItem:
    def __init__(self, test_case: MetamorphicTestCase, index: int, is_source: bool):
        self.test_case = test_case
        self.index = index
        self.is_source = is_source

    def get_input(self):
        if self.is_source:
            return self.test_case.source_inputs[self.index]
        return self.test_case.followup_inputs[self.index]

    def set_output(self, value):
        if self.is_source:
            self.test_case.source_outputs_set_at(self.index, value)
        else:
            self.test_case.followup_outputs_set_at(self.index, value)


class InputQueue(deque):
    def get_all_with_testcase(
            self,
            mtc: MetamorphicTestCase,
            is_source: bool,
            max_items: int = -1,
    ) -> List[InputQueueItem]:
        acc = []

        for item in self:
            if item.test_case is mtc and item.is_source == is_source:
                acc.append(item)

            if max_items == len(acc):
                break

        for item in acc:
            self.remove(item)

        return acc
