import os

def load_dimacs(filename):
    clause_set = []  # Initialize the list to hold the clause sets
    with open(filename, 'r') as file:
        for line in file:
            # Ignore comments and the problem line
            if line.startswith('c') or line.startswith('p'):
                continue
            # Convert the line into a list of integers, excluding the trailing 0
            clause = [int(x) for x in line.split() if x != '0']
            clause_set.append(clause)
    return clause_set

print(os.getcwd())
dimacs = load_dimacs("sat.txt")
assert dimacs == [[1],[1,-1],[-1,-2]]
print("Test passed")
