from saport.simplex.model import Model 
from saport.simplex.tableaux import Tableaux
import numpy as np

def model_1():
        m = Model("case 1")
        x1 = m.create_variable("x1")
        x2 = m.create_variable("x2")
        x3 = m.create_variable("x3")
        m.add_constraint(x1 + x2 <= 5)
        m.add_constraint(x1 - x2 + x3 == 1)
        m.add_constraint(x2 - x3 >= 3)
        m.maximize(x1 + x2 + x3)
        return m
    
def augmented_1():
    m = Model("augmented 1")
    x1 = m.create_variable("x1")
    x2 = m.create_variable("x2")
    x3 = m.create_variable("x3")
    s1 = m.create_variable("s1")
    s2 = m.create_variable("s2")
    m.add_constraint(x1 + x2 + s1 == 5)
    m.add_constraint(x1 - x2 + x3 == 1)
    m.add_constraint(x2 - x3 - s2 == 3)
    m.maximize(x1 + x2 + x3)
    return m

def tableaux_1():
    return Tableaux(augmented_1(), np.array([[-1., -1., -1.,  0.,  0.,  0.],
                                             [ 1.,  1.,  0.,  1.,  0.,  5.],
                                             [ 1., -1.,  1.,  0.,  0.,  1.],
                                             [ 0.,  1., -1.,  0., -1.,  3.]]))

def model_2():
    m = Model("case 2")
    x1 = m.create_variable("x1")
    x2 = m.create_variable("x2")
    x3 = m.create_variable("x3")
    m.add_constraint(x1 - x2 <= -5)
    m.add_constraint(x1 - x2 - x3 == -1)
    m.add_constraint(x2 + x3 >= -3)
    m.minimize(x1 + x2 + x3)
    m.simplify()
    return m

def augmented_2():
    m = Model("augmented 2")
    x1 = m.create_variable("x1")
    x2 = m.create_variable("x2")
    x3 = m.create_variable("x3")
    s1 = m.create_variable("s1")
    s2 = m.create_variable("s2")
    m.add_constraint(-x1 + x2 - s1 == 5)
    m.add_constraint(-x1 + x2 + x3  == 1)
    m.add_constraint(-x2 - x3 + s2 == 3)
    m.maximize(-x1 - x2 - x3)
    m.simplify()
    return m

def tableaux_2():
    return Tableaux(augmented_2(), np.array([[ 1.,  1.,  1.,  0.,  0.,  0.],
                                             [-1.,  1.,  0., -1.,  0.,  5.],
                                             [-1.,  1.,  1.,  0.,  0.,  1.],
                                             [ 0., -1., -1.,  0., 1.,  3.]]))