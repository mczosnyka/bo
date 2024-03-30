import logging
from saport.simplex.model import Model 

def create_model() -> Model:
    model = Model(__file__)

    #TODO:
    # fill missing test based on the example_01_solvable.py
    # to make the test a bit more interesting:
    # * minimize the objective (so the solver would have to normalize it)
    # * make some ">=" constraints (GE)
    # * the model still has to be solvable by the basix simplex withour artificial var

    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")

    model.add_constraint(x1 >= -100)
    model.add_constraint(x2 <= 150)
    model.add_constraint(2 * x1 + x2 <= 500)

    model.minimize(5 * x1 + 10 * x2)



    return model 

def run():
    model = create_model()
    #TODO:
    # add a test "assert something" based on the example_01_solvable.py
    # TIP: you may use other solvers (e.g. https://online-optimizer.appspot.com)
    #      to find the correct solution

    try:
        solution = model.solve()
    except:
        raise AssertionError("This problem has a solution and your algorithm hasn't found it!")

    logging.info(solution)
    assert (solution.assignment(model) == [0.0, 0.0]), "Your algorithm found an incorrect solution!"


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run()
