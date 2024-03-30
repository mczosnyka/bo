from __future__ import annotations
from typing import Dict, List

from copy import deepcopy
from . import model as ssmod 
from .expressions import constraint as ssecon
from .expressions import expression as sseexp
from .expressions import objective as sseobj
from . import solution as sssol 
from . import tableaux as sstab
import numpy as np 

class Solver:
    """
        A class to represent a simplex solver.

        Methods
        -------
        solve(model: Model) -> Tableaux:
            solves the given model and return the first solution
    """
    def solve(self, model: ssmod.Model) -> sssol.Solution:
        augmented_model = self._augment_model(model)
        tableaux = self._basic_initial_tableaux(augmented_model)
        solution = self._extract_solution(tableaux, model)
        return solution
        
    def _augment_model(self, original_model: ssmod.Model) -> ssmod.Model:
        """
            _augment_model(model: Model) -> Model:
                returns an augmented version of the given model 
        """
        # We don't want to modify the original model, so we copy it
        model = deepcopy(original_model)
        # Wa want to have simplified expressions 
        # each variable should occur only once in every expression
        model.simplify()


        if model.objective.type == sseobj.ObjectiveType.MIN:
            model.objective.invert()

        for i in range(len(model.constraints)):
            if model.constraints[i].bound < 0:
                model.constraints[i].invert()
            if model.constraints[i].type == ssecon.ConstraintType.GE:
                model.constraints[i].type = ssecon.ConstraintType.EQ
                model.constraints[i].expression -= model.create_variable("surplus"+str(i))
            if model.constraints[i].type == ssecon.ConstraintType.LE:
                model.constraints[i].type = ssecon.ConstraintType.EQ
                model.constraints[i].expression += model.create_variable("surplus" + str(i))


        # TODO:
        # 1. the augmented model is always a maximizing model
        # - if the objective is minimizing, we have to "invert" it
        #   tip 1. Objective has `type` attribute storing ObjectiveType (.MIN / .MAX) 
        #   tip 2. Objective class has an `invert` method just for this purpose
        # 2. all the bounds in the augmented model have to be positive or equal zero
        # - every constraint with a negative bound has to be "inverted"
        #   tip. Constraint class has an "invert" method just for this purpose
        # 3. add slack/surplus variables
        # - every constraint of type ConstraintType.GE needs a new surplus variable, that should be subtracted from its expression
        # - every constraint of type ConstraintType.LE needs a new slack variable, that should be added to its expression
        # tip. '-' and '+' operators are overloaded for the expression type, so you can literally add/subtract variables
        #      in Python you can also use shortcuts "-=" and "+=" ("*=" and "/=" also work, but you don't need them here)
        # - all constraints in the augmented model should be of type CosntrainType.EQ
        return model  

    def _basic_initial_tableaux(self, model: ssmod.Model) -> sstab.Tableaux:
        a = model.objective.expression * (-1)
        table1 = a.coefficients(model)
        table1.append(0)
        matrix = [table1]
        for constraint in model.constraints:
            table2 = constraint.expression.coefficients(model)
            table2.append(constraint.bound)
            matrix.append(table2)


        # TODO:
        # replace the 'None' below with a numpy array, where
        # 1) first row consists of the inverted coefficients of the objective expression 
        #    plus 0.0 in the last column
        # 2) every other row consists of the coefficitients in the corresponding constraints, 
        #    don't forget to put the constraint bound in the last column
        # tips.
        # - to invert coefficients in the expression, one can multiply it by `-1``
        # - to get coefficients one can use the `coefficients` method in the expression object 
        table = np.array(matrix)
        return sstab.Tableaux(model, table)

    def _extract_solution(self, tableaux: sstab.Tableaux, model: ssmod.Model) -> sssol.Solution:
        return sssol.Solution(model, tableaux)