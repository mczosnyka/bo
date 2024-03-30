from abc import ABC, abstractmethod
from typing import List
from ..solver import Solver
from ..model import Problem, Solution, Item


class Heuristic(ABC):
    """
    A knapsack problem heuristic.

    Methods:
    --------
    __call__(item : Item) -> float:
        return a value representing how much the given items is valuable to the greedy algorithm
        bigger value > earlier to take in the backpack
    """

    @abstractmethod
    def __call__(self, item: Item) -> float:
        '''Override this method, it should use info in the item to calculate its priority'''
        

class GreedySolver(Solver):
    """
    A greedy solver for the knapsack problems.

    Attributes:
        heuristics: List[Heuristic]
            list of all the heuristics that should be tried
    """
    heuristics: List[Heuristic]

    def __init__(self, problem: Problem, timelimit: int, heuristics: List[Heuristic]):
        super().__init__(problem, timelimit)
        self.heuristics = heuristics

    def _solve_using_heuristic(self, heuristic: Heuristic) -> Solution:
        # den_h = [DensityHeuristic(x) for x in self.problem.items.copy()].sort(reverse=True)
        # val_h = [ValueHeuristic(x) for x in self.problem.items].sort(reverse=True)
        # wei_h = [WeightHeuristic(x) for x in self.problem.items].sort()
        # cap = self.problem.capacity
        # cap_counter_v = 0
        # val = 0
        # items = self.problem.items.copy()
        # for i in val_h:
        #     for x in items:
        #         if x.value == i:
        #             if x.weight + cap_counter_v <= cap:
        #                 val += i
        #                 cap_counter_v += x.weight
        sorted_items = sorted(self.problem.items, key=heuristic, reverse=True)
        weight_limit = self.problem.capacity
        taken_items = []
        total_value = 0
        total_weight = 0
        for item in sorted_items:
            if total_weight + item.weight <= weight_limit:
                taken_items.append(item)
                total_value += item.value
                total_weight += item.weight

        return Solution(taken_items, total_value, total_weight, False)
        # cap_counter_d = 0
        # den = 0
        # for i in den_h:
        #     for x in items:
        #         if x.value/x.weight == i:
        #             if x.weight + cap_counter_d <= cap:
        #                 den += x.value
        #                 cap_counter_d += x.weight
        #
        # cap_counter_w = 0
        # wei = 0
        # for i in wei_h:
        #     for x in items:
        #         if x.weight == i:
        #             if cap_counter_w + i <= cap:
        #                 wei += x.value
        #                 cap_counter_w += wei
        #
        # caps = {'w' : cap_counter_w, 'd' : cap_counter_d, 'v' : cap_counter_v}
        # opt = max(val, den, wei)
        # keys = {'w' : wei, 'd' : den, 'v' : val}
        # for key, value in keys:
        #     if value == opt:
        #         key_ = key
        #         break
        # opt_w = caps[key_]
        # lists = {'w' : wei_h, 'd' : den_h, 'v' : val_h}
        #
        #
        #
        #
        # # TODO: implement the greedy solving strategy
        # #      1) sort items in the problem by the `heuristic`
        # #      2) take as many as you can
        # #      3) remember to replace the dummy solution below :)
        # # tip. don't implement sorting! Just use the "sorted" function
        # return Solution(lists[key_], opt, opt_w, True)


    def solve(self) -> Solution:
        self.start_timer()
        solutions = [self._solve_using_heuristic(h) for h in self.heuristics]
        self.stop_timer()
        return max(solutions, key=lambda s: s.value)


class DensityHeuristic(Heuristic):
    """
    Uses value/weight density of the item. 
    """
    def __call__(self, item: Item) -> float:
        # TODO: replace line below with the correct value
        return item.value/item.weight


class ValueHeuristic(Heuristic):
    """
    Uses value of the item. 
    """
    def __call__(self, item: Item) -> float:
        # TODO: replace line below with the correct value
        return item.value


class WeightHeuristic(Heuristic):
    """
    Uses weight of the item. 
    """
    def __call__(self, item: Item) -> float:
        # TODO: replace line below with the correct value
        return item.weight*-1