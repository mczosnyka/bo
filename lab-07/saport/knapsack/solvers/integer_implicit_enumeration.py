from saport.knapsack.solver import Solver
from saport.knapsack.model import Problem, Solution, Item
from typing import List
from saport.integer.model import BooleanModel
from saport.integer.solvers.implicit_enumeration import ImplicitEnumerationSolver
from saport.simplex.expressions.expression import Expression


class IntegerImplicitEnumerationSolver(Solver):
    """
    An Integer Programming solver for the knapsack problems

    Methods:
    --------
    _create_model() -> Model:
        creates and returns an integer programming model based on the self.problem
    """
    def _create_model(self) -> BooleanModel:
        m = BooleanModel('knapsack')
        # TODO:
        # - variables: whether the item gets taken
        # - constraints: weights
        # - objective: values
        variable_weights = []
        variable_values = []
        for i in self.problem.items:
            m.create_variable(f'{i}')
            variable_weights.append(i.weight)
            variable_values.append(i.value)
        m.add_constraint(Expression.from_vectors(m.variables, variable_weights) <= self.problem.capacity)
        m.maximize(Expression.from_vectors(m.variables, variable_values))
        return m
        return m

    def solve(self) -> Solution:
        m = self._create_model()
        solver = ImplicitEnumerationSolver()
        integer_solution = solver.solve(m, self.timelimit)
        items = [item for (i, item) in enumerate(self.problem.items) if integer_solution.value(m.variables[i]) > 0]
        solution = Solution.from_items(items, not solver.interrupted)
        return solution