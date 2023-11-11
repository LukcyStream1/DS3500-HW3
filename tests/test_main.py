"""
Unit Test Case based on Sample Solutions
"""

import numpy as np
import pytest
import code.main as main

    #create fixture of test solution (1)
@pytest.fixture
def sol():
    return np.loadtxt("test1.csv",
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

# create fixture of test solution (2)
@pytest.fixture
def sol():
    return np.loadtxt("test2.csv",
                 delimiter=",", dtype=int)


#test each individual objective function with expected scores
def test_overallocation(sol):
    assert main.overallocation(sol) == 41, 'overallocation objective ' \
                                      'is not properly calculated'

def test_conflicts(sol):
    assert main.conflicts(sol) == 5, 'conflicts objective ' \
                                           'is not properly calculated'


def test_undersupport(sol):
    assert main.undersupport(sol) == 0, 'undersupport objective ' \
                                        'is not properly calculated'

def test_unwilling(sol):
    assert main.unwilling(sol) == 58, 'unwilling objective ' \
                                        'is not properly calculated'

def test_unpreferred(sol):
    assert main.unpreferred(sol) == 19, 'unpreferred objective ' \
                                      'is not properly calculated'


# create fixture of test solution (3)
@pytest.fixture
def sol():
    return np.loadtxt("test3.csv",
                 delimiter=",", dtype=int)

#test each individual objective function with expected scores
def test_overallocation(sol):
    assert main.overallocation(sol) == 23, 'overallocation objective ' \
                                      'is not properly calculated'

def test_conflicts(sol):
    assert main.conflicts(sol) == 2, 'conflicts objective ' \
                                           'is not properly calculated'

def test_undersupport(sol):
    assert main.undersupport(sol) == 7, 'undersupport objective ' \
                                        'is not properly calculated'

def test_unwilling(sol):
    assert main.unwilling(sol) == 43, 'unwilling objective ' \
                                        'is not properly calculated'

def test_unpreferred(sol):
    assert main.unpreferred(sol) == 10, 'unpreferred objective ' \
                                      'is not properly calculated'
