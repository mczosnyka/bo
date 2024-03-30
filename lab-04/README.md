# Lab 04 - Assignment Problem

The goal of this is lab is to implement two algorithms to find the best assignment of tasks to workers. 

Tasks:
* fill missing code in: 
  * [ ] `saport.assignment.model.py`
  * [ ] `saport.assignment.simplex_solver.py`
  * [ ] `saport.assignment.hungarian_solver.py`

## SAPORT

SAPORT = Student's Attempt to Produce an Operation Research Toolkit

The project depends on the fairly recent numpy distribution and Python interpreter (version >= `3.9` is recommended). All depedendencies are listed in `requirements.txt`. One can install them with simple `pip install -r requirements.txt`, but using a virtual environment (e.g. virtualenv) is encouraged ([official tutorial](https://docs.python.org/3/tutorial/venv.html)). 

## Unit Tests

The `tests` folder contains unit test written using `pytest`. 

## Functional Tests

The `assignment_tests` folder contains some test instances. You may test your solvers by running: `python test.py`.
This script is **not** used in the grading process.

## GitLab Setup 

* [ ] Make sure, you have a **private** group 
  * [how to create a group](https://docs.gitlab.com/ee/user/group/#create-a-group)
* [ ] Add @bobot-is-a-bot as the new group member (role: **maintainer**)
  * [how to add a group member](https://docs.gitlab.com/ee/user/group/#add-users-to-a-group)
* [ ] Fork this project into your new **private** group
  * [how to create a fork](https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html#creating-a-fork)

## How To Submit Solutions

* [ ] Clone repository: git clone:
    ```bash 
    git clone <repository url>
    ```
* [ ] Solve the exercises 
    * remember to change only files with `#TODO` comments
* [ ] Commit your changes
    ```bash
    git add <path to the changed files>
    git commit -m <commit message>
    ```
* [ ] Push changes to the gitlab master branch
    ```bash
    git push -u origin master
    ```

The rest will be taken care of automatically. You can check the `GRADE.md` file for your grade / test results. Be aware that it may take some time (up to one hour) till this file appears / gets updated.  

## Repository Guide

```bash
.
├── README.md        # this README
├── assignment_tests # this folder contains some test cases
│   ├── ...
│   └── square_min_05_173.txt # a single test case
├── requirements.txt # package requirements - install with `pip -r requirements.txt`
├── saport
│   ├── assignment   # directory with assignment problem solver
│   │   ├── hungarian_solver.py # TODO: class representing hungarian solver
│   │   ├── model.py            # TODO: class representing an assignment problem 
│   │   └── simplex_solver.py   # TODO: class representing assignment solver using linear programming 
│   └── simplex      # directory containing code related to the simplex algorithm 
│       ├── expressions        # directory with classes related to the linear programming model components 
│       │   ├── atom.py        # atom is just a single variable with a coefficient
│       │   ├── constraint.py  # class representing linear constraint
│       │   ├── expression.py  # class representing linear expression
│       │   └── objective.py   # class representing objective
│       ├── exceptions.py # project specific exceptions
│       ├── model.py      # class allowing to create linear programming models
│       ├── solution.py   # class representing solutions to the problems
│       ├── solver.py     # this class contains main simplex solver loop
│       └── tableau.py    # class representing so called simplex tableau
├── tests # unit tests
└── test.py # script to test assignment solvers on the instances in `assignment_tests`
```
