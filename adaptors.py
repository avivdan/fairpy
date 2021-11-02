#!python3

"""
Adapts algorithms, using a specific input and output formats, to accept various other input/output formats.

Programmer: Erel Segal-Halevi
Since: 2021-11
"""

import numpy as np
from typing import Any, Callable, List
from fairpy import ValuationMatrix, AllocationMatrix, Allocation
from fairpy.bundles import FractionalBundle, ListBundle


def adapt_list_algorithm(algorithm: Callable, input: Any):
    """
    Adapts an algorithm, that accepts as input a list of lists,
    to accept various other input formats.

    >>> # Available input formats:

    >>> input_matrix = np.ones([2,3])        # a numpy array of valuations.
    >>> adapt_list_algorithm(dummy_list_list_algorithm, input_matrix)
    Agent #0 gets {0,2} with value 2.
    Agent #1 gets {1} with value 1.
    <BLANKLINE>
    >>> adapt_list_algorithm(dummy_list_matrix_algorithm, input_matrix)
    Agent #0 gets { 100.0% of 0, 100.0% of 2} with value 2.
    Agent #1 gets { 100.0% of 1} with value 1.
    <BLANKLINE>

    >>> input_list_of_lists = [[1,4,7],[6,3,0]]     # a list of lists.
    >>> adapt_list_algorithm(dummy_list_list_algorithm, input_list_of_lists)
    Agent #0 gets {0,2} with value 8.
    Agent #1 gets {1} with value 3.
    <BLANKLINE>
    >>> adapt_list_algorithm(dummy_list_matrix_algorithm, input_list_of_lists)
    Agent #0 gets { 100.0% of 0, 100.0% of 2} with value 8.
    Agent #1 gets { 100.0% of 1} with value 3.
    <BLANKLINE> 

    >>> input_valuation_matrix = ValuationMatrix(input_list_of_lists)
    >>> adapt_list_algorithm(dummy_list_list_algorithm, input_valuation_matrix)
    Agent #0 gets {0,2} with value 8.
    Agent #1 gets {1} with value 3.
    <BLANKLINE>
    >>> adapt_list_algorithm(dummy_list_matrix_algorithm, input_valuation_matrix)
    Agent #0 gets { 100.0% of 0, 100.0% of 2} with value 8.
    Agent #1 gets { 100.0% of 1} with value 3.
    <BLANKLINE> 

    >>> input_dict_of_lists = {"a": [1,2,3], "b": [4,5,6]}      # a dict mapping agent names to list of values.
    >>> adapt_list_algorithm(dummy_list_list_algorithm, input_dict_of_lists)
    a gets {0,2} with value 4.
    b gets {1} with value 5.
    <BLANKLINE>
    >>> adapt_list_algorithm(dummy_list_matrix_algorithm, input_dict_of_lists)
    a gets { 100.0% of 0, 100.0% of 2} with value 4.
    b gets { 100.0% of 1} with value 5.
    <BLANKLINE>

    >>> input_dict_of_dicts = {"a": {"x":1,"y":2,"z":3}, "b": {"x":4,"y":5,"z":6}}       # a dict mapping agent names to dict of values.
    >>> adapt_list_algorithm(dummy_list_list_algorithm, input_dict_of_dicts)
    a gets {x,z} with value 4.
    b gets {y} with value 5.
    <BLANKLINE>
    >>> adapt_list_algorithm(dummy_list_matrix_algorithm, input_dict_of_dicts)
    a gets { 100.0% of x, 100.0% of z} with value 4.
    b gets { 100.0% of y} with value 5.
    <BLANKLINE>
    """
    # Step 1. Adapt the input:
    object_names = agent_names = None
    if isinstance(input, dict):  
        agent_names = list(input.keys())
        list_of_valuations = list(input.values())
        if isinstance(list_of_valuations[0], dict): # maps agent names to dicts of valuations
            object_names = list(list_of_valuations[0].keys())
            list_of_valuations = [
                [valuation[object] for object in object_names]
                for valuation in list_of_valuations
            ]
        valuation_matrix = input
    elif isinstance(input, list) and isinstance(input[0], list):  # list of lists
        agent_names = [f"Agent #{i}" for i in range(len(input))]
        list_of_valuations = input
        valuation_matrix = ValuationMatrix(input)
    elif isinstance(input, np.ndarray) or isinstance(input, ValuationMatrix):
        valuation_matrix = ValuationMatrix(input)
        agent_names = [f"Agent #{i}" for i in valuation_matrix.agents()]
        list_of_valuations = [valuation_matrix[i] for i in valuation_matrix.agents()]
    else:
        raise TypeError(f"Unsupported input type: {type(input)}")

    # Step 2. Run the algorithm:
    output = algorithm(list_of_valuations)

    # Step 3. Adapt the output:
    if isinstance(output, np.ndarray) or isinstance(output, AllocationMatrix):  # allocation matrix
        allocation_matrix = AllocationMatrix(output)
        if isinstance(input, dict):
            list_of_bundles = [FractionalBundle(allocation_matrix[i], object_names) for i in allocation_matrix.agents()]
            dict_of_bundles = dict(zip(agent_names,list_of_bundles))
            return Allocation(input, dict_of_bundles)
        else:
            return Allocation(valuation_matrix, allocation_matrix)
    elif isinstance(output, list):
        if object_names is None:
            list_of_bundles = output
        else:
            list_of_bundles = [
                [object_names[object_index] for object_index in bundle]
                for bundle in output
            ]
        dict_of_bundles = dict(zip(agent_names,list_of_bundles))
        return Allocation(valuation_matrix, dict_of_bundles)
    else:
        raise TypeError(f"Unsupported output type: {type(output)}")



