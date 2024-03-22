"""
This script converts a given NFA (Non-Deterministic Finite Automaton) to a DFA (Deterministic Finite Automaton).
It defines functions to compute the epsilon closure, compute the next state, and convert the NFA to DFA.
"""

# Define the NFA transitions
nfa_transitions = {
    'q0': {'a': {'q1'}, 'ε': {'q2'}},
    'q1': {'b': {'q2'}, 'ε': {'q3'}},
    'q2': {'a': {'q1'}, 'b': {'q2'}},
    'q3': {'a': {'q3'}, 'b': {'q3'}}
}

# Define the DFA transitions
dfa_transitions = {}

# Define the initial state of the DFA
dfa_initial_state = frozenset(['q0'])

# Define the set of final states of the DFA
dfa_final_states = set()

# Define a stack to keep track of unprocessed DFA states
unprocessed_states = [dfa_initial_state]

# Process unprocessed DFA states until the stack is empty
while unprocessed_states:
    current_state = unprocessed_states.pop()
    
    # Compute the ε-closure of the current DFA state
    epsilon_closure = set(current_state)
    stack = list(epsilon_closure)
    while stack:
        state = stack.pop()
        if state in nfa_transitions and 'ε' in nfa_transitions[state]:
            for epsilon_transition in nfa_transitions[state]['ε']:
                if epsilon_transition not in epsilon_closure:
                    epsilon_closure.add(epsilon_transition)
                    stack.append(epsilon_transition)
    
    # Add the current DFA state to the DFA transitions
    dfa_transitions[current_state] = {}
    
    # Process each input symbol
    for symbol in ['a', 'b']:
        next_state = set()
        
        # Compute the set of NFA states reachable from the current DFA state on the input symbol
        for state in epsilon_closure:
            if state in nfa_transitions and symbol in nfa_transitions[state]:
                next_state.update(nfa_transitions[state][symbol])
        
        # Compute the ε-closure of the set of NFA states
        stack = list(next_state)
        while stack:
            state = stack.pop()
            if state in nfa_transitions and 'ε' in nfa_transitions[state]:
                for epsilon_transition in nfa_transitions[state]['ε']:
                    if epsilon_transition not in next_state:
                        next_state.add(epsilon_transition)
                        stack.append(epsilon_transition)
        
        # Add the transition to the DFA transitions
        dfa_transitions[current_state][symbol] = frozenset(next_state)
        
        # Add the next DFA state to the unprocessed states if it hasn't been processed yet
        if frozenset(next_state) not in dfa_transitions:
            unprocessed_states.append(frozenset(next_state))
    
    # Check if the current DFA state contains any final NFA states
    if any(state in dfa_final_states for state in current_state):
        dfa_final_states.add(current_state)

# Print the DFA transitions, initial state, and final states
print("DFA Transitions:")
for state, transitions in dfa_transitions.items():
    print(f"{state}: {transitions}")
print("DFA Initial State:", dfa_initial_state)
print("DFA Final States:", dfa_final_states)


def convert_nfa_to_dfa(nfa_transitions, nfa_initial_state, nfa_final_states):
    """
    Converts a given NFA to a DFA.

    Parameters:
    - nfa_transitions (dict): The transitions of the NFA.
    - nfa_initial_state (str): The initial state of the NFA.
    - nfa_final_states (set): The set of final states of the NFA.

    Returns:
    - dfa_transitions (dict): The transitions of the DFA.
    - dfa_initial_state (frozenset): The initial state of the DFA.
    - dfa_final_states (set): The set of final states of the DFA.
    """
    dfa_transitions = {}
    dfa_initial_state = frozenset([nfa_initial_state])
    dfa_final_states = set()
    unprocessed_states = [dfa_initial_state]

    while unprocessed_states:
        current_state = unprocessed_states.pop()

        epsilon_closure = compute_epsilon_closure(current_state, nfa_transitions)

        dfa_transitions[current_state] = {}

        for symbol in ['a', 'b']:
            next_state = compute_next_state(epsilon_closure, symbol, nfa_transitions)

            if next_state:
                dfa_transitions[current_state][symbol] = frozenset(next_state)

                if frozenset(next_state) not in dfa_transitions:
                    unprocessed_states.append(frozenset(next_state))

                if any(state in nfa_final_states for state in next_state):
                    dfa_final_states.add(current_state)

    return dfa_transitions, dfa_initial_state, dfa_final_states


def compute_epsilon_closure(states, transitions):
    """
    Computes the epsilon closure of a given set of states in an NFA.

    Parameters:
    - states (set): The set of states.
    - transitions (dict): The transitions of the NFA.

    Returns:
    - epsilon_closure (set): The epsilon closure of the given set of states.
    """
    epsilon_closure = set(states)
    stack = list(epsilon_closure)

    while stack:
        state = stack.pop()

        if state in transitions and 'ε' in transitions[state]:
            for epsilon_transition in transitions[state]['ε']:
                if epsilon_transition not in epsilon_closure:
                    epsilon_closure.add(epsilon_transition)
                    stack.append(epsilon_transition)

    return epsilon_closure


def compute_next_state(states, symbol, transitions):
    """
    Computes the next state given a set of states, an input symbol, and the transitions of an NFA.

    Parameters:
    - states (set): The set of states.
    - symbol (str): The input symbol.
    - transitions (dict): The transitions of the NFA.

    Returns:
    - next_state (set): The set of next states.
    """
    next_state = set()

    for state in states:
        if state in transitions and symbol in transitions[state]:
            next_state.update(transitions[state][symbol])

    epsilon_closure = compute_epsilon_closure(next_state, transitions)

    return epsilon_closure


# Example 1
nfa_transitions_1 = {
    'q0': {'a': {'q1'}, 'ε': {'q2'}},
    'q1': {'b': {'q2'}, 'ε': {'q3'}},
    'q2': {'a': {'q1'}, 'b': {'q2'}},
    'q3': {'a': {'q3'}, 'b': {'q3'}}
}
nfa_initial_state_1 = 'q0'
nfa_final_states_1 = {'q3'}

dfa_transitions_1, dfa_initial_state_1, dfa_final_states_1 = convert_nfa_to_dfa(nfa_transitions_1, nfa_initial_state_1, nfa_final_states_1)

print("Example 1 - DFA Transitions:")
for state, transitions in dfa_transitions_1.items():
    print(f"{state}: {transitions}")
print("Example 1 - DFA Initial State:", dfa_initial_state_1)
print("Example 1 - DFA Final States:", dfa_final_states_1)

# Example 2
nfa_transitions_2 = {
    'q0': {'a': {'q1', 'q2'}, 'ε': {'q3'}},
    'q1': {'b': {'q2'}, 'ε': {'q4'}},
    'q2': {'a': {'q1'}, 'b': {'q2'}},
    'q3': {'a': {'q3'}, 'b': {'q3'}},
    'q4': {'a': {'q4'}, 'b': {'q4'}}
}
nfa_initial_state_2 = 'q0'
nfa_final_states_2 = {'q3', 'q4'}

dfa_transitions_2, dfa_initial_state_2, dfa_final_states_2 = convert_nfa_to_dfa(nfa_transitions_2, nfa_initial_state_2, nfa_final_states_2)

print("Example 2 - DFA Transitions:")
for state, transitions in dfa_transitions_2.items():
    print(f"{state}: {transitions}")
print("Example 2 - DFA Initial State:", dfa_initial_state_2)
print("Example 2 - DFA Final States:", dfa_final_states_2)

