import logging
from saport.simplex.model import Model 

from saport.simplex.model import Model

def create_model() -> Model:
    model = Model("example_04_solvable_artificial")
    # TODO:
    # fill missing test based on the example_01_solvable.py
    # to make the test a bit more interesting:
    # * make sure solver has to use some artificial variables

    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")

    model.add_constraint(2 * x1 - x2 <= -1)
    model.add_constraint(x1 + x2 == 3)

    model.maximize(x1 + 3 * x2)
    return model

def run():
    model = create_model()

    try:
        solution = model.solve()
    except:
        raise AssertionError("This problem has a solution and your algorithm hasn't found it!")

    logging.info(solution)

    assert (solution.assignment(model) == [9.0, 0.0, 3.0]), "Your algorithm found an incorrect solution!"

    logging.info("Congratulations! This solution seems to be alright :)")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run()
