from itertools import product

def load_dimacs(file_name):
    #file_name will be of the form "problem_name.txt"
    setofclauses = []
    f = open(file_name, 'r')
    lines_of_file = f.readlines()
    for line in lines_of_file:
        if line[0] != 'c' and line[0] != 'p':
            individual_clause = []
            count = ''
            for char in line:
                if char.isdigit() or char == '-':
                    count += char
                elif count:
                    if count != '0':
                        individual_clause.append(int(count))
                    count = ''
            if count and count != '0':
                individual_clause.append(int(count))
            setofclauses.append(individual_clause)
    f.close()
    return setofclauses

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


def branching_sat_solve(clause_set,partial_assignment):
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


def unit_propagate(clause_set):
    litset = set()
    ch = True

    while ch:
        ch = False
        clause_set_ofunits = set()
        for singleitem in clause_set:
            if len(singleitem) == 1 and singleitem[0] not in litset:
                clause_set_ofunits.add(singleitem[0])
        
        if not clause_set_ofunits:
            break

        for unit in clause_set_ofunits:
            litset.add(unit)
            new_clause_set = []
            for singleitem in clause_set:
                if unit not in singleitem:
                    new_clause_set.append(singleitem)
            clause_set = new_clause_set

            for i in range(len(clause_set)):
                if -unit in clause_set[i]:
                    new_clause = []
                    for literal in clause_set[i]:
                        if literal != -unit:
                            new_clause.append(literal)
                    clause_set[i] = new_clause
                    ch = True

    list_of_clauses_final = []
    for singleitem in clause_set:
        if singleitem:
            contains_determined_literal = False
            for literal in singleitem:
                if literal in litset:
                    contains_determined_literal = True
                    break
            if not contains_determined_literal:
                list_of_clauses_final.append(singleitem)
    
    return list_of_clauses_final


def dpll_sat_solve(clause_set,partial_assignment):
    ...



def test():
    print("Testing load_dimacs")
    try:
        dimacs = load_dimacs("sat.txt")
        assert dimacs == [[1],[1,-1],[-1,-2]]
        print("Test passed")
    except:
        print("Failed to correctly load DIMACS file")

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

    print("Testing branching_sat_solve")
    try:
        sat1 = [[1],[1,-1],[-1,-2]]
        check = branching_sat_solve(sat1,[])
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


    print("Testing unit_propagate")
    try:
        clause_set = [[1],[-1,2]]
        check = unit_propagate(clause_set)
        assert check == []
        print("Test passed")
    except:
        print("unit_propagate did not work correctly")


    print("Testing DPLL") #Note, this requires load_dimacs to work correctly
    problem_names = ["sat.txt","unsat.txt"]
    for problem in problem_names:
        try:
            clause_set = load_dimacs(problem)
            check = dpll_sat_solve(clause_set,[])
            if problem == problem_names[1]:
                assert (not check)
                print("Test (UNSAT) passed")
            else:
                assert check == [1,-2] or check == [-2,1]
                print("Test (SAT) passed")
        except:
            print("Failed problem " + str(problem))
    print("Finished tests")

test()