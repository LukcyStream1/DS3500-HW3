import pandas as pd
import numpy as np
from evo import Evo
import random as rnd

# Read the TAS and sections data from CSV files
tas = pd.read_csv('../tas.csv', index_col=0)
pref = tas.iloc[:, 2:]
sections = pd.read_csv('../sections.csv', index_col=0)

# Define functions to evaluate different objectives for TA allocation

def overallocation(sol):
    """Calculate overallocation by summing differences between assigned and max assignable TAs."""
    diff = sol.sum(axis=1) - tas.max_assigned
    return sum(diff[diff > 0])

def conflicts(sol):
    """Calculate number of time conflicts among TAs' schedules."""
    # Extract day and time for each section
    dt = sections['daytime'].values

    # Create matrix representing time conflicts between sections
    conflict = (dt[:, None] == dt).astype(int)

    # Determine conflicts by matrix multiplication and sum up
    ta_conflict = np.dot(sol, conflict) >= 2
    return sum(1 for x in ta_conflict if True in x)

def undersupport(sol):
    """Calculate undersupport by comparing minimum required TAs and assigned TAs."""
    diff = sections.min_ta - sol.sum(axis=0)
    return sum(diff[diff > 0])

def unwilling(sol):
    """Count the number of unwilling TA allocations."""
    return ((sol * pref == 'U').astype(int).sum().sum())

def unpreferred(sol):
    """Calculate the number of unpreferred TA allocations."""
    return (sol * (pref == 'W').astype(int)).sum().sum()

# Define functions for generating new solutions
def swap(solutions):
    """Exchange positions of two rows in a solution."""
    sol_copy = solutions[0].copy()
    i, j = rnd.sample(range(len(sol_copy)), 2)
    sol_copy[[i, j]] = sol_copy[[j, i]]
    return sol_copy

def replace(solutions):
    """Replace a row in the solution with a randomly generated array of 0s and 1s."""
    sol_copy = solutions[0].copy()
    row_index = rnd.randrange(len(sol_copy))
    sol_copy[row_index, :] = np.random.choice([0, 1], size=(sol_copy.shape[1],))
    return sol_copy

def min_unwilling(solutions):
    """Modify solution to eliminate unwilling allocations of TAs."""
    sol_copy = solutions[0].copy()
    willing = sol_copy * (tas.iloc[:, 2:] == 'U').astype(int)
    willing = np.where(willing == 1, 0, 1)
    return willing * sol_copy

def combine(solutions):
    """Combine halves of two solutions to create a new one."""
    sol1, sol2 = solutions[0].copy(), solutions[1].copy()
    half1 = sol1[:len(sol1) // 2, :]
    half2 = sol2[len(sol2) // 2:, :]
    return np.concatenate((half1, half2), axis=0)

# Main function to run the evolutionary algorithm

def main():
    # Initialize the evolutionary algorithm framework
    E = Evo()

    # Add objectives for the evolutionary algorithm to optimize
    E.add_fitness_criteria('overallocation', overallocation)
    E.add_fitness_criteria('conflicts', conflicts)
    E.add_fitness_criteria('undersupport', undersupport)
    E.add_fitness_criteria('unwilling', unwilling)
    E.add_fitness_criteria('unpreferred', unpreferred)

    # Add agents (variation methods) to the evolutionary algorithm
    E.add_agent("swap", swap, k=1)
    E.add_agent("replace", replace, k=1)
    E.add_agent("min_unwilling", min_unwilling, k=1)
    E.add_agent("combine", combine, k=2)

    # Seed the evolutionary algorithm with an initial random solution
    initial_solution = np.random.choice([0, 1], size=pref.shape)
    E.add_solution(initial_solution)

    # Run the evolutionary algorithm
    E.evolve(1000, 100, 100)  # parameters: iterations, population size, mutation rate

    # Output the results
    print(E.pop.keys())

    E.csv(groupname='case')
if __name__ == '__main__':
    main()
