
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

#Offical test
dimacs = load_dimacs("sat.txt")
assert dimacs == [[1],[1,-1],[-1,-2]]
print("Test passed")

