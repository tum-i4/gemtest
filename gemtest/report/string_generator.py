import math

from .execution_report import GeneralMTCExecutionReport


def shorten(value, length=25):
    value = str(value)
    if len(value) > length:
        return value[:length] + "..."
    return value


class StringReportGenerator:
    """
            ___________________________________________________________________
            |                                                                 |
            |   source input[0]     ------ sut ----->      source output[0]   |
            |   source input[1]     ------ sut ----->      source output[1]   |
            |   source input[n]     ------ sut ----->      source output[n]   |
            |   |                                                         |   |
            |   | (transformation name)                                   |   |
            |   |                                                         |   |
            |   followup input[0]   ------ sut ----->      followup output[0] |
            |   followup input[1]   ------ sut ----->      followup output[1] |
            |   followup input[m]   ------ sut ----->      followup output[m] |
            |_________________________________________________________________|
                |-------------->   relation name: True   <----------------|
        """

    report: GeneralMTCExecutionReport

    def __init__(self, report: GeneralMTCExecutionReport):
        self.report = report

    def generate(self) -> str:

        output_lines = []

        # header
        # box width: 4 + 28 + 8 + shorten(sut) + 8 + 28 + 4
        width = 80 + len(shorten(self.report.sut_name))

        # parameters
        if self.report.parameters:
            params_string = f"parameters: {str(self.report.parameters)}"
            params_width = len(params_string)
            if params_width > width:
                output_lines.append(shorten(params_string, width))
            else:
                space_side = math.ceil((width - params_width) / 2)
                output_lines.append(" " * space_side + params_string)

        output_lines.append("-" * width)
        output_lines.append("|" + " " * (width - 2) + "|")

        # source input - sut - source output
        for source_input, source_output in zip(self.report.source_inputs,
                                               self.report.source_outputs):
            output_lines.append("|   "
                                + shorten(source_input)
                                + " " * (28 - len(shorten(source_input)))
                                + " ------ "
                                + shorten(self.report.sut_name)
                                + " -----> "
                                + " " * (28 - len(shorten(source_output)))
                                + shorten(source_output)
                                + "   |")

        # transformation
        output_lines.append("|   |" + " " * (width - 10) + "|   |")
        output_lines.append("|   | "
                            + shorten(self.report.transformation_name)
                            + " "
                            * (width - 11 - len(shorten(self.report.transformation_name)))
                            + "|   |")
        output_lines.append("|   |" + " " * (width - 10) + "|   |")

        # source input - sut - source output
        for followup_input, followup_output in zip(self.report.followup_inputs,
                                                   self.report.followup_outputs):
            output_lines.append("|   "
                                + shorten(followup_input)
                                + " " * (28 - len(shorten(followup_input)))
                                + " ------ "
                                + shorten(self.report.sut_name)
                                + " -----> "
                                + " " * (28 - len(shorten(followup_output)))
                                + shorten(followup_output)
                                + "   |")

        # footer
        output_lines.append("|" + " " * (width - 2) + "|")
        output_lines.append("-" * width)

        # relation
        # center relation result on "------ sut ----->"
        sut_width = 16 + len(shorten(self.report.sut_name))
        relation_width = len(shorten(self.report.relation_name)) + len(
            str(self.report.relation_result)) + 1

        # this won't work if the relation_width > sut_width
        num_spaces = sut_width - relation_width
        num_left_spaces = num_spaces // 2
        num_right_spaces = num_spaces - num_left_spaces

        output_lines.append("    "
                            + "|" + "-" * 25 + "> "
                            + " " * num_left_spaces
                            + shorten(self.report.relation_name)
                            + ": " + str(self.report.relation_result)
                            + " " * num_right_spaces
                            + " <" + "-" * 25 + "|")

        return "\n".join(output_lines)
