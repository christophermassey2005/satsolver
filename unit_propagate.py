

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

print("Testing unit_propagate")
try:
    clause_set = [[1],[-1,2]]
    check = unit_propagate(clause_set)
    assert check == []
    print("Test passed")
except:
    print("unit_propagate did not work correctly")