import inspect
from functools import wraps
from pathlib import Path
from typing import Dict, Union, TypeVar, Sequence

from .generator import MetamorphicGenerator
from .metamorphic_relation import MetamorphicRelation
from .types import Transform, GeneralTransform, MR_ID

A = TypeVar('A')
METAMORPHIC_TEST_PACKAGE_PATH = Path(__file__).parent


class MetamorphicTestSuite:
    """
    A singleton class that holds all created metamorphic relations.
    """

    _metamorphic_relations: Dict[MR_ID, MetamorphicRelation]

    def __new__(cls):
        """
        Creates a singleton metamorphic test suite object, if it is
        not created, or else returns the previous singleton object.

        metamorphic_relations : Dict[MR_ID, MetamorphicRelation]
            A dictionary with keys as MR_ID and values as metamorphic relation
            to hold all the metamorphic relations within a single data structure.
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(MetamorphicTestSuite, cls).__new__(cls)
            cls.instance._metamorphic_relations: Dict[MR_ID, MetamorphicRelation] = {}
        return cls.instance

    def get_metamorphic_relations(self) -> Dict[MR_ID, MetamorphicRelation]:
        """
        A getter method for getting the dict of metamorphic relations registered
        in this metamorphic test suite singleton object.

        Returns
        -------
        self._metamorphic_relations : Dict[MR_ID, MetamorphicRelation]
            The dict of metamorphic relations.
        """
        return self._metamorphic_relations

    def get_metamorphic_relation(self, mr_id: MR_ID) -> MetamorphicRelation:
        """
        A method to create a new metamorphic relation and add it to the test suite.

        Parameters
        ----------
        mr_id : MR_ID
            The id of the metamorphic relation.

        Returns
        -------
        metamorphic_relation : MetamorphicRelation
            The metamorphic relation object with key=mr_id.

        See Also
        --------
        MetamorphicRelation : Object that holds a metamorphic relation.
        """
        return self._metamorphic_relations[mr_id]

    @staticmethod
    def get_caller_module() -> str:
        """
        A static method for getting the name of a test module.

        Returns
        -------
        module.__name__ : str
            the module name where the test is created.
        """
        # inspect.stack() returns a list of frame records for the caller's stack.
        # The first entry in the returned list represents the caller.
        for frame in inspect.stack():
            test_module_path = Path(frame[1])
            if METAMORPHIC_TEST_PACKAGE_PATH not in test_module_path.parents:
                module = inspect.getmodule(frame[0])
                if module is not None:
                    return module.__name__
        raise ValueError('Internal Error: no calling module found.')

    def add_metamorphic_relation(self,  # noqa - to many arguments
                                 name: str,
                                 data: Sequence,
                                 testing_strategy: str,
                                 number_of_test_cases: int,
                                 number_of_sources: int
                                 ) -> MR_ID:
        """
        A method to create a new metamorphic relation and add it to the test suite.

        Parameters
        ----------
        name : str
            The name of the metamorphic relation.
        data : Sequence
            The datasource from which sample source are sampled for metamorphic test cases
            of the metamorphic relation.
        testing_strategy: str
            Strategy for creating metamorphic test cases.
        number_of_test_cases : int
            The number of metamorphic test cases that should be created and executed for
            this metamorphic relation.
        number_of_sources : int
            The number of source inputs used for the general transformation.

        Returns
        -------
        name : MR_ID
            The name of the metamorphic relation used as a unique identifier for
            metamorphic relations in a metamorphic test suite.

        See Also
        --------
        MetamorphicRelation : Object that holds a metamorphic relation.
        """
        module = self.get_caller_module()
        metamorphic_relation_id = f"{module}.{name}"
        if metamorphic_relation_id in self.get_metamorphic_relations():
            raise ValueError(f"Metamorphic Relation with with ID: {metamorphic_relation_id} "
                             f"already exists.")

        # create the metamorphic relation and add it to the suite
        self._metamorphic_relations[metamorphic_relation_id] = MetamorphicRelation(
            mr_id=metamorphic_relation_id,
            data=data,
            testing_strategy=testing_strategy,
            number_of_test_cases=number_of_test_cases,
            number_of_sources=number_of_sources
        )

        return metamorphic_relation_id

    @staticmethod
    def fixed_generator(transformation: Union[Transform, GeneralTransform], arg: str,
                        value: A) -> Union[Transform, GeneralTransform]:
        """
        This method is internally called by decorator.fixed() to register a fixed
        generator to a transformation.

        Parameters
        ----------
        transformation : Union[Transform, GeneralTransform]
            The transformation to which the fixed_generator needs to be associated
            to always get a fixed value for an argument to the transformation.

        arg : str
            Name of the argument which needs to be supplied with a fixed value while
            performing transformation.

        value : A
            Fixed value for the argument arg.

        Returns
        -------
        wrapper : Union[Transform, GeneralTransform]
            A function which modifies the original transformation function by setting a
            given fixed value to one of its arguments.
            Please note: to set fixed values to multiple arguments of a transformation,
            use the fixed decorator multiple times.

        See Also
        --------
        decorators.fixed : Fix the argument arg to the given value overriding the value
            of arg in the given kwargs.
        """

        @wraps(transformation)
        def wrapper(*args, **kwargs):
            kwargs[arg] = value
            transformation_result = transformation(*args, **kwargs)
            is_parameterized = True
            return transformation_result, kwargs, is_parameterized

        return wrapper

    @staticmethod
    def randomized_generator(transform: Union[Transform, GeneralTransform], arg: str,
                             generator:
                             MetamorphicGenerator[A]) -> Union[Transform, GeneralTransform]:
        """
        This method is internally called by decorator.randomized() to register a
        randomized generator to a transformation.

        Parameters
        ----------
        transform : Union[Transform, GeneralTransform]
            The transformation to which the randomized_generator needs to be
            associated to always get a fixed value for an argument to the
            transformation.

        arg : str
            Name of the argument which needs to be supplied with a randomized
            value while performing transformation.

        generator: MetamorphicGenerator[A]
            The custom random generator for the argument arg.

        Returns
        -------
        wrapper : Union[Transform, GeneralTransform]
            A function which modifies the original transformation function by setting a
            randomized value to one of its arguments.
            Please note: to set randomized values to multiple arguments of a transformation,
            use the randomized decorator multiple times.

        See Also
        --------
        decorators.randomized : Randomize the argument arg by the value generated by
                                the generator.
        """

        @wraps(transform)
        def wrapper(*args, **kwargs):
            kwargs[arg] = generator.generate()
            transformation_result = transform(*args, **kwargs)
            is_parameterized = True
            return transformation_result, kwargs, is_parameterized

        return wrapper