def adapt_matrix_algorithm(algorithm: Callable, input: Any):
    """
    Adapts an algorithm, that accepts as input a ValuationMatrix object,
    to accept various other input formats.

    >>> # Available input formats:
    >>> input_matrix = np.ones([2,3])        # a numpy array of valuations.
    >>> adapt_matrix_algorithm(dummy_matrix_list_algorithm, input_matrix)
    Agent #0 gets {0,2} with value 2.
    Agent #1 gets {1} with value 1.
    <BLANKLINE>
    >>> adapt_matrix_algorithm(dummy_matrix_matrix_algorithm, input_matrix)
    Agent #0 gets { 100.0% of 0, 100.0% of 2} with value 2.
    Agent #1 gets { 100.0% of 1} with value 1.
    <BLANKLINE>
    >>> input_list_of_lists = [[1,4,7],[6,3,0]]     # a list of lists.
    >>> adapt_matrix_algorithm(dummy_matrix_list_algorithm, input_list_of_lists)
    Agent #0 gets {0,2} with value 8.
    Agent #1 gets {1} with value 3.
    <BLANKLINE>
    >>> adapt_matrix_algorithm(dummy_matrix_matrix_algorithm, input_list_of_lists)
    Agent #0 gets { 100.0% of 0, 100.0% of 2} with value 8.
    Agent #1 gets { 100.0% of 1} with value 3.
    <BLANKLINE>
    >>> input_dict_of_lists = {"a": [1,2,3], "b": [4,5,6]}      # a dict mapping agent names to list of values.
    >>> adapt_matrix_algorithm(dummy_matrix_list_algorithm, input_dict_of_lists)
    a gets {0,2} with value 4.
    b gets {1} with value 5.
    <BLANKLINE>
    >>> adapt_matrix_algorithm(dummy_matrix_matrix_algorithm, input_dict_of_lists)
    a gets { 100.0% of 0, 100.0% of 2} with value 4.
    b gets { 100.0% of 1} with value 5.
    <BLANKLINE>
    >>> input_dict_of_dicts = {"a": {"x":1,"y":2,"z":3}, "b": {"x":4,"y":5,"z":6}}       # a dict mapping agent names to dict of values.
    >>> adapt_matrix_algorithm(dummy_matrix_list_algorithm, input_dict_of_dicts)
    a gets {x,z} with value 4.
    b gets {y} with value 5.
    <BLANKLINE>
    >>> adapt_matrix_algorithm(dummy_matrix_matrix_algorithm, input_dict_of_dicts)
    a gets { 100.0% of x, 100.0% of z} with value 4.
    b gets { 100.0% of y} with value 5.
    <BLANKLINE>
    """
    def list_algorithm(list_input:List):
        matrix_input = ValuationMatrix(list_input)
        return algorithm(matrix_input)
    return adapt_list_algorithm(list_algorithm, input)






"""
The algorithms below are dummy algorithms, used for demonstrating the adaptors.
They accept an input a valuation profile (as a list of lists, or valuation matrix),
     and return as output an allocation profile (as a list of lists, or allocation matrix).
The allocate the objects in turn, like "round robin" but without regard to valuations.
"""

def dummy_list_list_algorithm(valuations:List[List])->List[List]:
    """ 
    >>> dummy_list_list_algorithm([[11,22,33],[44,55,66]])
    [[0, 2], [1]]
    """
    num_agents = len(valuations)
    num_objects = len(valuations[0])
    bundles = [[] for _ in range(num_agents)]
    i_agent = 0
    for i_object in range(num_objects):
        bundles[i_agent].append(i_object)
        i_agent += 1
        if i_agent >= num_agents:
            i_agent = 0
    return bundles


def dummy_list_matrix_algorithm(valuations:List[List])->np.ndarray:
    """ 
    >>> dummy_list_matrix_algorithm([[11,22,33],[44,55,66]])
    array([[1., 0., 1.],
           [0., 1., 0.]])
    """
    num_agents = len(valuations)
    num_objects = len(valuations[0])
    bundles = np.zeros([num_agents,num_objects])
    i_agent = 0
    for i_object in range(num_objects):
        bundles[i_agent][i_object] = 1
        i_agent += 1
        if i_agent >= num_agents:
            i_agent = 0
    return bundles

def dummy_matrix_list_algorithm(valuations:ValuationMatrix)->List[List]:
    """ 
    >>> dummy_matrix_list_algorithm(ValuationMatrix([[11,22,33],[44,55,66]]))
    [[0, 2], [1]]
    """
    num_agents = valuations.num_of_agents
    num_objects = valuations.num_of_objects
    bundles = [[] for _ in range(num_agents)]
    i_agent = 0
    for i_object in range(num_objects):
        bundles[i_agent].append(i_object)
        i_agent += 1
        if i_agent >= num_agents:
            i_agent = 0
    return bundles

def dummy_matrix_matrix_algorithm(valuations:ValuationMatrix)->np.ndarray:
    """ 
    >>> dummy_matrix_matrix_algorithm(ValuationMatrix([[11,22,33],[44,55,66]]))
    array([[1., 0., 1.],
           [0., 1., 0.]])
    """
    num_agents = valuations.num_of_agents
    num_objects = valuations.num_of_objects
    bundles = np.zeros([num_agents,num_objects])
    i_agent = 0
    for i_object in range(num_objects):
        bundles[i_agent][i_object] = 1
        i_agent += 1
        if i_agent >= num_agents:
            i_agent = 0
    return bundles


if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))