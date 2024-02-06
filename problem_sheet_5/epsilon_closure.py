
def epsilon_closure(dfa, state):
    closure = set([state])
    stack = [state]

    while stack:
        current_state = stack.pop()

        if current_state in dfa and 'ε' in dfa[current_state]:
            epsilon_transitions = dfa[current_state]['ε']

            for epsilon_state in epsilon_transitions:
                if epsilon_state not in closure:
                    closure.add(epsilon_state)
                    stack.append(epsilon_state)

    return closure

def find_epsilon_closures(dfa):
    epsilon_closures = {}

    for state in dfa:
        closure = epsilon_closure(dfa, state)
        epsilon_closures[state] = closure

    return epsilon_closures

# Example usage 1
dfa1 = {
    'q0': {'a': 'q1', 'ε': ['q2']},
    'q1': {'b': 'q2'},
    'q2': {'a': 'q0', 'ε': ['q1', 'q3']},
    'q3': {'b': 'q2'}
}

epsilon_closures1 = find_epsilon_closures(dfa1)
for state, closure in epsilon_closures1.items():
    print(f'ϵ-closure of state {state}: {closure}')

# Example usage 2
dfa2 = {
    'q0': {'a': 'q1', 'ε': ['q2']},
    'q1': {'b': 'q2'},
    'q2': {'a': 'q0', 'ε': ['q1', 'q3']},
    'q3': {'b': 'q2', 'ε': ['q4']},
    'q4': {'c': 'q5'},
    'q5': {'d': 'q6'},
    'q6': {'e': 'q7'},
    'q7': {'f': 'q8'},
    'q8': {'g': 'q9'},
    'q9': {'h': 'q10'},
    'q10': {'i': 'q11'},
    'q11': {'j': 'q12'},
    'q12': {'k': 'q13'},
    'q13': {'l': 'q14'},
    'q14': {'m': 'q15'},
    'q15': {'n': 'q16'},
    'q16': {'o': 'q17'},
    'q17': {'p': 'q18'},
    'q18': {'q': 'q19'},
    'q19': {'r': 'q20'},
    'q20': {'s': 'q21'},
    'q21': {'t': 'q22'},
    'q22': {'u': 'q23'},
    'q23': {'v': 'q24'},
    'q24': {'w': 'q25'},
    'q25': {'x': 'q26'},
    'q26': {'y': 'q27'},
    'q27': {'z': 'q28'}
}

epsilon_closures2 = find_epsilon_closures(dfa2)
for state, closure in epsilon_closures2.items():
    print(f'ϵ-closure of state {state}: {closure}')
