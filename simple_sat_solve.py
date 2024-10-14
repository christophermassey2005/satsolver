from itertools import product


def simple_sat_solve(clause_set):
    listofliterals = set()
    for givenclause in clause_set:
        for literal in givenclause:
            listofliterals.add(abs(literal))

    if not listofliterals:
        return []

    list_of_sorted_literals = sorted(list(listofliterals))

    for cartesian_product in product([True, False], repeat=len(list_of_sorted_literals)):
        satisfied = True
        for givenclause in clause_set:
            givenclauseis_satisfied = False
            for singleliteral in givenclause:
                literal_index = list_of_sorted_literals.index(abs(singleliteral))
                is_this_literal_true = cartesian_product[literal_index]
                if (singleliteral > 0 and is_this_literal_true) or (singleliteral < 0 and not is_this_literal_true):
                    givenclauseis_satisfied = True
                    break
            if not givenclauseis_satisfied:
                satisfied = False
                break
        
        if satisfied:
            sat_assign_list = []
            for i in range(len(cartesian_product)):
                if cartesian_product[i]:
                    sat_assign_list.append(list_of_sorted_literals[i])
                else:
                    sat_assign_list.append(-list_of_sorted_literals[i])
            return sat_assign_list

    return False



example_clause_set = [[1, -2], [-1, 3]]
example_result = simple_sat_solve(example_clause_set)
print(example_result)


print("Testing simple_sat_solve")
try:
    sat1 = [[1],[1,-1],[-1,-2]]
    check = simple_sat_solve(sat1)
    assert check == [1,-2] or check == [-2,1]
    print("Test (SAT) passed")
except:
    print("simple_sat_solve did not work correctly a sat instance")

try:
    unsat1 = [[1, -2], [-1, 2], [-1, -2], [1, 2]]
    check = simple_sat_solve(unsat1)
    assert (not check)
    print("Test (UNSAT) passed")
except:
    print("simple_sat_solve did not work correctly an unsat instance")

def run_tests():
    test_cases = [
        # Test case 1: Satisfiable clause set
        ([[1, -2], [-1, 3], [2, -3]], "Satisfiable", None),
        
        # Test case 2: Unsatisfiable clause set
        ([[1, 2], [-1, -2]], "Unsatisfiable", False),
        
        # Test case 3: Mixed clause set with single and multiple literals
        ([[1], [-2, 3], [2, -3, 4]], "Satisfiable", None),
        
        # Test case 4: Clause set with a single literal
        ([[1]], "Satisfiable", None),
        
        # Test case 5: Empty clause set
        ([], "Trivially Satisfiable", []),
    ]

    all_tests_passed = True

    for i, (clause_set, expected_outcome, expected_result) in enumerate(test_cases, start=1):
        result = simple_sat_solve(clause_set)
        if expected_outcome == "Unsatisfiable":
            if result != expected_result:
                print(f"Test case {i} failed: Expected {expected_result}, but got {result}")
                all_tests_passed = False
        else:  # For satisfiable cases, we check if a solution is provided
            if result == False:
                print(f"Test case {i} failed: Expected a satisfying assignment, but got {result}")
                all_tests_passed = False
            elif expected_result is not None and set(result) != set(expected_result):
                print(f"Test case {i} failed: Expected {expected_result}, but got {result}")
                all_tests_passed = False

    if all_tests_passed:
        print("All tests passed successfully!")
    else:
        print("Some tests failed.")

# Let's run the tests
run_tests()