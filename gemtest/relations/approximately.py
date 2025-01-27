import pytest

from gemtest.types import Source_Output, Follow_Up_Output


def approximately(f_x: Source_Output, f_xt: Follow_Up_Output,  # noqa
                  relative: float = None, absolute: float = None,
                  **_kwargs) -> bool:
    """
    Checks if the given arguments are approximately equal by delegating to
    pytest.approx.

    Parameters
    -----------
    f_x : Source_Output
        The first generic argument.
    f_xt : Follow_Up_Output
        The second generic argument.
    relative: float
        Relative error between x and y.
    absolute: float
        Absolute error between x and y.

    Returns
    --------
    out : bool
        A boolean indicating if the two given arguments are approximately equal.

    Examples
    ---------
    >>> import math

    >>> approximately(math.pi, 3.1315926536) # holds
    >>> approximately(math.pi, 3.13) # does not hold
    """
    return f_x == pytest.approx(f_xt, rel=relative, abs=absolute)
