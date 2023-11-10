import csv
import random as rnd
import copy
from functools import reduce
import time
import pickle

class Evo:

    def __init__(self):
        self.pop = {}  # eval -> solution   eval = ((name1, val1), (name2, val2)..)
        self.fitness = {}  # name -> function
        self.agents = {}  # name -> (operator, num_solutions_input)

    def size(self):
        """ The size of the solution population """
        return len(self.pop)

    def add_fitness_criteria(self, name, f):
        self.fitness[name] = f

    def add_agent(self, name, op, k=1):
        self.agents[name] = (op, k)

    def add_solution(self, sol):
        eval = tuple([(name, f(sol)) for name, f in self.fitness.items()])
        self.pop[eval] = sol

    def get_random_solutions(self, k=1):
        if self.size() == 0:  # No solutions in the populations
            return []
        else:
            popvals = tuple(self.pop.values())
            return [copy.deepcopy(rnd.choice(popvals)) for _ in range(k)]

    def run_agent(self, name):
        op, k = self.agents[name]
        picks = self.get_random_solutions(k)
        new_solution = op(picks)
        self.add_solution(new_solution)

    @staticmethod
    def _dominates(p, q):
        """ Return whether p dominates q """
        pscores = [score for _, score in p]
        qscores = [score for _, score in q]
        score_diffs = list(map(lambda x, y: y - x, pscores, qscores))
        min_diff = min(score_diffs)
        max_diff = max(score_diffs)
        return min_diff >= 0.0 and max_diff > 0.0

    @staticmethod
    def _reduce_nds(S, p):
        return S - {q for q in S if Evo._dominates(p, q)}

    def remove_dominated(self):
        nds = reduce(Evo._reduce_nds, self.pop.keys(), self.pop.keys())
        self.pop = {k:self.pop[k] for k in nds}

    def evolve(self, n=1, dom=100, status=100, sync=1000, time_limit = 600):
        agent_names = list(self.agents.keys())
        start_time = time.time()  # Record the start time

        for i in range(n):
            # If a time limit has been set, check if we've reached it
            if time_limit and (time.time() - start_time) >= time_limit:
                break

            # pick an agent
            pick = rnd.choice(agent_names)

            # run the agent to produce a new solution
            self.run_agent(pick)

            # periodically cull the population
            # discard dominated solutions
            if i % dom == 0:
                self.remove_dominated()


            if i % status == 0: # print the population
                self.remove_dominated()
                print("Iteration: ", i)
                print("Population Size: ", self.size())
                print(self)

            if i % sync == 0:
                try:
                    with open('../solutions.dat', 'rb') as file:

                        # load saved population into a dictionary object
                        loaded = pickle.load(file)

                        # merge loaded solutions into my population
                        for eval, sol in loaded.items():
                            self.pop[eval] = sol
                except Exception as e:
                    print(e)

                # remove the dominated solutions
                self.remove_dominated()

                # resave the non-dominated solutions back to the file
                with open('../solutions.dat', 'wb') as file:
                    pickle.dump(self.pop, file)

                # break loop if invocations evolver finishes before time limit
                if time.time() - start_time >= time_limit:
                    # Clean up population
                    self.remove_dominated()
                    break

    def __str__(self):
        """ Output the solutions in the population """
        rslt = ""
        for eval,sol in self.pop.items():
            rslt += str(dict(eval))+":\t"+str(sol)+"\n"
        return rslt

    def csv(self, groupname, filename='result.csv'):

        # open the file for writing
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)

            # Write the header row
            header_row = [groupname] + list(self.fitness.keys())
            writer.writerow(header_row)

            # write the result for each objective/score
            for eval in self.pop.keys():
                eval_dict = dict()
                for obj, score in eval:
                    eval_dict[obj] = score
                writer.writerow([groupname,
                                 eval_dict['overallocation'],
                                 eval_dict['conflicts'],
                                 eval_dict['undersupport'],
                                 eval_dict['unwilling'],
                                 eval_dict['unpreferred']])