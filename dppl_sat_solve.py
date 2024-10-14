from itertools import product


#Previously used

def load_dimacs(filename):
    setofclauses = []
    f = open(filename, 'r')
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


def dpll_sat_solve(clause_set, partial_assignment):
    litset = set()
    ch = True
    newlist = []

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
            newlist.append(unit)
            potentialanswers = []
            for singleitem in clause_set:
                if unit not in singleitem:
                    potentialanswers.append(singleitem)
            clause_set = []
            for singleitem in potentialanswers:
                new_clause = []
                for literal in singleitem:
                    if literal != -unit:
                        new_clause.append(literal)
                clause_set.append(new_clause)
            ch = True

    simpler = True
    for singleitem in clause_set:
        if len(singleitem) == 0:
            simpler = False
            break
    
    partial_assignment.extend(newlist)
    
    if not simpler:
        return False
    
    if not clause_set:
        return partial_assignment
    
    variabletobranchon = None
    for clause in clause_set:
        for literal in clause:
            if abs(literal) not in map(abs, partial_assignment):
                variabletobranchon = literal
                break
        if variabletobranchon:
            break
    
    if variabletobranchon is None:
        return partial_assignment
    
    for guess in [variabletobranchon, -variabletobranchon]:
        finalpotentialanswers = []
        for clause in clause_set:
            if guess not in clause:
                finalpotentialanswers.append(clause)
        potentialanswers = []
        for clause in finalpotentialanswers:
            new_clause = []
            for literal in clause:
                if -guess != literal:
                    new_clause.append(literal)
            potentialanswers.append(new_clause)
        finalpotentialanswers = potentialanswers
        
        result = dpll_sat_solve(finalpotentialanswers, partial_assignment + [guess])
        if result:
            return result
    
    return False


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


print("Testing other instances")

try:
    clause_set2 = load_dimacs("PHP-5-4.txt")
    check2 = dpll_sat_solve(clause_set2,[])
    assert (not check2)
    print("Test PHP-5-4.txt (UNSAT) passed")
except:
    print("Failed problem PHP-5-4.txt")



try:
    clause_set3 = load_dimacs("LNP-6.txt")
    check3 = dpll_sat_solve(clause_set3,[])
    assert (not check3)
    print("Test LNP-6.txt (UNSAT) passed")
except:
    print("Failed problem LNP-6.txt")

try:
    clause_set4 = load_dimacs("8queens.txt")
    check4 = dpll_sat_solve(clause_set4,[])
    #assert (not check2)
    print(check4)
    #print("Test PHP-5-4.txt (UNSAT) passed")
except:
    print("Failed problem PHP-5-4.txt")

try:
    clause_set5 = load_dimacs("W.txt")
    check5 = dpll_sat_solve(clause_set5,[])
    #assert (not check2)
    #print("Test PHP-5-4.txt (UNSAT) passed")
    print(check5)
except:
    print("Failed problem PHP-5-4.txt")

print("Finished tests")

