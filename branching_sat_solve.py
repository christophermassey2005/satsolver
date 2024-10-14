

def branching_sat_solve(clause_set, partial_assignment):
    if partial_assignment is None:
        partial_assignment = []

    for givenclause in clause_set:
        if givenclause == []:
            return False

    satisfied = True
    for givenclause in clause_set:
        clause_satisfied = False
        for singleliteral in givenclause:
            if singleliteral in partial_assignment:
                clause_satisfied = True
                break
        if not clause_satisfied:
            satisfied = False
            break
    if satisfied:
        return partial_assignment

    set_ = set()
    for givenclause in clause_set:
        for singleliteral in givenclause:
            if singleliteral not in partial_assignment and -singleliteral not in partial_assignment:
                set_.add(abs(singleliteral))
    if not set_:
        return partial_assignment
    popped_var = set_.pop()

    partialassignment2 = []
    for givenclause in clause_set:
        if -popped_var not in givenclause:
            new_clause = []
            for singleliteral in givenclause:
                if singleliteral != popped_var:
                    new_clause.append(singleliteral)
            partialassignment2.append(new_clause)

    result = branching_sat_solve(partialassignment2, partial_assignment + [-popped_var])
    if result is not False:
        return result

    new_clause_set_true = []
    for givenclause in clause_set:
        if popped_var not in givenclause:
            new_clause = []
            for singleliteral in givenclause:
                if singleliteral != -popped_var:
                    new_clause.append(singleliteral)
            new_clause_set_true.append(new_clause)

    return branching_sat_solve(new_clause_set_true, partial_assignment + [popped_var])


print("Testing branching_sat_solve")
try:
    sat1 = [[1],[1,-1],[-1,-2]]
    check = branching_sat_solve(sat1,[])
    print(check)
    assert check == [1,-2] or check == [-2,1]
    print("Test (SAT) passed")
except:
    print("branching_sat_solve did not work correctly a sat instance")

try:
    unsat1 = [[1, -2], [-1, 2], [-1, -2], [1, 2]]
    check = branching_sat_solve(unsat1,[])
    assert (not check)
    print("Test (UNSAT) passed")
except:
    print("branching_sat_solve did not work correctly an unsat instance")

