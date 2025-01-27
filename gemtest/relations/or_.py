from gemtest.types import Relation, Source_Output, Follow_Up_Output


def or_(rel1: Relation, rel2: Relation, **kwargs) -> Relation:  # noqa
    """
    Construct a new relation which checks if at least one of the given
    relations holds.

    Parameters
    -----------
    rel1 : Relation
        The first relation to consider.
    rel2 : Relation
        The second relation to consider.

    Returns
    -------
    out : Relation
        A new relation checking semantically 'rel1 or rel2'.

    Examples
    ---------
    >>> is_less_than_or_equal = or_(equality, is_less_than)
    """

    def or_impl(f_x: Source_Output, f_xt: Follow_Up_Output) -> bool:
        return rel1(f_x, f_xt, **kwargs) or rel2(f_x, f_xt, **kwargs)  # noqa

    or_impl.__name__ = f'{rel1.__name__} or {rel2.__name__}'
    return or_impl
