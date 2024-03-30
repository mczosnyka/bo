from saport.assignment.model import AssignmentProblem, NormalizedAssignmentProblem
from tests.common_test_utils import indented_string
import numpy as np
import pytest 

class TestModel:

    @pytest.mark.parametrize("costs, is_min, norm_costs", [
        ([[2, 11, 2, 6], [3, 10, 9, 4], [8, 6, 6, 6], [10, 13, 15, 13]], False, [[13, 4, 13, 9], [12, 5, 6, 11], [7, 9, 9, 9], [5, 2, 0, 2]]),
        ([[2, 11, 2, 6], [3, 10, 9, 4], [8, 6, 6, 6], [18, 13, 15, 13]], False, [[16, 7, 16, 12], [15, 8, 9, 14], [10, 12, 12, 12], [0, 5, 3, 5]]),
        ([[4, 9, 8], [6, 7, 5], [4, 6, 1]], True, [[4, 9, 8], [6, 7, 5], [4, 6, 1]]),
        ([[2, 11, 2, 6], [3, 10, 9, 4], [8, 6, 6, 6], [10, 13, 15, 13]], True, [[2, 11, 2, 6], [3, 10, 9, 4], [8, 6, 6, 6], [10, 13, 15, 13]]),
        ([[2, 11, 2, 1], [3, 10, 3, 4], [8, 6, 6, 2], [11, 13, 15, 13]], True, [[2, 11, 2, 1], [3, 10, 3, 4], [8, 6, 6, 2], [11, 13, 15, 13]]),
        ([[4, 9, 8], [6, 7, 5], [4, 6, 9]], True, [[4, 9, 8], [6, 7, 5], [4, 6, 9]])
    ])
    def test_maximization_problem_should_be_converted_to_minimization_problem(self, costs, is_min, norm_costs):
        costs = np.array(costs)
        norm_costs = np.array(norm_costs)
        problem = AssignmentProblem("test_model", costs, is_min)
        norm_problem = NormalizedAssignmentProblem.from_problem(problem=problem)

        assert np.array_equal(
            norm_problem.costs, norm_costs
        ), "maximization problem is not correctly normalized:" +\
            f"\n- got cost matrix: {indented_string(str(norm_problem.costs))}" +\
            f"\n- expected: {indented_string(str(norm_costs))}" +\
            f"\n- from initial cost matrix: {indented_string(str(costs))}" +\
            f"\n- and the original goal was '{'minimization' if is_min else 'maximization'}'"

    @pytest.mark.parametrize("costs, norm_costs", [
        ([[4, 3, 8], [6, 7, 5], [4, 6, 9], [5, 7, 4]],[[4.0, 3.0, 8.0, 0.0], [6.0, 7.0, 5.0, 0.0], [4.0, 6.0, 9.0, 0.0], [5.0, 7.0, 4.0, 0.0]]),
        ([[4, 9, 8], [6, 7, 5], [4, 6, 9], [5, 7, 4]],[[4.0, 9.0, 8.0, 0.0], [6.0, 7.0, 5.0, 0.0], [4.0, 6.0, 9.0, 0.0], [5.0, 7.0, 4.0, 0.0]]),
        ([[4, 9, 8, 5], [6, 7, 5, 8], [4, 6, 9, 6]],[[4.0, 9.0, 8.0, 5.0], [6.0, 7.0, 5.0, 8.0], [4.0, 6.0, 9.0, 6.0], [0.0, 0.0, 0.0, 0.0]]),
        ([[4, 9, 8, 5], [6, 7, 5, 8], [4, 6, 1, 6]],[[4.0, 9.0, 8.0, 5.0], [6.0, 7.0, 5.0, 8.0], [4.0, 6.0, 1.0, 6.0], [0.0, 0.0, 0.0, 0.0]])
    ])
    def test_rectangular_problem_should_be_padded_with_zeros_to_make_it_square(
        self, costs, norm_costs
    ):
        costs = np.array(costs)
        norm_costs = np.array(norm_costs)
        problem = AssignmentProblem("test_model", costs, True)
        norm_problem = NormalizedAssignmentProblem.from_problem(problem=problem)
        
        meta_info = f"\n- got cost matrix: {indented_string(str(norm_problem.costs))}" +\
            f"\n- expected: {indented_string(str(norm_costs))}" +\
            f"\n- from initial cost matrix: {indented_string(str(problem.costs))}"

        assert norm_problem.costs is not None, \
            "the normalized costs matrix should not be `None`" + meta_info

        assert norm_problem.costs.shape == norm_costs.shape, \
            "the normalized costs matrix should be square and big enough" + meta_info
        
        assert np.array_equal(
            norm_problem.costs, norm_costs
        ), "the extra rows/cols should contain zeros:" + meta_info


