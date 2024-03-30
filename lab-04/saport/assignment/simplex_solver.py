import numpy as np
from .model import AssignmentProblem, Assignment, NormalizedAssignmentProblem
from ..simplex.model import Model
from ..simplex.expressions.expression import Expression
from dataclasses import dataclass
from typing import List 



class Solver:
    '''
    A simplex solver for the assignment problem.

    Methods:
    --------
    __init__(problem: AssignmentProblem):
        creates a solver instance for a specific problem
    solve() -> Assignment:
        solves the given assignment problem
    '''
    def __init__(self, problem: AssignmentProblem):
        self.problem = NormalizedAssignmentProblem.from_problem(problem)

    def solve(self) -> Assignment:
        model = Model("assignment")
        # TODO:
        # 1) creates variables, one for each cost in the cost matrix
        # 2) add constraint, that sum of every row has to be equal 1
        # 3) add constraint, that sum of every col has to be equal 1
        # 4) add constraint, that every variable has to be <= 1
        # 5) create an objective expression, involving all variables weighted by their cost
        # 6) add the objective to model (minimize it!)
        #
        #  tip. model.add_constraint(Expression.from_vectors([x1,x2,x3], [3,2,1]) < 3))
        #       accepts lists as arguments and gives the same result as:
        #       model.add_constraint(3*x1 + 2*x2 + x3 < 3) 
        tab = []
        for i in range(len(self.problem.costs)):
            temp = []
            for j in range(len(self.problem.costs[i])):
                temp.append(model.create_variable(f'x{i}{j}'))
            tab.append(temp)

        for i in range(len(tab)):
            row_sum = tab[i][0]
            for j in range(1, len(tab[i])):
                row_sum += tab[i][j]
            model.add_constraint(row_sum >= 1)
            model.add_constraint(row_sum <= 1)

        for i in range(len(tab[0])):
            column_sum = tab[0][i]
            for j in range(1, len(tab)):
                column_sum += tab[j][i]
            model.add_constraint(column_sum <= 1)
            model.add_constraint(column_sum >= 1)

        for i in range(len(tab)):
            for j in range(len(tab[i])):
                model.add_constraint(tab[i][j] <= 1)
        # for i in range(len(tab)):
            # model.add_constraint(Expression.from_vectors(tab[i], self.problem.costs[i]) == 0)
        obj_expr = Expression.from_vectors(tab[0], self.problem.costs[0])
        for i in range(1, len(tab)):
            obj_expr += Expression.from_vectors(tab[i], self.problem.costs[i])
        model.minimize(obj_expr)

        solution = model.solve()


        # 1) extract assignment for the original problem from the solution object
        # tips:
        # - remember that in the original problem n_workers() not alwyas equals n_tasks()
        assigned_tasks = []
        org_objective = 0
        t = np.reshape(solution.assignment(), self.problem.costs.shape)
        for i in range(len(self.problem.original_problem.costs)):
            check = False
            for j in range(len(self.problem.original_problem.costs[0])):
                if t[i][j] == 1:
                    check = True
                    assigned_tasks.append(j)
                    org_objective += self.problem.original_problem.costs[i][j]
                    break
            if check is not True:
                assigned_tasks.append(-1)





        return Assignment(assigned_tasks, org_objective)



