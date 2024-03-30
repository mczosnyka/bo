from saport.simplex.expressions.expression import Expression
from saport.simplex.model import Model

#TODO:
# Model assignments from assignment.pdf
# tip 1. you may use an external solver to check if your models reach correct optima
# tip 2. external solver available on-line: https://online-optimizer.appspot.com/?model=builtin:default.mod 

def assignment_1():
    model = Model("Assignment 1")

    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")
    x3 = model.create_variable("x3")

    model.add_constraint((x1+x2+x3) <= 30)
    model.add_constraint((x1+2*x2+x3) >= 10)
    model.add_constraint((2*x2+x3) <= 20)
    model.maximize(2*x1+x2+3*x3)

    print("Before solving:")
    print(model)

    solution = model.solve()
    #TODO:
    # Add:
    # - variables
    # - constraints
    # - objective
    # tip. value at optimum: 80.0
    return model

def assignment_2():
    model = Model("Assignment 2")

    p1 = model.create_variable("p1")
    p2 = model.create_variable("p2")
    p3 = model.create_variable("p3")
    p4 = model.create_variable("p4")

    model.add_constraint((0.8*p1 + 2.4*p2 + 0.9*p3 + 0.4*p4) >= 1200)
    model.add_constraint((0.6*p1 + 0.6*p2 + 0.3*p3 + 0.3*p4) >= 600)

    model.minimize(9.6 * p1 + 14.4 * p2 + 10.8 * p3 + 7.2 * p4)

    print("Before solving:")
    print(model)

    solution = model.solve()
    #TODO:
    # Add:
    # - variables
    # - constraints
    # - objective
    # tip. value at optimum: 10800.0
    return model

def assignment_3():
    model = Model("Assignment 3")

    s = model.create_variable("s")
    z = model.create_variable("z")

    model.add_constraint((5*s + 15*z) >= 50)
    model.add_constraint((20*s + 5*z) >= 40)
    model.add_constraint((15*s + 2*z) <= 60)

    model.minimize(8*s+4*z)

    print("Before solving:")
    print(model)

    solution = model.solve()

    #TODO:
    # Add:
    # - variables
    # - constraints
    # - objective
    # tip. value at optimum: 21.8181818
    return model

def assignment_4():
    model = Model("Assignment 4")

    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")
    x3 = model.create_variable("x3")
    x4 = model.create_variable("x4")
    x5 = model.create_variable("x5")

    model.add_constraint(x1+x2 >= 150)
    model.add_constraint(x1 + 2*x3 + x5 >= 200)
    model.add_constraint(2*x2 + x3 + 5*x4 + 3*x5 >= 150)

    model.minimize(20*x1+25*x2+15*x3+25*x4+20*x5)

    print("Before solving:")
    print(model)

    solution = model.solve()
    #TODO:
    # Add:
    # - variables
    # - constraints
    # - objective
    # tip. value at optimum: 4000.0
    return model