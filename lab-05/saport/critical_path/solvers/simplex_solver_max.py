from ..model import Project
from ..project_network import ProjectNetwork
from ...simplex.model import Model
from ...simplex.expressions.expression import Expression
from ..solution import BasicSolution


class Solver:
    '''
    Simplex based solver looking for the critical path in the project.
    Uses linear model maximizing length of the path in the project network. 

    Attributes:
    ----------
    project_network: ProjectNetwork
        a project network related to the given project
    model: simplex.model.Model
        a linear model looking for the maximal path in the project network
    Methods:
    --------
    __init__(problem: Project)
        create a solver for the given project
    create_model() -> simplex.model.Model
        builds a linear model of the problem
    solve() -> BasicSolution
        finds the duration of the critical (longest) path in the project network
    '''
    def __init__(self, problem: Project):
        self.project_network = ProjectNetwork(problem)
        self.model = self.create_model()

#     def create_model(self) -> Model:
#         # TODO:
#         model = Model("critical path (max)")
#         max_model = []
#         variables = {}
#         for i in self.project_network.edges():
#             variables[(i[0], i[1])] = model.create_variable(f"x{i[0]}{i[1]}")
#             model.add_constraint(variables[(i[0], i[1])] <= 1)
#             max_model.append(self.project_network.arc_duration(i[0], i[1]) * variables[(i[0], i[1])])
#
#         sum_start = []
#         for i in self.project_network.successors(self.project_network.start_node):
#             sum_start.append(variables[(self.project_network.start_node, i)])
#         model.add_constraint(sum(sum_start) == 1)
#         sum_goal = []
#         for i in self.project_network.predecessors(self.project_network.goal_node):
#             sum_goal.append(variables[(i, self.project_network.goal_node)])
#         model.add_constraint(sum(sum_goal) == 1)
#         suma = []
#         for i in self.project_network.normal_nodes():
#             for j in self.project_network.successors(i):
#                 for k in self.project_network.predecessors(i):
#                     suma.append(variables[(k, i)])
#                 suma.append(-variables[(i, j)])
#             model.add_constraint(sum(suma) == 0)
#             # suma.clear()
# #chuj
#         model.maximize(sum(max_model))
#
#
#         # 0) we need as many variables as there are edges in the project network
#         # 1) every variable has to be <= 1
#         # 2) sum of the variables starting at the initial state has to be equal 1
#         # 3) sum of the variables ending at the goal state has to be equal 1
#         # 4) for every other node, total flow going trough it has to be equal 0
#         #    i.e. sum of incoming arcs minus sum of the outgoing arcs = 0
#         # 5) we have to maximize length of the path
#         #    (sum of variables weighted by the durations of the corresponding tasks)
#         #
#         # tip 1. `self.project_network` is the project network you should use
#         #        - read documentation of ProjectNetwork class in
#         #          `saport/critical_path/project_network.py` for guidance
#
#
#         return model
    def create_model(self) -> Model:
        model = Model("critical path (max)")
        max_model = []
        variables = {}
        for i in self.project_network.edges():
            variables[(i[0], i[1])] = model.create_variable(f"x{i[0]}{i[1]}")
            model.add_constraint(variables[(i[0], i[1])] <= 1)
            max_model.append(self.project_network.arc_duration(i[0], i[1]) * variables[(i[0], i[1])])

        sum_start = []
        for i in self.project_network.successors(self.project_network.start_node):
            sum_start.append(variables[(self.project_network.start_node, i)])
        model.add_constraint(sum(sum_start) == 1)
        sum_goal = []
        for i in self.project_network.predecessors(self.project_network.goal_node):
            sum_goal.append(variables[(i, self.project_network.goal_node)])
        model.add_constraint(sum(sum_goal) == 1)
        for i in self.project_network.normal_nodes():
            suma = []
            for j in self.project_network.successors(i):
                suma.append(-variables[(i, j)])
            for j in self.project_network.predecessors(i):
                suma.append(variables[(j, i)])
            model.add_constraint(sum(suma) == 0)
            # suma.clear()

        model.maximize(sum(max_model))

        return model

    def solve(self) -> BasicSolution:
        solution = self.model.solve()
        return BasicSolution(int(solution.objective_value()))
