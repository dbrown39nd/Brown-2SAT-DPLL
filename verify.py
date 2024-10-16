#!/usr/bin/env python3
from dpll import main as dpll, prettify_expression
import random 
from DumbSAT import dumb_sat
import matplotlib.pyplot as plt #type: ignore -> ignore the error that says it can't find the module
import pandas as pd
from tqdm import tqdm
def build_wff(Nvars,Nclauses,LitsPerClause):
    wff=[]
    for i in range(1,Nclauses+1):
        clause=[]
        for j in range(1,LitsPerClause+1):
            var=random.randint(1,Nvars)
            if random.randint(0,1)==0: var=-var
            clause.append(var)
        wff.append(clause)
    return wff


def read_input():
    ''' generator that returns a list of clauses from the input file.'''
    with open('2SAT.cnf.csv', 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('c') or not line: continue

            if line.startswith('p'):
                _, _, n_vars, n_clauses = line.split(',')
                n_vars = int(n_vars)
                n_clauses = int(n_clauses)
                expression = [] 
                for i in range(n_clauses):
                    clause = next(f).split(',')
                    clause = [int(literal.strip()) for literal in clause if literal.strip() != '0' and literal.strip() != '']
                    expression.append(clause)
                yield (expression, n_vars, n_clauses)
                
def write_results_to_file(output_file, expression, count, dpll_success, dpll_assignment, dpll_execution_time, ds_success, ds_assignment, ds_execution_time):
    expression_str = prettify_expression(expression)
    top_row_len = len(expression_str) + 4
    half_len = (top_row_len - len(str(count + 1)) - 2) // 2
    top_line = '+' + '-' * half_len + f'{count + 1}' + '-' * (half_len + (top_row_len % 2)) + '+\n'
    output_file.write(top_line)

    # Get padding! 
    total_width = len(top_line) - 3
    extra_spaces = total_width - len(expression_str)
    left_padding = extra_spaces // 2
    right_padding = extra_spaces - left_padding

    output_file.write('|' + ' ' * left_padding + f'{expression_str}' + ' ' * right_padding + '|\n')
    output_file.write('+' + '-' * (total_width) + '+\n')
                            
    dpll_sat_str = 'DPLL - ' + ('SATISFIABLE' if dpll_success else 'UNSATISFIABLE')
    ds_sat_str = 'DumbSAT - ' + ('SATISFIABLE' if ds_success else 'UNSATISFIABLE')

    dpll_padding = total_width - len(dpll_sat_str)
    ds_padding = total_width - len(ds_sat_str)

    dpll_left_padding = dpll_padding // 2
    dpll_right_padding = dpll_padding - dpll_left_padding

    ds_left_padding = ds_padding // 2
    ds_right_padding = ds_padding - ds_left_padding
    output_file.write('|' + ' ' * dpll_left_padding + f'{dpll_sat_str}' + ' ' * dpll_right_padding + '|\n')
    output_file.write('|' + ' ' * ds_left_padding + f'{ds_sat_str}' + ' ' * ds_right_padding + '|\n')

    # only write the assignments if both algorithms were successful
    if dpll_success and ds_success:
        dpll_assignment_str = f'DPLL Assignment:    {dpll_assignment}'
        ds_assignment_str = f'DumbSAT Assignment: {ds_assignment}'

        max_assignment_width = max(len(dpll_assignment_str), len(ds_assignment_str))
        dpll_padding = total_width - max_assignment_width
        ds_padding = total_width - max_assignment_width

        dpll_left_padding = dpll_padding // 2
        dpll_right_padding = dpll_padding - dpll_left_padding
        ds_left_padding = ds_padding // 2
        ds_right_padding = ds_padding - ds_left_padding

        output_file.write('+' + '-' * (total_width) + '+\n')
        output_file.write('|' + ' ' * dpll_left_padding + dpll_assignment_str + ' ' * dpll_right_padding + '|\n')
        output_file.write('|' + ' ' * ds_left_padding + ds_assignment_str + ' ' * ds_right_padding + '|\n')

        # WRITE THE EXECUTION TIMES
        dpll_time_str = f'DPLL Execution Time: {dpll_execution_time:.2e}'
        ds_time_str = f'DumbSAT Execution Time: {ds_execution_time:.2e}'

        dpll_time_padding = total_width - len(dpll_time_str)
        ds_time_padding = total_width - len(ds_time_str)

        dpll_left_padding = dpll_time_padding // 2
        dpll_right_padding = dpll_time_padding - dpll_left_padding

        ds_left_padding = ds_time_padding // 2
        ds_right_padding = ds_time_padding - ds_left_padding

        output_file.write('+' + '-' * (total_width) + '+\n')
        output_file.write('|' + ' ' * dpll_left_padding + dpll_time_str + ' ' * dpll_right_padding + '|\n')
        output_file.write('|' + ' ' * ds_left_padding + ds_time_str + ' ' * ds_right_padding + '|\n')
    output_file.write('+' + '-' * (total_width) + '+\n')

    
    # 3 buffer lines
    output_file.write('\n')
    output_file.write('\n')
    output_file.write('\n')
            
def convert_assignment_to_list(assignment):
    return [int(val) for val in assignment.values()]

def main():
    literals_counts = []
    dpll_times = []
    dumb_sat_times = []
    count = 0
    count_success = 0 
    count_failures = 0
    sat_count = 0
    unsat_count = 0
    output_lines = []
    
    with open('trace.txt', 'w') as output_file:
        for expression, n_vars, n_clauses in tqdm(read_input(), total=100, desc='Processing WFFs', colour='green'): 
                        
            num_literals = sum(len(clause) for clause in expression)
        
            dpll_success, dpll_assignment, dpll_execution_time = dpll(expression)
            ds_success, ds_assignment, ds_execution_time = dumb_sat(wff=expression, n_vars=n_vars, n_clauses=n_clauses)
            dpll_assignment = convert_assignment_to_list(dpll_assignment)
            ds_assignment = convert_assignment_to_list(ds_assignment)

            write_results_to_file(output_file, expression, count, dpll_success, dpll_assignment, dpll_execution_time, ds_success, ds_assignment, ds_execution_time)
            # Add execution times to the list. 
                
            literals_counts.append(num_literals)
            dpll_times.append(dpll_execution_time)
            dumb_sat_times.append(ds_execution_time)
            
            result_width = 10
            number_str = str(count + 1)
            
            
            if dpll_success == ds_success:
                line = f'WFF {count + 1}' + '.' * (4-len(number_str) + 3) +  f' {"Success":<{result_width}}' + ('SATISFIABLE' if dpll_success else 'UNSATISFIABLE')
                output_lines.append(line)
                tqdm.write(line)
                count_success += 1
                if dpll_success:
                    sat_count += 1
                else:
                    unsat_count += 1
        
            else:
                line = f'WFF {count + 1}' + '.' * (4-len(number_str) + 3) +  f' {"Failure":<{result_width}} <----'
                output_lines.append(line)
                tqdm.write(line)
                count_failures += 1
            
            count += 1        
    
                
            

    output_lines.insert(0, f"{count} WFFs tested. ")
    output_lines.insert(1, f"{sat_count} WFFs SATISFIABLE. ")
    output_lines.insert(2, f"{unsat_count} WFFs UNSATISFIABLE. ")
    output_lines.insert(3, f"{count_success} WFFs with matching results. ")
    output_lines.insert(4, f"{count_failures} WFFs with mismatching results. ")
    if count_failures > 0:
        output_lines.insert(5, "Mismatching results found. ")
    else:
        output_lines.insert(5, "No mismatching results found... SUCCESS! ")    
    output_lines.insert(6, '-'*45)
    
    with open('output.txt', 'w') as output_file:
        for line in output_lines:
            output_file.write(line + '\n')
            
    df = pd.DataFrame({
        'Number of Literals': literals_counts,
        'DPLL Time': dpll_times,
        'DumbSAT Time': dumb_sat_times
    })
    # plot the execution times
    plt.figure(figsize=(10, 6))
    plt.plot(df['Number of Literals'], df['DPLL Time'], label='DPLL Algorithm', marker='o')
    plt.plot(df['Number of Literals'], df['DumbSAT Time'], label='DumbSAT Algorithm', marker='x')
    plt.xlabel('Number of Literals')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Execution Time vs. Number of Literals')
    plt.legend()
    plt.savefig('execution_time_graph.png', format='png') 



        
        
        
        
        
        
        
    
    
if __name__ == "__main__":
    main()
    