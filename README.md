# GeMTest 💎: A General Metamorphic Testing Framework

The ``gemtest`` framework can simply be installed via ``pip install gemtest`` and makes it easy to write metamorphic relations in Python, from which the framework derives 
multiple metamorphic test cases.
Metamorphic test cases are then executed as a ``pytest`` test suite.

An example of a simple metamorphic relation:

```python
# content of test_sin_metamorphic.py
import gemtest as gmt
import math

mr_1 = gmt.create_metamorphic_relation(name='mr_1', data=range(100))


@gmt.transformation(mr_1)
def example_transformation(source_input: float) -> float:
  return source_input + 2 * math.pi


@gmt.relation(mr_1)
def example_relation(source_output: float, followup_output: float) -> bool:
  return gmt.relations.approximately(source_output, followup_output)


@gmt.system_under_test(mr_1)
def test_example_sut(input: float) -> float:
  return math.sin(input)
```

To execute it:

```console
$ pytest test_sin_metamorphic.py
=============== test session starts ===============
platform linux -- Python 3.10.12, pytest-8.3.4, 
pluggy-1.5.0 
rootdir: /home/user/gemtest 
plugins: typeguard-2.13.3, html-3.2.0, 
metadata-3.1.1, xdist-3.6.1, gemtest-1.0.0, 
cov-4.1.0, hypothesis-6.113.0 
collected 100 items             

test_sin_metamorphic.py ..................
..........................................
........................................

=============== 100 passed in 0.28s ===============
```

## Available Command Line Options for Running GeMTest
- `pytest --string-report <test-file path>`: Enables custom string report output on console.
- `pytest --html-report <test-file path>`: Enables custom html report including 
  visualization of in- and outputs if a visualization function is provided, additionally 
  test results are stored in an SQLite database and can be viewed with the ``gemtest-webapp``.

