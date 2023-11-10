"""
Unit Test Case based on Sample Solution 1
"""

import numpy as np
import pytest
import HW3.code.main as main


# create fixture of test solution (1)
@pytest.fixture
def sol():
    return np.loadtxt("../test1.csv",
                 delimiter=",", dtype=int)


#test each individual objective function with expected scores
def test_overallocation(sol):
    assert main.overallocation(sol) == 37, 'overallocation objective ' \
                                      'is not properly calculated'

def test_conflicts(sol):
    assert main.conflicts(sol) == 8, 'conflicts objective ' \
                                           'is not properly calculated'


def test_undersupport(sol):
    assert main.undersupport(sol) == 1, 'undersupport objective ' \
                                        'is not properly calculated'

def test_unwilling(sol):
    assert main.unwilling(sol) == 53, 'unwilling objective ' \
                                        'is not properly calculated'

def test_unpreferred(sol):
    assert main.unpreferred(sol) == 15, 'unpreferred objective ' \
                                      'is not properly calculated'