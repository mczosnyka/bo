import numpy as np
import pytest
from saport.assignment.simplex_solver import Solver
from saport.assignment.model import AssignmentProblem, NormalizedAssignmentProblem
from tests.common_test_utils import indented_string

class TestSimplexSolver:


    @pytest.mark.parametrize("costs, is_min, norm_costs, expected_objective", [
        ([[4, 9, 8], [6, 7, 5], [4, 6, 1]], True, [[4, 9, 8], [6, 7, 5], [4, 6, 1]], 12),
        ([[2, 11, 2, 6], [3, 10, 9, 4], [8, 6, 6, 6], [10, 13, 15, 13]], True, [[2, 11, 2, 6], [3, 10, 9, 4], [8, 6, 6, 6], [10, 13, 15, 13]], 22),
        ([[2, 11, 2, 1], [3, 10, 3, 4], [8, 6, 6, 2], [11, 13, 15, 13]], True, [[2, 11, 2, 1], [3, 10, 3, 4], [8, 6, 6, 2], [11, 13, 15, 13]], 20),
        ([[4, 9, 8], [6, 7, 5], [4, 6, 9]], True, [[4, 9, 8], [6, 7, 5], [4, 6, 9]], 15),
        ([[4, 3, 8], [6, 7, 5], [4, 6, 9], [5, 7, 4]], True, [[4, 3, 8, 0], [6, 7, 5, 0], [4, 6, 9, 0], [5, 7, 4, 0]], 11),
        ([[4, 9, 8], [6, 7, 5], [4, 6, 9], [5, 7, 4]], True, [[4, 9, 8, 0], [6, 7, 5, 0], [4, 6, 9, 0], [5, 7, 4, 0]], 14),
        ([[4, 9, 8, 5], [6, 7, 5, 8], [4, 6, 9, 6]], True, [[4, 9, 8, 5], [6, 7, 5, 8], [4, 6, 9, 6], [0, 0, 0, 0]], 14),
        ([[4, 9, 8, 5], [6, 7, 5, 8], [4, 6, 1, 6]], True, [[4, 9, 8, 5], [6, 7, 5, 8], [4, 6, 1, 6], [0, 0, 0, 0]], 12),
        ([[2, 11, 2, 6], [3, 10, 9, 4], [8, 6, 6, 6], [10, 13, 15, 13]], False, [[13, 4, 13, 9], [12, 5, 6, 11], [7, 9, 9, 9], [5, 2, 0, 2]], 41),
        ([[2, 11, 2, 6], [3, 10, 9, 4], [8, 6, 6, 6], [18, 13, 15, 13]], False, [[16, 7, 16, 12], [15, 8, 9, 14], [10, 12, 12, 12], [0, 5, 3, 5]], 44),
        ([[4, 9, 8], [6, 7, 5], [4, 6, 9], [5, 7, 4]], False, [[5, 0, 1, 0], [3, 2, 4, 0], [5, 3, 0, 0], [4, 2, 5, 0]], 24),
        ([[4, 7, 8], [6, 7, 5], [4, 6, 9], [5, 7, 4]], False, [[5, 2, 1, 0], [3, 2, 4, 0], [5, 3, 0, 0], [4, 2, 5, 0]], 22)
    ])
    def test_simplex_should_be_able_to_solve_assignment_problems(
        self, costs, is_min, norm_costs, expected_objective
    ):
        costs = np.array(costs)
        norm_costs = np.array(norm_costs)
        problem = AssignmentProblem("test_problem", costs, is_min)
        norm_problem = NormalizedAssignmentProblem(norm_costs, problem)
        correct_solver = Solver.__new__(Solver)
        correct_solver.problem = norm_problem

        solution = correct_solver.solve()

        assert (
            solution.objective == expected_objective
        ), f"simplex algorithm returns incorrect objective:" +\
            f"\n- got: {solution.objective}" +\
            f"\n- expected: {expected_objective}" +\
            f"\n- for cost matrix: {indented_string(str(problem.costs))}"

        assert isinstance(solution.assigned_tasks, list), \
            f"the assigned tasks are expected to be returned as list:" +\
            f"the assigned tasks are expected to be returned as a list:" +\
            f"\n- got: {solution.assigned_tasks} of type: `{type(solution.assigned_tasks).__name__}`"

        meta_inf = f"\n- got assignment: {solution.assigned_tasks}" +\
            f"\n- for cost matrix: {indented_string(str(problem.costs))}"
        assert len(solution.assigned_tasks) >= problem.n_workers(), \
            "the assignment seems to miss a worker:" + meta_inf
        assert len(solution.assigned_tasks) <= problem.n_workers(), \
            "the assignment seems to use non-existing workers:" + meta_inf
        assert max(solution.assigned_tasks) <= problem.n_tasks(), \
            "the assignment seems to assing a non-existing task" + meta_inf



