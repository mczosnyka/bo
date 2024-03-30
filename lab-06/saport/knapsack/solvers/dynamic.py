from ..solver import Solver
from ..model import Solution, Item
import numpy as np
from typing import List



class DynamicSolver(Solver):
    """
    A naive dynamic programming solver for the knapsack problem.
    """

    def _create_table(self) -> np.ndarray:
        # TODO: fill the table!
        # tip 1. init table using np.zeros function (replace `None``)
        # tip 2. remember to handle timeout (refer to the dfs solver for an example)
        #        - just return the current state of the table
        items = self.problem.items.copy()
        table = np.zeros((self.problem.capacity + 1, len(self.problem.items) + 1))
        for i in items:
            for j in range(self.problem.capacity + 1):
                if i.weight > j:
                    table[j][i.index + 1] = table[j][i.index]
                elif i.weight <= j:
                    table[j][i.index + 1] = max(table[j - i.weight][i.index] + i.value, table[j][i.index])
        return table

    def _extract_solution(self, table: np.ndarray) -> Solution:
        used_items: List[Item] = []
        optimal = table[-1, -1] > 0
        # height = table.shape[0] - 1
        length = table.shape[1] - 1
        cap = self.problem.capacity
        j = 0
        while length - j - 1 >= 0 and cap > 0:
            if table[cap, length - j] != table[cap, length - j - 1]:
                used_items.append(self.problem.items[length - j - 1])
                cap -= self.problem.items[length - j - 1].weight
            j += 1
        # TODO: fill in the `used_items` list using info from the table!

        return Solution.from_items(used_items, optimal)

    def solve(self) -> Solution:
        self.interrupted = False
        self.start_timer()

        table = self._create_table()
        solution = self._extract_solution(table) if table is not None else Solution.empty()

        self.stop_timer()
        return solution
