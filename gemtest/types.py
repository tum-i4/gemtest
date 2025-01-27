from typing import Any, Callable, TypeVar, Hashable

from typing_extensions import Protocol

T_contra = TypeVar("T_contra", contravariant=True)


class Comparable(Protocol[T_contra]):
    """
    This abstract base class is used to mark that any type implementing this
    class must support the common comparison operators.

    It is used for exclusively for typing.
    """

    def __eq__(self, other: Any) -> bool:
        ...

    def __ne__(self, other: Any) -> bool:
        ...

    def __lt__(self: T_contra, other: T_contra) -> bool:
        ...

    def __gt__(self: T_contra, other: T_contra) -> bool:
        ...

    def __le__(self: T_contra, other: T_contra) -> bool:
        ...

    def __ge__(self: T_contra, other: T_contra) -> bool:
        ...


A = TypeVar('A')
"""
Common type variable.
"""

System = Callable
"""
The type of the system under test (SUT).
"""

Input = Callable[[A], bool]
"""
The general type of a valid input function.
"""

Transform = Callable[..., Any]
"""
A transformation that takes one source input and generate one follow-up input.
"""

GeneralTransform = Callable[..., Any]
"""
A transformation that can take any number of source inputs and source outputs and generates
any number of follow-up inputs.
"""

Relation = Callable[..., bool]
"""
The general type of an un-constrained relation.
"""

ComplexRelation = Callable[..., bool]
"""
The more complex type of an un-constrained relation.
"""

GeneralRelation = Callable[..., bool]
"""
The most general type of an un-constrained relation.
"""

Source_Input = TypeVar('Source_Input')
"""
Common type variable for the input of a transformation.
"""

Follow_Up_Input = TypeVar('Follow_Up_Input')
"""
Common type variable for the output of a transformation.
"""

Source_Output = TypeVar('Source_Output', bound="Comparable")
"""
Common type variable for the output of a SUT.
"""

Follow_Up_Output = TypeVar('Follow_Up_Output', bound="Comparable")
"""
Common type variable for the output of a transformation.
"""

MR_ID = Hashable
