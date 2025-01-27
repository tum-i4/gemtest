import pytest

from gemtest.metamorphic_test_suite import MetamorphicTestSuite
from gemtest.testing_strategy import TestingStrategy
from unittest.mock import Mock, patch

# Define a mock transformation function
def mock_transformation(arg1, arg2):
    return arg1 + arg2

def test_multiple_mrs_same_name():
    suite = MetamorphicTestSuite()

    suite.add_metamorphic_relation(name="mr1", data=[1],
                                   testing_strategy=TestingStrategy.SAMPLE,
                                   number_of_test_cases=1,
                                   number_of_sources=1)

    with pytest.raises(ValueError):
        suite.add_metamorphic_relation(name="mr1", data=[1],
                                       testing_strategy=TestingStrategy.SAMPLE,
                                       number_of_test_cases=1,
                                       number_of_sources=1)
        
def test_fixed_generator():
    # Call fixed_generator function with the mock transformation, the argument to be fixed and a value
    fixed_gen = MetamorphicTestSuite.fixed_generator(mock_transformation, 'arg2', 5)

    # Call the modified transformation
    result, kwargs, is_parameterized = fixed_gen(2, arg2=3)  # This should overwrite arg2 to 5

    # Check correct result, the argument correctly fixed and the parameterization to be set 
    assert result == 7  
    assert kwargs['arg2'] == 5  
    assert is_parameterized == True

def test_randomized_generator():
    mock_generator = Mock()
    mock_generator.generate.return_value = 7

    # Use the randomized_generator 
    randomized_gen = MetamorphicTestSuite.randomized_generator(mock_transformation, 'arg2', mock_generator)

    # Call the modified transformation arg2 will be set to 7
    result, kwargs, is_parameterized = randomized_gen(3, arg2=4)

    assert result == 10
    assert kwargs['arg2'] == 7
    assert is_parameterized == True