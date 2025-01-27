import random

from gemtest.generator import MetamorphicGenerator


class RandFloat(MetamorphicGenerator[float]):
    """
    This is a custom random floating point number generator.
    """

    def __init__(self, min_value: float, max_value: float):
        self.min_value = min_value
        """
        min_value : float
            Minimum value of the range.
        """
        self.max_value = max_value
        """
        max_value : float
            Maximum value of the range.
        """

    def generate(self) -> float:
        """
        Returns a random floating point value from the closed interval
        [self.min_value, self.max_value].
        """
        return random.uniform(self.min_value, self.max_value)  # nosec
