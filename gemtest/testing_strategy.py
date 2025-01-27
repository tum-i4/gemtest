class TestingStrategy:
    """
    Strategy for Metamorphic Test Case creation.

    SAMPLE:
        Creates a specified number of MTCs from the provided data.
    EXHAUSTIVE:
        Creates an MTC for every element of the provided data. Be careful using
        EXHAUSTIVE in combination with multiple source inputs. The number of created MTCs grows
        exponentially with the number of source inputs n, bcause all possible n-tuples are
        created from the provided data.
    """
    EXHAUSTIVE = 'exhaustive'
    SAMPLE = 'sample'
