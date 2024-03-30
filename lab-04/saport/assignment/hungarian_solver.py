import numpy as np
from .model import Assignment, AssignmentProblem, NormalizedAssignmentProblem
from typing import List, Dict, Tuple, Set
from numpy.typing import ArrayLike

class Solver:
    '''
    A hungarian solver for the assignment problem.

    Methods:
    --------
    __init__(problem: AssignmentProblem):
        creates a solver instance for a specific problem
    solve() -> Assignment:
        solves the given assignment problem
    extract_mins(costs: ArrayLike):
        substracts from columns and rows in the matrix to create 0s in the matrix
    find_max_assignment(costs: ArrayLike) -> Dict[int,int]:
        finds the biggest possible assinments given 0s in the cost matrix
        result is a dictionary, where index is a worker index, value is the task index
    add_zero_by_crossing_out(costs: ArrayLike, partial_assignment: Dict[int,int])
        creates another zero(s) in the cost matrix by crossing out lines (rows/cols) with zeros in the cost matrix,
        then substracting/adding the smallest not crossed out value
    create_assignment(raw_assignment: Dict[int, int]) -> Assignment:
        creates an assignment instance based on the given dictionary assignment
    '''
    def __init__(self, problem: AssignmentProblem):
        self.problem = NormalizedAssignmentProblem.from_problem(problem)

    def solve(self) -> Assignment:
        costs = np.array(self.problem.costs)

        while True:
            self.extracts_mins(costs)
            max_assignment = self.find_max_assignment(costs)
            if len(max_assignment) == self.problem.size():
                return self.create_assignment(max_assignment)
            self.add_zero_by_crossing_out(costs, max_assignment)

    def extracts_mins(self, costs: ArrayLike):
        #TODO: substract minimal values from each row and column
        for i in range(len(costs)):
            temp = np.amin(costs[i])
            for j in range(len(costs[i])):
                costs[i][j] -= temp
        for i in range(len(costs[0])):
            temp = np.amin(costs[:, i])
            for j in range(len(costs)):
                costs[j][i] -= temp

    def add_zero_by_crossing_out(self, costs: ArrayLike, partial_assignment: Dict[int,int]):
        # TODO:
        # 1) "mark" columns and rows according to the instructions given by teacher
        # 2) cross out marked columns and not marked rows
        # 3) find minimal uncrossed value and subtract it from the cost matrix
        # 4) add the same value to all crossed out columns and rows
        raise NotImplementedError()

    def find_max_assignment(self, costs) -> Dict[int,int]:
        partial_assignment = dict()
        # TODO: find the biggest assignment in the cost matrix
        # 1) always try first the row with the least amount of 0s
        # 2) then use column with the least amount of 0s
        # TIP: remember, rows and cols can't repeat in the assignment
        #      partial_assignment[1] = 2 means that the worker with index 1
        #                                has been assigned to task with index 2
        return partial_assignment

    def create_assignment(self, raw_assignment: Dict[int,int]) -> Assignment:
        # TODO: create an assignment instance based on the dictionary
        # tips:
        # 1) use self.problem.original_problem.costs to calculate the cost
        # 2) in case the original cost matrix (self.problem.original_problem.costs wasn't square)
        #    and there is more workers than task, you should assign -1 to workers with no task
        assignment = None
        total_cost = None
        return Assignment(assignment, total_cost)