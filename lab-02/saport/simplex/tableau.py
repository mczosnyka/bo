from __future__ import annotations
from typing import List
from numpy.typing import ArrayLike
import numpy as np
from . import model as ssmod

"""
eps is used to avoid numerical errors, e.g.
- for float equality checks use math.isclose https://docs.python.org/3/library/math.html#math.isclose
- for inequality checks, instead of >= 0 you may just write >= -eps
"""
eps = 1e-09


class Tableau:
    """
    A class to represent a tableau to linear programming problem.

    Attributes
    ----------
    model : Model
        model corresponding to the tableau
    table : numpy.Array
        2d-array with the tableau

    Methods
    -------
    __init__(model: Model, table: array) -> Tableau:
        constructs a new tableau for the specified model and initial table
    objective_coefficients() -> numpy.Array:
        returns a vector containing coefficients in the objective row
    objective_value() -> float:
        returns the objective value of solution represented in tableau
    is_optimal() -> bool:
        checks whether the current solution is optimal
    choose_entering_variable() -> int:
        finds index of the variable, that should enter the basis next
    is_unbounded(col: int) -> bool:
        checks whether the problem is unbounded
    choose_leaving_variable(col: int) -> int:
        finds index of the variable, that should leave the basis next
    pivot(col: int, row: int):
        updates tableau using pivot operation with given entering and leaving variables
    extract_assignment() -> List[float]:
        returns assignment corresponding to the tableau
    extract_basis() -> List[int]
        returns list of indexes corresponding to the variables belonging to the basis
    """

    model: ssmod.Model
    table: ArrayLike

    def __init__(self, model: ssmod.Model, table: ArrayLike):
        self.model = model
        self.table = table

    def objective_coefficients(self) -> ArrayLike:
        return self.table[0, :-1]

    def objective(self) -> float:
        return self.table[0, -1]

    def is_optimal(self) -> bool:
        # TODO:
        # if all coefficients in the objective row are >= 0
        # tip. check the eps constant at the top of this file
        row = self.objective_coefficients()

        for c in row:
            if c < -eps:
                return False
        return True
        raise NotImplementedError()

    def choose_entering_variable(self) -> int:
        # TODO:
        # return column index with the smallest coefficient in the objective row
        row = self.objective_coefficients()
        pom = self.table[0, 0]
        i = 0
        index = 0
        for c in row:
            if c < pom:
                pom = c
                index = i
            i += 1
        return index



        raise NotImplementedError()

    def is_unbounded(self, col: int) -> bool:
        # TODO:
        # if all coefficients in the specified column are <= 0
        elements_number = len(self.table)
        for i in range(1, elements_number):
            if self.table[i, col] > eps:
                return False
        return True
        raise NotImplementedError()

    def choose_leaving_variable(self, col: int) -> int:
        # TODO:
        # return row index associated with the leaving variable
        # to choose the row, divide bound column (last column) by the specified column
        # then choose a row index associated with the smallest positive value in the result
        # tip: take care to not divide by 0 :)
        elements_number = len(self.table)
        tab = np.copy(self.table)
        for i in range(1, elements_number):
           if self.table[i, col] != 0:
              tab[i, -1] = self.table[i, -1] / self.table[i, col]
        min = float('inf')
        for i in range(1, elements_number):
            if tab[i, -1] < min and self.table[i, col] > eps:
                min = tab[i, -1]
                index = i
        return index
        raise NotImplementedError()

    def pivot(self, row: int, col: int):
        # TODO:
        # Pivot operation should transform the tableau to a form, where pivot column ('col')
        # contains only 0's with the exception of 1 in the pivot row ('row'), i.e.
        #
        #              col
        #       _ _ _ _ 0 _
        #       _ _ _ _ 0 _
        #  row  _ _ _ _ 1 _
        #       _ _ _ _ 0 _
        #
        # To achieve this goal, one has to transform tableau in a way preserving the set of solutions
        # (remember, that tableau represents a set of linear equations, we don't want to break them!).
        # Therefore one can only use following operations taught in the secondary school:
        # - multiple the row (coefficients in the equation) by scalar, e.g.
        #       4x + 5y = 4 | * 1/5 -> 4/5x + y = 4/5
        # - add one equation (optionally multiplied by scalar) to another, e.g.
        #       4x - 3y = 7
        #       2x - 1y = 3
        #       ___________ -2*
        #       0x - 5y = 1
        #
        # In other words, one can only multiple the rows of the tableau by a scalar (numpy rows
        # can be easily multiplied), or add one row (possibly multiplied by scalar) to another
        # (again, numpy supports this out of the box). There exists a fixed set of such operations
        # leading to the correct pivot.


# len(self.table[i])
        t = len(self.table)
        s = len(self.table[0])
        p = np.shape(self.table)


        a = self.table[row,col]
        for i in range(len(self.table[row])):
            self.table[row, i] = self.table[row, i] / a
        for i in range(len(self.table)):
            if i != row and self.table[i, col] != 0:
                b = self.table[i, col]
                for j in range(len(self.table[i])):
                    self.table[i,j] = self.table[i,j] - (b * self.table[row, j])
        # raise NotImplementedError()

    def extract_assignment(self) -> List[float]:
        rows_n, cols_n = self.table.shape
        assignment = [0.0 for _ in range(cols_n - 1)]
        basis = self.extract_basis()
        for r in range(1, rows_n):
            var_index = basis[r - 1]
            assignment[var_index] = self.table[r, -1]

        return assignment

    def extract_basis(self) -> List[int]:
        rows_n, cols_n = self.table.shape
        basis = [-1 for _ in range(rows_n - 1)]
        for c in range(cols_n - 1):
            column = self.table[:, c]
            belongs_to_basis = column.min() == 0.0 and column.max() == 1.0 and column.sum() == 1.0
            if belongs_to_basis:
                row = np.where(column == 1.0)[0][0]
                # [row-1] because we ignore the objective variable in the basis
                basis[row - 1] = c
        return basis

    def __str__(self) -> str:
        def cell(x: float, w: int) -> str:
            return "{0: >{1}}".format(x, w)

        objective_name = self.model.objective.name()
        basis = self.extract_basis()
        header = ["basis", objective_name] + [var.name for var in self.model.variables] + ["b"]
        longest_col = max([len(h) for h in header])

        rows = [[objective_name]] + [[self.model.variables[i].name] for i in basis]

        for i, r in enumerate(rows):
            objective_coefficient = 0.0 if i > 0 else 1.0
            r += ["{:.3f}".format(v) for v in [objective_coefficient] + list(self.table[i])]
            longest_col = max(longest_col, max([len(v) for v in r]))

        header = [cell(h, longest_col) for h in header]
        rows = [[cell(v, longest_col) for v in row] for row in rows]

        cell_sep = " | "

        result = cell_sep.join(header) + "\n"
        for row in rows:
            result += cell_sep.join(row) + "\n"
        return result
