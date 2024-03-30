import numpy as np
from saport.assignment.model import Assignment, AssignmentProblem, NormalizedAssignmentProblem
from saport.assignment.hungarian_solver import Solver
from tests.common_test_utils import indented_string
import pytest

class TestHungarianSolver:

    @pytest.mark.parametrize("costs, is_min, norm_costs, expected_costs", [
        ([[4, 9, 8], [6, 7, 5], [4, 6, 1]], True, [[4, 9, 8], [6, 7, 5], [4, 6, 1]], [[0, 3, 4], [1, 0, 0], [3, 3, 0]]),
        ([[2, 11, 2, 6], [3, 10, 9, 4], [8, 6, 6, 6], [10, 13, 15, 13]], True, [[2, 11, 2, 6], [3, 10, 9, 4], [8, 6, 6, 6], [10, 13, 15, 13]], [[0, 9, 0, 4], [0, 7, 6, 1], [2, 0, 0, 0], [0, 3, 5, 3]]),
        ([[2, 11, 2, 1], [3, 10, 3, 4], [8, 6, 6, 2], [11, 13, 15, 13]], True, [[2, 11, 2, 1], [3, 10, 3, 4], [8, 6, 6, 2], [11, 13, 15, 13]], [[1, 8, 1, 0], [0, 5, 0, 1], [6, 2, 4, 0], [0, 0, 4, 2]]),
        ([[4, 9, 8], [6, 7, 5], [4, 6, 9]], True, [[4, 9, 8], [6, 7, 5], [4, 6, 9]], [[0, 3, 4], [1, 0, 0], [0, 0, 5]]),
        ([[4, 3, 8], [6, 7, 5], [4, 6, 9], [5, 7, 4]], True, [[4, 3, 8, 0], [6, 7, 5, 0], [4, 6, 9, 0], [5, 7, 4, 0]], [[0, 0, 4, 0], [2, 4, 1, 0], [0, 3, 5, 0], [1, 4, 0, 0]]),
        ([[4, 9, 8], [6, 7, 5], [4, 6, 9], [5, 7, 4]], True, [[4, 9, 8, 0], [6, 7, 5, 0], [4, 6, 9, 0], [5, 7, 4, 0]], [[0, 3, 4, 0], [2, 1, 1, 0], [0, 0, 5, 0], [1, 1, 0, 0]]),
        ([[4, 9, 8, 5], [6, 7, 5, 8], [4, 6, 9, 6]], True, [[4, 9, 8, 5], [6, 7, 5, 8], [4, 6, 9, 6], [0, 0, 0, 0]], [[0, 5, 4, 1], [1, 2, 0, 3], [0, 2, 5, 2], [0, 0, 0, 0]]),
        ([[4, 9, 8, 5], [6, 7, 5, 8], [4, 6, 1, 6]], True, [[4, 9, 8, 5], [6, 7, 5, 8], [4, 6, 1, 6], [0, 0, 0, 0]], [[0, 5, 4, 1], [1, 2, 0, 3], [3, 5, 0, 5], [0, 0, 0, 0]]),
        ([[2, 11, 2, 6], [3, 10, 9, 4], [8, 6, 6, 6], [10, 13, 15, 13]], False, [[13, 4, 13, 9], [12, 5, 6, 11], [7, 9, 9, 9], [5, 2, 0, 2]], [[9, 0, 9, 3], [7, 0, 1, 4], [0, 2, 2, 0], [5, 2, 0, 0]]),
        ([[2, 11, 2, 6], [3, 10, 9, 4], [8, 6, 6, 6], [18, 13, 15, 13]], False, [[16, 7, 16, 12], [15, 8, 9, 14], [10, 12, 12, 12], [0, 5, 3, 5]], [[9, 0, 8, 3], [7, 0, 0, 4], [0, 2, 1, 0], [0, 5, 2, 3]]),
        ([[4, 9, 8], [6, 7, 5], [4, 6, 9], [5, 7, 4]], False, [[5, 0, 1, 0], [3, 2, 4, 0], [5, 3, 0, 0], [4, 2, 5, 0]], [[2, 0, 1, 0], [0, 2, 4, 0], [2, 3, 0, 0], [1, 2, 5, 0]]),
        ([[4, 7, 8], [6, 7, 5], [4, 6, 9], [5, 7, 4]], False, [[5, 2, 1, 0], [3, 2, 4, 0], [5, 3, 0, 0], [4, 2, 5, 0]], [[2, 0, 1, 0], [0, 0, 4, 0], [2, 1, 0, 0], [1, 0, 5, 0]])
    ])
    def test_should_subtract_min_values_in_every_row_and_column_in_cost_matrix(
        self, costs, is_min, norm_costs, expected_costs
    ):
        costs = np.array(costs)
        norm_costs = np.array(norm_costs)
        problem = AssignmentProblem("test_model", costs, is_min)
        norm_problem = NormalizedAssignmentProblem(norm_costs, problem)

        solver = Solver.__new__(Solver)
        solver.problem = norm_problem

        solver.extracts_mins(solver.problem.costs)

        assert np.array_equal(
            solver.problem.costs, expected_costs
        ), "min values are not extracted properly:" +\
            f"\n- got cost matrix: {indented_string(str(solver.problem.costs))}" +\
            f"\n- expected: {indented_string(str(expected_costs))}" +\
            f"\n- from initial cost matrix: {indented_string(str(problem.costs))}"


    @pytest.mark.parametrize("costs, is_min, norm_costs, exp_partial_assignment", [
        ([[4, 9, 8], [6, 7, 5], [4, 6, 1]], True, [[0, 3, 4], [1, 0, 0], [3, 3, 0]], {0: 0, 2: 2, 1: 1}),
        ([[2, 11, 2, 6], [3, 10, 9, 4], [8, 6, 6, 6], [10, 13, 15, 13]], True, [[0, 9, 0, 4], [0, 7, 6, 1], [2, 0, 0, 0], [0, 3, 5, 3]], {1: 0, 0: 2, 2: 1}),
        ([[2, 11, 2, 1], [3, 10, 3, 4], [8, 6, 6, 2], [11, 13, 15, 13]], True, [[1, 8, 1, 0], [0, 5, 0, 1], [6, 2, 4, 0], [0, 0, 4, 2]], {0: 3, 1: 2, 3: 0}),
        ([[4, 9, 8], [6, 7, 5], [4, 6, 9]], True, [[0, 3, 4], [1, 0, 0], [0, 0, 5]], {0: 0, 2: 1, 1: 2}),
        ([[4, 3, 8], [6, 7, 5], [4, 6, 9], [5, 7, 4]], True, [[0, 0, 4, 0], [2, 4, 1, 0], [0, 3, 5, 0], [1, 4, 0, 0]], {1: 3, 2: 0, 0: 1, 3: 2}),
        ([[4, 9, 8], [6, 7, 5], [4, 6, 9], [5, 7, 4]], True, [[0, 3, 4, 0], [2, 1, 1, 0], [0, 0, 5, 0], [1, 1, 0, 0]], {1: 3, 0: 0, 2: 1, 3: 2}),
        ([[4, 9, 8, 5], [6, 7, 5, 8], [4, 6, 9, 6]], True, [[0, 5, 4, 1], [1, 2, 0, 3], [0, 2, 5, 2], [0, 0, 0, 0]], {0: 0, 1: 2, 3: 1}),
        ([[4, 9, 8, 5], [6, 7, 5, 8], [4, 6, 1, 6]], True, [[0, 5, 4, 1], [1, 2, 0, 3], [3, 5, 0, 5], [0, 0, 0, 0]], {0: 0, 1: 2, 3: 1}),
        ([[2, 11, 2, 6], [3, 10, 9, 4], [8, 6, 6, 6], [10, 13, 15, 13]], False, [[9, 0, 9, 3], [7, 0, 1, 4], [0, 2, 2, 0], [5, 2, 0, 0]], {0: 1, 2: 0, 3: 2}),
        ([[2, 11, 2, 6], [3, 10, 9, 4], [8, 6, 6, 6], [18, 13, 15, 13]], False, [[9, 0, 8, 3], [7, 0, 0, 4], [0, 2, 1, 0], [0, 5, 2, 3]], {0: 1, 1: 2, 3: 0, 2: 3}),
        ([[4, 9, 8], [6, 7, 5], [4, 6, 9], [5, 7, 4]], False, [[2, 0, 1, 0], [0, 2, 4, 0], [2, 3, 0, 0], [1, 2, 5, 0]], {3: 3, 0: 1, 1: 0, 2: 2}),
        ([[4, 7, 8], [6, 7, 5], [4, 6, 9], [5, 7, 4]], False, [[2, 0, 1, 0], [0, 0, 4, 0], [2, 1, 0, 0], [1, 0, 5, 0]], {0: 1, 3: 3, 1: 0, 2: 2})
    ])
    def test_should_find_partial_assignment_in_cost_matrix(
        self, costs, is_min, norm_costs, exp_partial_assignment
    ):
        costs = np.array(costs)
        norm_costs = np.array(norm_costs)
        problem = AssignmentProblem("test_model", costs, is_min)
        norm_problem = NormalizedAssignmentProblem(np.copy(norm_costs), problem)

        solver = Solver.__new__(Solver)
        solver.problem = norm_problem


        partial_assignment = solver.find_max_assignment(solver.problem.costs)

        assert partial_assignment == exp_partial_assignment, f"partial assignment is incorrect:" +\
                f"\n- got: {partial_assignment}" +\
                f"\n- expected: {exp_partial_assignment}" +\
                f"\n- for cost matrix: {indented_string(str(norm_costs))}" +\
                f"\ntip. remember that smaller index wins ties"


    @pytest.mark.parametrize("costs, is_min, start_costs, partial_assignment, exp_costs", [
        ([[2, 11, 2, 6], [3, 10, 9, 4], [8, 6, 6, 6], [10, 13, 15, 13]], True, [[0, 9, 0, 4], [0, 7, 6, 1], [2, 0, 0, 0], [0, 3, 5, 3]], {1: 0, 0: 2, 2: 1}, [[1, 9, 0, 4], [0, 6, 5, 0], [3, 0, 0, 0], [0, 2, 4, 2]]),
        ([[2, 11, 2, 1], [3, 10, 3, 4], [8, 6, 6, 2], [11, 13, 15, 13]], True, [[1, 8, 1, 0], [0, 5, 0, 1], [6, 2, 4, 0], [0, 0, 4, 2]], {0: 3, 1: 2, 3: 0}, [[0, 7, 0, 0], [0, 5, 0, 2], [5, 1, 3, 0], [0, 0, 4, 3]]),
        ([[4, 9, 8, 5], [6, 7, 5, 8], [4, 6, 9, 6]], True, [[0, 5, 4, 1], [1, 2, 0, 3], [0, 2, 5, 2], [0, 0, 0, 0]], {0: 0, 1: 2, 3: 1}, [[0, 4, 3, 0], [2, 2, 0, 3], [0, 1, 4, 1], [1, 0, 0, 0]]),
        ([[4, 9, 8, 5], [6, 7, 5, 8], [4, 6, 1, 6]], True, [[0, 5, 4, 1], [1, 2, 0, 3], [3, 5, 0, 5], [0, 0, 0, 0]], {0: 0, 1: 2, 3: 1}, [[0, 5, 5, 1], [0, 1, 0, 2], [2, 4, 0, 4], [0, 0, 1, 0]]),
        ([[4, 9, 8, 5], [6, 7, 5, 8], [4, 6, 1, 6]], True, [[0, 5, 5, 1], [0, 1, 0, 2], [2, 4, 0, 4], [0, 0, 1, 0]], {0: 0, 1: 2, 3: 1}, [[0, 4, 5, 0], [0, 0, 0, 1], [2, 3, 0, 3], [1, 0, 2, 0]]),
        ([[2, 11, 2, 6], [3, 10, 9, 4], [8, 6, 6, 6], [10, 13, 15, 13]], False, [[9, 0, 9, 3], [7, 0, 1, 4], [0, 2, 2, 0], [5, 2, 0, 0]], {0: 1, 2: 0, 3: 2}, [[8, 0, 8, 2], [6, 0, 0, 3], [0, 3, 2, 0], [5, 3, 0, 0]])
    ])
    def test_should_perform_crossing_algorithm_on_cost_matrix(
        self, costs, is_min, start_costs, partial_assignment, exp_costs
    ):
        costs = np.array(costs)
        start_costs = np.array(start_costs)
        exp_costs = np.array(exp_costs)
        problem = AssignmentProblem("test_model", costs, is_min)
        norm_problem = NormalizedAssignmentProblem(np.copy(start_costs), problem)

        solver = Solver.__new__(Solver)
        solver.problem = norm_problem

        solver.add_zero_by_crossing_out(solver.problem.costs, partial_assignment)
                
        assert np.array_equal(
            solver.problem.costs, exp_costs
        ), "crossing algorithm is not performed properly:" +\
            f"\n- got: {indented_string(str(solver.problem.costs))}" +\
            f"\n- expected: {indented_string(str(exp_costs))}" +\
            f"\n- for cost matrix: {indented_string(str(start_costs))}" +\
            f"\n- and partial assignment: {partial_assignment}"

    @pytest.mark.parametrize("costs, is_min, norm_costs, assignment, exp_objective", [
        ([[4, 9, 8], [6, 7, 5], [4, 6, 1]], True, [[4, 9, 8], [6, 7, 5], [4, 6, 1]], {0: 0, 2: 2, 1: 1}, 12),
        ([[2, 11, 2, 6], [3, 10, 9, 4], [8, 6, 6, 6], [10, 13, 15, 13]], True, [[2, 11, 2, 6], [3, 10, 9, 4], [8, 6, 6, 6], [10, 13, 15, 13]], {0: 2, 3: 0, 1: 3, 2: 1}, 22),
        ([[2, 11, 2, 1], [3, 10, 3, 4], [8, 6, 6, 2], [11, 13, 15, 13]], True, [[2, 11, 2, 1], [3, 10, 3, 4], [8, 6, 6, 2], [11, 13, 15, 13]], {2: 3, 0: 2, 1: 0, 3: 1}, 20),
        ([[4, 9, 8], [6, 7, 5], [4, 6, 9]], True, [[4, 9, 8], [6, 7, 5], [4, 6, 9]], {0: 0, 2: 1, 1: 2}, 15),
        ([[4, 3, 8], [6, 7, 5], [4, 6, 9], [5, 7, 4]], True, [[4, 3, 8, 0], [6, 7, 5, 0], [4, 6, 9, 0], [5, 7, 4, 0]], {1: 3, 2: 0, 0: 1, 3: 2}, 11),
        ([[4, 9, 8], [6, 7, 5], [4, 6, 9], [5, 7, 4]], True, [[4, 9, 8, 0], [6, 7, 5, 0], [4, 6, 9, 0], [5, 7, 4, 0]], {1: 3, 0: 0, 2: 1, 3: 2}, 14),
        ([[4, 9, 8, 5], [6, 7, 5, 8], [4, 6, 9, 6]], True, [[4, 9, 8, 5], [6, 7, 5, 8], [4, 6, 9, 6], [0, 0, 0, 0]], {1: 2, 2: 0, 0: 3, 3: 1}, 14),
        ([[4, 9, 8, 5], [6, 7, 5, 8], [4, 6, 1, 6]], True, [[4, 9, 8, 5], [6, 7, 5, 8], [4, 6, 1, 6], [0, 0, 0, 0]], {2: 2, 0: 0, 1: 1, 3: 3}, 12),
        ([[2, 11, 2, 6], [3, 10, 9, 4], [8, 6, 6, 6], [10, 13, 15, 13]], False, [[13, 4, 13, 9], [12, 5, 6, 11], [7, 9, 9, 9], [5, 2, 0, 2]], {0: 1, 1: 2, 3: 3, 2: 0}, 41),
        ([[2, 11, 2, 6], [3, 10, 9, 4], [8, 6, 6, 6], [18, 13, 15, 13]], False, [[16, 7, 16, 12], [15, 8, 9, 14], [10, 12, 12, 12], [0, 5, 3, 5]], {0: 1, 1: 2, 3: 0, 2: 3}, 44),
        ([[4, 9, 8], [6, 7, 5], [4, 6, 9], [5, 7, 4]], False, [[5, 0, 1, 0], [3, 2, 4, 0], [5, 3, 0, 0], [4, 2, 5, 0]], {3: 3, 0: 1, 1: 0, 2: 2}, 24),
        ([[4, 7, 8], [6, 7, 5], [4, 6, 9], [5, 7, 4]], False, [[5, 2, 1, 0], [3, 2, 4, 0], [5, 3, 0, 0], [4, 2, 5, 0]], {0: 1, 3: 3, 1: 0, 2: 2}, 22)
    ])
    def test_should_create_proper_assignment_based_on_dict_of_assignments(
        self, costs, is_min, norm_costs, assignment, exp_objective
    ):
        costs = np.array(costs)
        norm_costs = np.array(norm_costs)
        problem = AssignmentProblem("test_model", costs, is_min)
        norm_problem = NormalizedAssignmentProblem(np.copy(norm_costs), problem)

        solver = Solver.__new__(Solver)
        solver.problem = norm_problem

        out_assignment = solver.create_assignment(assignment)

        assert (
            out_assignment.objective == exp_objective
        ), f"hungarian algorithm returns incorrect objective:" +\
            f"\n- got: {out_assignment.objective}" +\
            f"\n- expected: {exp_objective}" +\
            f"\n- for cost matrix: {indented_string(str(problem.costs))}" +\
            f"\n- and assignment: {out_assignment.assigned_tasks}" 

        assert isinstance(out_assignment.assigned_tasks, list), \
            f"the assigned tasks are expected to be returned as a list:" +\
            f"\n- got: {out_assignment.assigned_tasks} of type: `{type(out_assignment.assigned_tasks).__name__}`"
        meta_inf = f"\n- got assignment: {out_assignment.assigned_tasks}" +\
            f"\n- for cost matrix: {indented_string(str(problem.costs))}"
        assert len(out_assignment.assigned_tasks) >= problem.n_workers(), \
            "the assignment seems to miss a worker:" + meta_inf
        assert len(out_assignment.assigned_tasks) <= problem.n_workers(), \
            "the assignment seems to use non-existing workers:" + meta_inf
        assert max(out_assignment.assigned_tasks) <= problem.n_tasks(), \
            "the assignment seems to assing a non-existing task" + meta_inf
