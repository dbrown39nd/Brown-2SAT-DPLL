#!/usr/bin/env python3 

# Watched this youtube video: https://www.youtube.com/watch?v=ENHKXZg-a4c
from time import time 
from copy import deepcopy
            
def DPLL(expression: list[list], assignment={}, all_vars=None) -> tuple[bool, dict]:
    ''' Go through each clause in the expression '''
    # Initialize the assignment dictionary
    if all_vars is None:
        all_vars = {abs(lit) for clause in expression for lit in clause}
        assignment = {var: None for var in all_vars}
        
    if not expression: # If the expression is empty, we know it is satisfiable.
        for var in all_vars:
            if assignment[var] is None:
                assignment[var] = False
        return True, assignment
    
    if any(len(clause) == 0 for clause in expression): #  Any empty clause makes it unsatisfiable
        return False, {} 
    
    # Need to do unit propagation! ( Clauses with just one literal. They must be true for the statement to be true. )
    new_expression = deepcopy(expression)
    new_assignment = assignment.copy()
    unit_clauses = [clause for clause in new_expression if len(clause) == 1] # get a list of all unit clauses
    while unit_clauses:
        literal = unit_clauses[0][0]
        var = abs(literal)
        new_assignment[var] = literal > 0
        new_expression = simplify(new_expression, literal)
        unit_clauses = [clause for clause in new_expression if len(clause) == 1] # check if any new unit clauses have been created
    
    if not new_expression: # if the expression is empty, we know its satisfiable after propgating unit clauses
        for var in all_vars:
            if new_assignment[var] is None:
                new_assignment[var] = False
        return True, new_assignment

    if any(len(clause) == 0 for clause in new_expression): #  Any empty clause makes it unsatisfiable
        return False, {}
        
    # Choose variables to assign, perform DFS 
    literal = new_expression[0][0]
    var = abs(literal)
    assignment_true_copy = new_assignment.copy()
    assignment_true_copy[var] = True
    sat, final_assignment = DPLL(simplify(new_expression, literal), assignment_true_copy, all_vars) # Go to left child
    if sat:
        return True, final_assignment
    
    assignment_false_copy = new_assignment.copy()
    assignment_false_copy[var] = False
    sat, final_assignment = DPLL(simplify(new_expression, -literal), assignment_false_copy, all_vars) # Go to right child 
    if sat: 
        return True, final_assignment
        
    return False, {}
    
        
def simplify(expression: list[list], literal: int) -> list[list]:
    ''' This function simplifies the expression by removing clauses that contain the positive literal. We do this because we know they are satisfied. 
        This function also removes ~literal from clauses where it appears
    '''
    simplified_expression = []
    for clause in expression:
        if literal in clause:
            continue
        new_clause = [lit for lit in clause if lit != -literal]
        simplified_expression.append(new_clause)
        
    return simplified_expression
            

def prettify_expression(expression: list[list]) -> None:
    clauses = []
    for clause in expression:
        formatted_clause = []
        for literal in clause:
            literal = str(literal)
            if literal.startswith('-'):
                literal = f'~x{literal[1:]}'
            else:
                literal = f'x{literal}'
            formatted_clause.append(literal)
        clause_str = f"({' v '.join(literal for literal in formatted_clause)})"
        clauses.append(clause_str)
    return(' & '.join(clauses))
def complete_assignment(assignment):
    if not assignment:
        return {}
    ''' This function completes the assignment dictionary by adding False to any variable that is not in the dictionary '''
    max_var = max(assignment.keys())
    for i in range(1, max_var + 1):
        if i not in assignment:
            assignment[i] = False
    return assignment

def main(expression: list[list]) -> tuple[bool, dict, float]:
    # Count the number of literals in the expression
    literals = set()
    for clause in expression:
        for literal in clause:
            literals.add(abs(literal))
    
    start_time = time()
    success, assignment = DPLL(expression)
    end_time = time()
    execution_time = end_time - start_time
    completed_assignment = complete_assignment(assignment)
    ordered_assignment = {k: completed_assignment.get(k, False) for k in sorted(completed_assignment)}

    return success, ordered_assignment, execution_time
    
    


    