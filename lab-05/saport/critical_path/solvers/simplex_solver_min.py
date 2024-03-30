from ..model import Project
from ..project_network import ProjectNetwork
from ...simplex.model import Model
from ...simplex.expressions.expression import Expression
from ..solution import BasicSolution


class Solver:
    '''
    Simplex based solver looking for the critical path in the project.
    Uses linear model minimizing total duration of the project.

    Attributes:
    ----------
    project_network: ProjectNetwork
        a project network related to the given project
    model: simplex.model.Model
        a linear model looking for the quickest way to finish the project
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

    def create_model(self) -> Model:
        # TODO:
        # 0) we need as many variables as there are nodes in the project network
        # 1) for each arc in the network, difference between times at its ends has to be
        #    greater or equal duration of the task
        # 2) we have to minimize difference beetwen time of the goal node and the start node
        #
        # tip 1. `self.project_network` is the project network you should use
        #        - read documentation of ProjectNetwork class in 
        #          `saport/critical_path/project_network.py` for guidance
        model = Model("critical path (min)")
        variables = {}
        for i in self.project_network.nodes():
            variables[i] = model.create_variable(f"t{i}")
        for i in self.project_network.nodes():
            for j in self.project_network.successors(i):
                model.add_constraint(variables[j] - variables[i] >= self.project_network.arc_duration(i, j))
        model.minimize(variables[self.project_network.goal_node] - variables[self.project_network.start_node])
        return model

    def solve(self) -> BasicSolution:
        solution = self.model.solve()
        return BasicSolution(int(solution.objective_value()))
