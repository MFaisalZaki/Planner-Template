
import os
from z3 import *

from PDDLTaskEncoding import *


def simpleSolver(encoder, upper_bound):

    _solver = Optimize()
    _horizon = 1
    while _horizon < upper_bound:
        print(f'Trying horizon {_horizon}')
        incremental_formula, all_formula = encoder.encode(_horizon)

        # Assert subformulas in solver
        for k,v in incremental_formula.items():
            if k in ['objective', 'goal']:
                continue
            _solver.add(v)

        _solver.push()
        _solver.add(incremental_formula['goal'])
        
        if 'objective' in incremental_formula:
            _objective = _solver.minimize(incremental_formula['objective'])
            
        if _solver.check() == sat:
            _objective = None
            return extractPlanFromModel(_solver, encoder, _horizon, _objective)
        else:
            # Increment horizon until we find a solution
            _horizon = _horizon + 1
            _solver.pop()
    return extractPlanFromModel(None, None, None, None)
            


if __name__ == '__main__':

    domain_file  = os.path.join(os.path.dirname(__file__), 'rover-task', 'domain.pddl')
    problem_file = os.path.join(os.path.dirname(__file__), 'rover-task', 'instance-1.pddl')

    # parallel_linear_encoding = encodeProblem(domain_file, problem_file, 'linear', {'modifier': 'parallel'})
    # linear_linear_encoding   = encodeProblem(domain_file, problem_file, 'linear', {'modifier': 'parallel'})
    r2e_encoding = encodeProblem(domain_file, problem_file, 'r2e', {})

    plan_ = simpleSolver(r2e_encoding, 100)
    if plan_.is_valid():
        print('Solution found')
    else:
        print('No solution found')

    pass