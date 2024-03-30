from __future__ import annotations
import sys
from typing import Dict, List

from copy import deepcopy
import saport.simplex.model as ssmod 
import saport.simplex.expressions.objective as sseobj
import saport.simplex.expressions.constraint as ssecon
import saport.simplex.expressions.expression as sseexp
import saport.simplex.solution as sssol
import saport.simplex.tableau as sstab
import numpy as np 

class Solver:
    """
        A class to represent a simplex solver.

        Attributes:
        ______
        _slacks: Dict[Variable, Constraint]:
            contains mapping from slack variables to their corresponding constraints
        _surpluses: Dict[Variable, Constraint]:
            contains mapping from surplus variables to their corresponding constraints
    
        Methods
        -------
        solve(model: Model) -> Tableau:
            solves the given model and return the first solution
    """
    _slacks: Dict[sseexp.Variable, ssecon.Constraint]
    _surpluses: Dict[sseexp.Variable, ssecon.Constraint]

    def solve(self, model: ssmod.Model):
        normal_model = self._augment_model(model)
        tableau = self._basic_initial_tableau(normal_model)
        if self._optimize(tableau) == False:
            return sssol.Solution.unbounded(model, tableau)

        assignment = tableau.extract_assignment()
        return self._create_solution(assignment, model, tableau)

    def _optimize(self, tableau: sstab.Tableau):
        """
            _optimize(model: Tableau) -> bool:
                main simplex loop
        """
        while not tableau.is_optimal():
            pivot_col = tableau.choose_entering_variable()
            if tableau.is_unbounded(pivot_col):
                return False
            pivot_row = tableau.choose_leaving_variable(pivot_col)

            tableau.pivot(pivot_row, pivot_col)
        return True

    def _augment_model(self, original_model: ssmod.Model):
        """
            _augment_model(model: Model) -> Model:
                returns an augmented version of the given model 
        """
        model = deepcopy(original_model)
        model.simplify()
        self._change_objective_to_max(model)
        self._change_constraints_bounds_to_nonnegative(model)
        self._slacks = self._add_slack_variables(model)
        self._surpluses = self._add_surplus_variables(model)   
        return model  

    def _change_objective_to_max(self, model: ssmod.Model):
        if model.objective.type == sseobj.ObjectiveType.MIN:
            model.objective.invert()           

    def _change_constraints_bounds_to_nonnegative(self, model: ssmod.Model):
        for constraint in model.constraints:
            if constraint.bound < 0:
                constraint.invert()
    
    def _add_slack_variables(self, model: ssmod.Model) -> List[sseexp.Variable]:
        slacks: Dict[sseexp.Variable, ssecon.Constraint] = dict()

        for constraint in model.constraints:
            if constraint.type == ssecon.ConstraintType.LE:
                slack_var = model.create_variable(f"s{constraint.index}")
                slacks[slack_var] = constraint
                constraint.expression = constraint.expression + slack_var
                constraint.type = ssecon.ConstraintType.EQ
        return slacks

    def _add_surplus_variables(self, model: ssmod.Model) -> List[sseexp.Variable]:
        surpluses: Dict[sseexp.Variable, ssecon.Constraint] = dict()
        for constraint in model.constraints:
            if constraint.type == ssecon.ConstraintType.GE:
                surplus_var = model.create_variable(f"s{constraint.index}")
                surpluses[surplus_var] = constraint
                constraint.expression = constraint.expression - surplus_var
                constraint.type = ssecon.ConstraintType.EQ
        return surpluses 

    def _basic_initial_tableau(self, model: ssmod.Model):
        objective_row = np.array((-1 * model.objective.expression).coefficients(model) + [0.0])
        table = np.array([objective_row] + [c.expression.coefficients(model) + [c.bound] for c in model.constraints])
        return sstab.Tableau(model, table)

    def _create_solution(self, assignment: List[float], model: ssmod.Model, tableau: sstab.Tableau):
        return sssol.Solution.with_assignment(model, assignment, tableau)