from datetime import datetime
from typing import Callable, List

from gemtest.metamorphic_test_case import MetamorphicTestCase
from .database_handler import DatabaseHandler
from .execution_report import GeneralMTCExecutionReport


def generate_run_id():
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"metamorphic_test_run_{current_datetime}"


class ReportHandler:
    def __init__(self, max_size: int):
        self.mtc_reports: List[GeneralMTCExecutionReport] = []
        self.run_id = generate_run_id()
        self.database_handler = DatabaseHandler(self.run_id)
        self.max_size = max_size

    def add_report(self, mtc: MetamorphicTestCase,
                   input_visualizer: Callable,
                   output_visualizer: Callable):

        # apply the visualizer to the input and output.
        self._visualize_input(mtc, input_visualizer)
        self._visualize_output(mtc, output_visualizer)

        # insert report into database if max list length is reached
        self.mtc_reports.append(mtc.report)
        self.check_size()

    def _visualize_input(self, mtc: MetamorphicTestCase, input_visualizer: Callable):
        """
        Apply a visualizer function to inputs if specified for the SUT.

        Parameters
        ----------
        mtc : MetamorphicTestCase
            The metamorphic test case object.
        input_visualizer : Callable
            The input visualizer function specified for the SUT.
        """
        if not input_visualizer:
            return

        self._visualize_source_input(mtc, input_visualizer)
        self._visualize_followup_input(mtc, input_visualizer)

    def _visualize_source_input(self, mtc: MetamorphicTestCase, input_visualizer: Callable):
        """
        Try to apply a visualizer function to all source inputs. If an error occurs during
        the visualization, the original source input is used instead.
        """
        visualized_source_inputs = []
        for index, source_input in enumerate(mtc.report.source_inputs):
            try:
                visualized_source_inputs.append(
                    input_visualizer(source_input,
                                     position="source_input",
                                     index=index,
                                     run_id=self.run_id,
                                     mtc=mtc)
                )
            except Exception:
                visualized_source_inputs.append(source_input)
            finally:
                mtc.report.source_inputs = visualized_source_inputs

    def _visualize_followup_input(self, mtc: MetamorphicTestCase, input_visualizer: Callable):
        """
        Try to apply a visualizer function to all follow-up inputs. If an error occurs during
        the visualization, the original source input is used instead.
        """
        visualized_followup_inputs = []
        for index, followup_input in enumerate(mtc.report.followup_inputs):
            try:
                visualized_followup_inputs.append(
                    input_visualizer(followup_input,
                                     position="followup_input",
                                     index=index,
                                     run_id=self.run_id,
                                     mtc=mtc)
                )
            except Exception:
                visualized_followup_inputs.append(followup_input)
            finally:
                mtc.report.followup_inputs = visualized_followup_inputs

    def _visualize_output(self, mtc: MetamorphicTestCase, output_visualizer: Callable):
        """
        Apply a visualizer function to outputs if specified for the SUT.

        Parameters
        ----------
        mtc : MetamorphicTestCase
            The metamorphic test case object.
        output_visualizer : Callable
            The input visualizer function specified for the SUT.
        """
        if not output_visualizer:
            return

        self._visualize_source_output(mtc, output_visualizer)
        self._visualize_followup_output(mtc, output_visualizer)

    def _visualize_source_output(self, mtc: MetamorphicTestCase, output_visualizer: Callable):
        """
        Try to apply a visualizer function to all source outputs. If an error occurs during
        the visualization, the original source output is used instead.
        """
        visualized_source_outputs = []
        for index, (source_output, source_input) \
                in enumerate(zip(mtc.source_outputs, mtc.source_inputs)):
            try:
                visualized_source_outputs.append(
                    output_visualizer(
                        source_output,
                        position="source_output",
                        sut_input=source_input,
                        index=index,
                        run_id=self.run_id,
                        mtc=mtc
                    )
                )
            except Exception:
                visualized_source_outputs.append(source_output)
            finally:
                mtc.report.source_outputs = visualized_source_outputs

    def _visualize_followup_output(self, mtc: MetamorphicTestCase,
                                   output_visualizer: Callable):
        """
        Try to apply a visualizer function to all follow-up outputs. If an error occurs during
        the visualization, the original follow-up output is used instead.
        """
        visualized_followup_outputs = []
        for index, (followup_output, followup_input) \
                in enumerate(zip(mtc.followup_outputs, mtc.followup_inputs)):
            try:
                visualized_followup_outputs.append(
                    output_visualizer(
                        followup_output,
                        position="followup_output",
                        sut_input=followup_input,
                        index=index,
                        run_id=self.run_id,
                        mtc=mtc
                    )
                )
            except Exception:
                visualized_followup_outputs.append(followup_output)
            finally:
                mtc.report.followup_outputs = visualized_followup_outputs

    def check_size(self):
        if len(self.mtc_reports) == self.max_size:
            # save reports in database and clear report list
            self.save()
            self.mtc_reports.clear()

    def save(self):
        self.database_handler.insert(self.mtc_reports)

    def close(self):
        self.database_handler.close()
