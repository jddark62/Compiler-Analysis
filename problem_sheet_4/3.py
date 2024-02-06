# DFA table
#DFA accepts strings that end with 'ab'
dfa = {
    'q0': {'a': 'q1', 'b': 'q0'},
    'q1': {'a': 'q1', 'b': 'q2'},
    'q2': {'a': 'q2', 'b': 'q2'}
}


def check_string_acceptance(string):
    current_state = 'q0'
    for char in string:
        if char not in dfa[current_state]:
            return False
        current_state = dfa[current_state][char]
    return current_state == 'q2'

# Display the DFA table
print("DFA Table:")
for state, transitions in dfa.items():
    print(f"{state}: {transitions}")

# Prompt the user to enter a string
input_string = input("Enter a string: ")

# Check whether the string can be accepted
if check_string_acceptance(input_string):
    print("String is accepted by the DFA")
else:
    print("String is not accepted by the DFA")
