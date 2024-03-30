import stopit
import saport.assignment.model as sam
import saport.assignment.hungarian_solver as sahs
import saport.assignment.simplex_solver as sass
from saport.simplex.exceptions import EmptyModelError
import numpy as np

TEST_DIR = "assignment_tests"

MIN = ["min_03_12", "min_03_15", "min_04_20", "min_05_124"]
RECT_MIN = ["min_03_04_12", "min_04_03_11", "min_04_03_14"]
MAX = ["max_04_41", "max_04_44"]
RECT_MAX = ["max_04_03_22"]

def check_normalization(path: str, expected_value: int, description: str):
    model = sam.AssignmentProblem.from_file(path)
    normalized_model = sam.NormalizedAssignmentProblem.from_problem(model)
    assert normalized_model.costs is not None, f"the normalized problem has empty cost matrix :("
    assert normalized_model.costs.shape[0] == normalized_model.costs.shape[1], f"the normalized problem cost array should be square!"
    assert np.all(normalized_model.costs >= 0), f"the normalized problem cost array should not contain negative values!"

def check_simplex(path: str, expected_value: int, description: str):
    model = sam.AssignmentProblem.from_file(path)
    simplex_solver = sass.Solver(model)
    try:
        simplex_solution = simplex_solver.solve()
        assert simplex_solution.objective == expected_value, f"simplex solver found incorrect solution cost for {description} at {path}: found {hungarian_solution.objective}, expected {expected}"
        simplex_recalculated_cost = sum([model.costs[w,t] for w,t in enumerate(simplex_solution.assigned_tasks) if t >= 0])
        assert simplex_recalculated_cost == expected_value, f"simplex solver found incorrect assignment for {description} at {path}"
    except EmptyModelError:
        raise AssertionError(f"simplex model is empty for {description} at {path}") from None

def check_hungarian(path: str, expected_value: int, description: str):
    model = sam.AssignmentProblem.from_file(path)     
    hungarian_solver = sahs.Solver(model)
    with stopit.ThreadingTimeout(10):
        try:
            hungarian_solution = hungarian_solver.solve()
            assert hungarian_solution.objective == expected_value, f"hungarian solver found incorrect solution cost for {description} at {path}: found {hungarian_solution.objective}, expected {expected}"
            hungarian_recalculated_cost = sum([model.costs[w,t] for w,t in enumerate(hungarian_solution.assigned_tasks) if t >= 0])
            assert hungarian_recalculated_cost == expected_value, f"hungarian solver found incorrect assignment for {description} at {path}"
        except stopit.TimeoutException:
            raise AssertionError(f"hungarian solver never (in 10 seconds) ends its computations for {description} at {path}") from None
        

if __name__ == "__main__":

    for i, (check, check_name) in enumerate([
                              (check_normalization, "normalization"), 
                              (check_simplex, "simplex solver"), 
                              (check_hungarian, "hungarian solver")]):
    # TESTING STANDARD SQUARE MIN ASSIGNMENTS
        print(f"{i}) checking the {check_name}...")
        for fname in MIN:
            expected = (int)(fname.split("_")[-1])
            check(f"{TEST_DIR}/{fname}.txt", expected, "standard square minimization problem")

        # TESTING RECTANGULAR MIN ASSIGNMENTS (NUMBER OF TASKS != NMBER OF WORKERS)
        for fname in RECT_MIN:
            expected = (int)(fname.split("_")[-1])
            check(f"{TEST_DIR}/{fname}.txt", expected, "rectangular minimization problem")

        # TESTING MAX ASSIGNMENTS
        for fname in MAX:
            expected = (int)(fname.split("_")[-1])
            check(f"{TEST_DIR}/{fname}.txt", expected, "square maximization problem")

        # TESTING RECTANGULAR MAX ASSIGNMENTS
        for fname in RECT_MAX:
            expected = (int)(fname.split("_")[-1])
            check(f"{TEST_DIR}/{fname}.txt", expected, "rectangular maximization problem")

        print(f"...congrats! Your {check_name} seems to work!")
    print("===============")
    print("Success! Your code operate correctly!")
    
    