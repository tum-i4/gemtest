from gemtest.types import Source_Output, Follow_Up_Output  # noqa


def equality(f_x: Source_Output, f_xt: Follow_Up_Output, **_kwargs) -> bool:  # noqa
    """
    Checks if the given arguments are exactly equal by delegating to
    python's built-in equality operator.

    Parameters
    -----------
    f_x : Source_Output
        The first generic argument.
    f_xt : Follow_Up_Output
        The second generic argument.

    Returns
    --------
    out : bool
        A boolean indicating if the two given arguments are exactly equal.

    Examples
    ---------
    >>> equality(1, 1) # holds
    True
    >>> equaltiy(1, 2) # does not hold
    False
    """
    return bool(f_x == f_xt)


def is_less_than(f_x: Source_Output, f_xt: Follow_Up_Output, **_kwargs) -> bool:  # noqa
    """
    Checks if the first argument is strictly less than the second argument by
    delegating to python's built-in "<"-operator.

    Parameters
    -----------
    f_x : Source_Output
        The first generic argument.
    f_xt : Follow_Up_Output
        The second generic argument.

    Returns
    --------
    out : bool
        A boolean indicating if the first argument is strictly less than the
        second argument.

    Examples
    ---------
    >>> is_less_than(1, 2) # holds
    True
    >>> is_less_than(2, 1) # does not hold
    False
    """
    return f_x < f_xt


def is_greater_than(f_x: Source_Output, f_xt: Follow_Up_Output, **_kwargs) -> bool:  # noqa
    """
    Checks if the first argument is strictly greater than the second argument by
    delegating to python's built-in ">"-operator.

    Parameters
    -----------
    f_x : Source_Output
        The first generic argument.
    f_xt : Follow_Up_Output
        The second generic argument.

    Returns
    --------
    out : bool
        A boolean indicating if the first argument is strictly greater than the
        second argument.

    Examples
    ---------
    >>> is_greater_than(2, 1) # holds
    True
    >>> is_greater_than(1, 2) # does not hold
    False
    """
    return f_x > f_xt
