from typing import List, Tuple
from saport.simplex.model import Model 
from saport.simplex.solver import Solver
from saport.simplex.tableaux import Tableaux
from saport.simplex.expressions.expression import Variable
from saport.simplex.expressions.constraint import Constraint, ConstraintType
from saport.simplex.expressions.objective import ObjectiveType
from copy import deepcopy
import numpy as np
from tests.cases import model_1, model_2, augmented_1, augmented_2, tableaux_1, tableaux_2
import pytest


class TestAugmentation:


    @pytest.mark.parametrize("input,expected", [(model_1(), augmented_1()), (model_2(), augmented_2())])
    def test_augment_model(self, input: Model, expected: Model):
        solver = Solver()
        result = solver._augment_model(input)
        result_constr_n = len(result.constraints)
        expect_constr_n = len(expected.constraints)
        assert result_constr_n == expect_constr_n, f"number of constraints should not be changed - got {result_constr_n}, expected: {expect_constr_n}" 
        
        result_var_n = len(result.variables)
        expect_var_n = len(expected.variables)
        assert result_var_n == expect_var_n, f"augmentation should add correct amount of slack/surplus variables - got {result_var_n}, expected: {expect_var_n}"        
        assert result.objective.type == ObjectiveType.MAX, f"augmentation should modify the objective to be of type 'max'"
        assert expected.objective.expression.is_equivalent(result.objective.expression, expected), f"objective is not augmented correctly - got: {result.objective.expression}, expected {expected.objective.expression}"
        for c in result.constraints:
            assert c.bound >= 0, f"augmented model has only non-negative bounds - got constraint {c}"
            assert c.type == ConstraintType.EQ, f"augmented constraints are always of type '==' - got constraint {c}"
            
            def sorted_coeffs(constraint: Constraint) -> bool:
                input_var_n = len(input.variables)
                coeffs = c.expression.coefficients(expected)
                return coeffs[:input_var_n] + sorted(coeffs[input_var_n:])
            
            assert any([sorted_coeffs(ec) == sorted_coeffs(c) for ec in expected.constraints]), f"constraint is not augmented correctly {c.expression.coefficients(expected)}"
            
    @pytest.mark.parametrize("input,expected", [(augmented_1(), tableaux_1()), (augmented_2(), tableaux_2())])        
    def test_basic_initial_tableaux(self, input: Model, expected:Tableaux):
        solver = Solver()
        result = solver._basic_initial_tableaux(input)
        assert result.table is not None, f"the initial table in `Tableaux` should not be `None` for model:\n{input}"
        assert result.table.shape == expected.table.shape, f"the initial tableaux has incorrect shape - got: {result.table.shape}, expected: {expected.table.shape} for model:\n{input}"
        assert np.allclose(result.table, expected.table), f"the initial tablaux is incorrect - got:\n{result.table}expected:\n{expected.table} for model:\n{input}"

