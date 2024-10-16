#                    Brute Force SAT
# This file generates a set of random wffs and tests each for satisfiability.
#   The test returns "Satisfiable" or not, and the time it took to determine that.
# A wff is expressed as a list of lists where each internal list is a clause.
#    and each integer within a clause list is a literal
#    A positive integer such as "3" means that clause is true if variable 3 is true
#    A negative integer such as "-3" means that clause is true if variable 3 is false
#  A clause is satisfiable if at least one literal is true
#  A wff is satisfiable if all clauses are satisfiable
# An assignment to n variables is a list of n 0s or 1s (0=>False, 1=>True)
#    where assignment[i] is value for variable i+1 (there is no variable 0)
#
# build_wff builds a random wff with specified # of clauses, variables,
#   and literals/clause
# check takes a wff, generates all possible assignments,
#   and determines if any assignment satisfies it.
#   If so it stops and returns the time ans assignment
# test_wff builds a random wff with certain structure
#
# run_cases takes a list of 4-tuples and for each one generates a number of wffs
#    with the same specified characteristices, and test each one.
#    It outputs to a file (in current directory) each wff in cnf format,
#    and also for each case it dumps a row to a .csv file that contains
#       the test conditions and the satisfying assignment if it exists
from time import time 
def dumb_sat(wff,n_vars,n_clauses):
# Run thru all possibilities for assignments to wff
# Starting at a given assignment (typically array of n_vars+1 0's)
# At each iteration the assignment is "incremented" to next possible
# At the 2^n_vars+1'st iteration, stop - tried all assignments
    start_time = time()
    assignment=list((0 for x in range(n_vars+2)))
    satisfiable=False
    while (assignment[n_vars+1]==0):
        # Iterate thru clauses, quit if not satisfiable
        for i in range(0,n_clauses): #Check i'th clause
            clause=wff[i]
            satisfiable=False
            for j in range(0,len(clause)): # check each literal
                literal=clause[j]
                if literal>0:  lit=1
                else: lit=0
                var_value=assignment[abs(literal)] # look up literal's value
                if lit==var_value:
                    satisfiable=True
                    break
            if satisfiable==False: break
        if satisfiable==True: break # exit if found a satisfying assignment
        # Last try did not satisfy; generate next assignment)
        for i in range(1,n_vars+2):
            if assignment[i]==0:
                assignment[i]=1
                break
            else: assignment[i]=0
            
    return satisfiable, prettify_assignment(assignment[1:-1]), time()-start_time

def prettify_assignment(assignment):
    p_assignment = {}
    for i, val in enumerate(assignment):
        p_assignment[f'x{i+1}'] = val > 0 
                
    return p_assignment
            
                

            