![Function Domains](https://raw.githubusercontent.com/tum-i4/gemtest/main/resources/Simple_MR_Scheme.png)
A simple metamorphic relation consists of 4 parts: 
1. The creation of the metamorphic relation. Every metamorphic relation requires a name and a data source from 
which the metamorphic test cases are created.
```python
<mr1_name> = gmt.create_metamorphic_relation(name='mr_1', data=range(100))
 ```
2. A function annotated with ``@transformation`` which takes a single source input and creates a 
  single followup input. A transformation can be registered to a metamorphic relation by 
  specifying the name of the metamorphic relation in the ``@transformation`` annotation.  A 
  transformation is registered to all metamorphic relations of a test file if no 
  metamorphic relation is explicitly specified in the ``@transformation`` annotation. Every 
  metamorphic relation can only have one registered transformation.
```python
@gmt.transformation(<mr1_name, mr2_name, ... >)
def <transformation_function_name>(source_input: Input) -> Input:
    <apply custom transformation to Input>
 ```
3. A function annotated with ``@relation`` which takes a single source output and followup 
  output and return a boolean value. Registering a relation to a metamorphic relation works 
  identically to the registration of a transformation. Every 
  metamorphic relation can only have one registered relation.
```python
@gmt.relation(<mr1_name, mr2_name, ... >)
def <relation_function_name>(source_output: Output, followup_output: Output) -> boolean:
    <apply custom relation to Outputs>
 ```
4. A function annotated by ``@system_under_test`` whose name must begin with test, take a 
  single input and return a single output. Registering a system under test to a metamorphic 
  relation works identical to the registration for a transformation. 
```python
@gmt.system_under_test(<mr1_name, mr2_name, ... >)
def test_<system_name>(input: Input) -> Output:
    <apply custom system functionality to Input>
 ```

## Documentation

To use ``gemtest``, one must first define one's metamorphic relations 
using the `create_metamorphic_relation()` function. This function takes in various arguments,
such as the name of the relation, the data to be transformed, and the number of test cases 
to generate:
````python
def create_metamorphic_relation(
        name: str,
        data: Sequence,
        testing_strategy: str = TestingStrategy.EXHAUSTIVE,
        number_of_test_cases: int = 1,
        number_of_sources: int = 1,
        parameters: Optional[Dict] = None,
        system_under_test: Optional[System] = None,
        transform: Optional[Transform] = None,
        general_transform: Optional[GeneralTransform] = None,
        relation: Optional[Relation] = None,
        general_relation: Optional[GeneralRelation] = None,
        valid_input: Optional[Input] = None
) -> MR_ID:
````

Parameters
- name: Name of the metamorphic relation.
- data: A sequence of input data that is used to generate metamorphic test cases.
- testing_strategy: Specifies the testing strategy to use for generating 
  metamorphic test cases. Can take the values TestingStrategy.SAMPLE or TestingStrategy.
  EXHAUSTIVE. Default value is TestingStrategy.EXHAUSTIVE.
- number_of_test_cases: An integer that specifies the number of metamorphic test cases to 
  generate. Default value is 1.
- number_of_sources: An integer that specifies the number of input sources to use for 
  generating metamorphic test cases. Default value is 1.
- parameters: Optional dictionary of test parameters. Can be used to define multiple similar tests with different parameters.
- system_under_test: The system under test whose functionality is to be verified. Defaults to None.
- transform: Optional transformation function to apply to the input data.
- general_transform: An optional callable that represents the general transformation function to apply to the input data.
- relation: Optional relation function evaluating the metamorphic test case.
- general_relation: An optional callable that represents the general relation function evaluating the metamorphic test case.
- valid_input: A list of functions returning a bool that are used to validate the input to the system under test. The metamorphic test case is skipped if function returns false 

Functions for the properties ``system_under_test``, ``transform``, ``general_transform``, ``relation``, 
``general_relation``, and ``valid_input`` can be added to a metamorphic relation with annotations 
after it is created, as seen in the example above. The ``gemtest`` framework also contains predefined 
functions that can be added to a metamorphic relation during creation. 

## General Example
Next to the simple functionality provided by ``@transformation`` and ``@relation`` decorated functions, 
``gemtest`` also supports a more general approach for defining metamorphic relations using the 
``@general_transformation`` and ``@general_relation`` decorators.

```python
import gemtest as gmt
import math

mr_2 = gmt.create_metamorphic_relation(
  name='mr_2',
  data=range(10),
  testing_strategy=gmt.TestingStrategy.SAMPLE,
  number_of_test_cases=10,
  number_of_sources=2
)


@gmt.general_transformation(mr_2)
def shift(mtc: gmt.MetamorphicTestCase):
  followup_input_1 = mtc.source_inputs[0] + 2 * math.pi
  followup_input_2 = mtc.source_inputs[1] - 2 * math.pi
  return followup_input_1, followup_input_2


@gmt.general_relation(mr_2)
def approximately_equals(mtc: gmt.MetamorphicTestCase) -> bool:
  return (gmt.approximately(mtc.source_outputs[0], mtc.followup_outputs[0]) 
          and gmt.approximately(mtc.source_outputs[1], mtc.followup_outputs[1]))


@gmt.system_under_test(mr_2)
def test_dummy_sut(input: float) -> float:
  return math.sin(input)
```

![Metamorphic Relation Scheme](https://raw.githubusercontent.com/tum-i4/gemtest/main/resources/General_MR_Scheme.png)

A general metamorphic relation consists of 4 parts: 
1. The creation of the metamorphic relation. Every metamorphic relation requires a name and a data source 
from which the metamorphic test cases are created.
```python
<mr1_name> = gmt.create_metamorphic_relation(name='mr_1', data=range(100))
```
2. A function annotated with ``@general_transformation`` must take a ``MetamorphicTestCase`` object 
  and return a single or multiple followup inputs as a tuple. Registering a 
  general_transformation to a metamorphic relation works identically to the registration of a 
  transformation. Every metamorphic relation can only have one registered 
  general_transformation or transformation. A metamorphic relation may have a registered 
  general_transformation and a registered relation if the functionality of a 
  general_relation is not required. 
```python
@gmt.general_transformation(<mr1_name, mr2_name, ... >)
def <transformation_function_name>(mtc: MetamorphicTestCase) -> Input:
    <access single source_input> 
    source_input: Input = mtc.source_input
    
    <access multiple source_inputs> 
    source_inputs: List[Input] = mtc.source_inputs
    
    <apply custom transformation to Input>
    return followup_input_1, followup_input_2, ... , followup_input_n
 ```
3. A function annotated with ``@general_relation`` must take a ``MetamorphicTestCase`` object and 
  return a boolean value. Registering a  general_relation to a metamorphic relation works 
  identically to the registration of a relation. Every metamorphic relation can only have 
  one registered general_relation or relation.
```python
@gmt.general_relation(<mr1_name, mr2_name, ... >)
def <relation_function_name>(mtc: MetamorphicTestCase) -> boolean:
    <apply custom relation to attributes of MetamorphicTestCase>
 ```
4. A function annotated with ``@system_under_test`` whose name must begin with test, take a 
  single input and return a single output.

Using the ``MetamorphicTestCase`` object allows general transformations to have any 
number of sources and create any number of followups. There is also the possibility to use 
source inputs and source outputs to create followup inputs. A general relation can also use 
multiple sources and followups as and additionally consider source and followup inputs and 
outputs when evaluating if the relation holds for a ``MetamorphicTestCase``.

## The MetamorphicTestCase Object
The ``MetamorphicTestCase`` class holds one concrete instance of a metamorphic test case for a 
metamorphic relation. The testing strategy is used to create ``MetamorphicTestCase`` objects from the 
provided data object. ``Pytest`` tests are executed on instances of a ``MetamorphicTestCase``. If all 
``pytest`` tests for the ``MetamorphicTestCase`` objects of a metamorphic relation pass, the relation holds 
for the provided data.  

Properties of class ``MetamorphicTestCase``
- source_inputs: list of the source inputs for the Metamorphic Test Case
- source_input: convenience property to access the single source input if there is only one
- followup_inputs: list of the followup inputs for the Metamorphic Test Case
- followup_input: convenience property to access the single followup input if there is only one
- source_outputs: list of the source outputs for the Metamorphic Test Case
- source_output: convenience property to access the single source output if there is only one
- followup_outputs: list of the followup outputs for the Metamorphic Test Case
- followup_output: convenience property to access the single followup output if there is only one
- parameters: dictionary containing previously specified parameters

## Citation
If you find the ``gemtest`` framework useful in your research or projects, please consider citing it:

```
@inproceedings{speth2025,
    author = {Speth, Simon and Pretschner, Alexander},
    title = {{GeMTest: A General Metamorphic Testing Framework}},
    booktitle = "Proceedings of the 47th International Conference on Software Engineering, (ICSE-Companion)",
    pages = {1--4},
    address = {Ottawa, ON, Canada},
    year = {2025},
}
```

## License
[MIT License](https://github.com/tum-i4/gemtest/blob/main/LICENSE)

