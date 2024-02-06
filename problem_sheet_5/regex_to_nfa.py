
import json
import sys

non_symbols = ['+', '*', '.', '(', ')']
nfa = {}

class charType:
    SYMBOL = 1
    CONCAT = 2
    UNION  = 3
    KLEENE = 4


class NFAState:
    def __init__(self):
        self.next_state = {}


class ExpressionTree:

    def __init__(self, charType, value=None):
        self.charType = charType
        self.value = value
        self.left = None
        self.right = None
    

def make_exp_tree(regexp):
    """
    Constructs an expression tree from a regular expression.

    Args:
        regexp (str): The regular expression.

    Returns:
        ExpressionTree: The root of the expression tree.
    """
    stack = []
    for c in regexp:
        if c == "+":
            z = ExpressionTree(charType.UNION)
            z.right = stack.pop()
            z.left = stack.pop()
            stack.append(z)
        elif c == ".":
            z = ExpressionTree(charType.CONCAT)
            z.right = stack.pop()
            z.left = stack.pop()
            stack.append(z)
        elif c == "*":
            z = ExpressionTree(charType.KLEENE)
            z.left = stack.pop() 
            stack.append(z)
        elif c == "(" or c == ")":
            continue  
        else:
            stack.append(ExpressionTree(charType.SYMBOL, c))
    return stack[0]


def compPrecedence(a, b):
    """
    Compares the precedence of two operators.

    Args:
        a (str): Operator a.
        b (str): Operator b.

    Returns:
        bool: True if a has higher precedence than b, False otherwise.
    """
    p = ["+", ".", "*"]
    return p.index(a) > p.index(b)


def compute_regex(exp_t):
    """
    Computes the E-NFA from the expression tree.

    Args:
        exp_t (ExpressionTree): The root of the expression tree.

    Returns:
        tuple: A tuple containing the start and end states of the E-NFA.
    """
    if exp_t.charType == charType.CONCAT:
        return do_concat(exp_t)
    elif exp_t.charType == charType.UNION:
        return do_union(exp_t)
    elif exp_t.charType == charType.KLEENE:
        return do_kleene_star(exp_t)
    else:
        return eval_symbol(exp_t)


def eval_symbol(exp_t):
    """
    Evaluates a symbol in the expression tree.

    Args:
        exp_t (ExpressionTree): The expression tree node representing the symbol.

    Returns:
        tuple: A tuple containing the start and end states of the NFA.
    """
    start = NFAState()
    end = NFAState()
    
    start.next_state[exp_t.value] = [end]
    return start, end


def do_concat(exp_t):
    """
    Performs concatenation operation on two expression trees.

    Args:
        exp_t (ExpressionTree): The root of the expression tree.

    Returns:
        tuple: A tuple containing the start and end states of the NFA.
    """
    left_nfa  = compute_regex(exp_t.left)
    right_nfa = compute_regex(exp_t.right)

    left_nfa[1].next_state['$'] = [right_nfa[0]]
    return left_nfa[0], right_nfa[1]


def do_union(exp_t):
    """
    Performs union operation on two expression trees.

    Args:
        exp_t (ExpressionTree): The root of the expression tree.

    Returns:
        tuple: A tuple containing the start and end states of the NFA.
    """
    start = NFAState()
    end = NFAState()

    first_nfa = compute_regex(exp_t.left)
    second_nfa = compute_regex(exp_t.right)

    start.next_state['$'] = [first_nfa[0], second_nfa[0]]
    first_nfa[1].next_state['$'] = [end]
    second_nfa[1].next_state['$'] = [end]

    return start, end


def do_kleene_star(exp_t):
    """
    Performs Kleene star operation on an expression tree.

    Args:
        exp_t (ExpressionTree): The root of the expression tree.

    Returns:
        tuple: A tuple containing the start and end states of the NFA.
    """
    start = NFAState()
    end = NFAState()

    starred_nfa = compute_regex(exp_t.left)

    start.next_state['$'] = [starred_nfa[0], end]
    starred_nfa[1].next_state['$'] = [starred_nfa[0], end]

    return start, end


def arrange_transitions(state, states_done, symbol_table):
    """
    Arranges the transitions in the NFA.

    Args:
        state (NFAState): The current state being processed.
        states_done (list): A list of states that have already been processed.
        symbol_table (dict): A dictionary mapping states to their corresponding numbers.
    """
    global nfa

    if state in states_done:
        return

    states_done.append(state)

    for symbol in list(state.next_state):
        if symbol not in nfa['letters']:
            nfa['letters'].append(symbol)
        for ns in state.next_state[symbol]:
            if ns not in symbol_table:
                symbol_table[ns] = sorted(symbol_table.values())[-1] + 1
                q_state = "Q" + str(symbol_table[ns])
                nfa['states'].append(q_state)
            nfa['transition_function'].append(["Q" + str(symbol_table[state]), symbol, "Q" + str(symbol_table[ns])])

        for ns in state.next_state[symbol]:
            arrange_transitions(ns, states_done, symbol_table)


def notation_to_num(str):
    """
    Converts a state notation to its corresponding number.

    Args:
        str (str): The state notation.

    Returns:
        int: The corresponding state number.
    """
    return int(str[1:])


def final_st_dfs():
    """
    Finds the final states in the NFA.
    """
    global nfa
    for st in nfa["states"]:
        count = 0
        for val in nfa['transition_function']:
            if val[0] == st and val[2] != st:
                count += 1
        if count == 0 and st not in nfa["final_states"]:
            nfa["final_states"].append(st)


def arrange_nfa(fa):
    """
    Arranges the NFA.

    Args:
        fa (tuple): A tuple containing the start and end states of the NFA.
    """
    global nfa
    nfa['states'] = []
    nfa['letters'] = []
    nfa['transition_function'] = []
    nfa['start_states'] = []
    nfa['final_states'] = []
    q_1 = "Q" + str(1)
    nfa['states'].append(q_1)
    arrange_transitions(fa[0], [], {fa[0] : 1})
    
    st_num = [notation_to_num(i) for i in nfa['states']]

    nfa["start_states"].append("Q1")
    final_st_dfs()


def add_concat(regex):
    """
    Adds concatenation operators to a regular expression.

    Args:
        regex (str): The regular expression.

    Returns:
        str: The regular expression with concatenation operators added.
    """
    global non_symbols
    l = len(regex)
    res = []
    for i in range(l - 1):
        res.append(regex[i])
        if regex[i] not in non_symbols:
            if regex[i + 1] not in non_symbols or regex[i + 1] == '(':
                res += '.'
        if regex[i] == ')' and regex[i + 1] == '(':
            res += '.'
        if regex[i] == '*' and regex[i + 1] == '(':
            res += '.'
        if regex[i] == '*' and regex[i + 1] not in non_symbols:
            res += '.'
        if regex[i] == ')' and regex[i + 1] not in non_symbols:
            res += '.'

    res += regex[l - 1]
    return res


def compute_postfix(regexp):
    """
    Converts a regular expression to postfix notation.

    Args:
        regexp (str): The regular expression.

    Returns:
        str: The regular expression in postfix notation.
    """
    stk = []
    res = ""

    for c in regexp:
        if c not in non_symbols or c == "*":
            res += c
        elif c == ")":
            while len(stk) > 0 and stk[-1] != "(":
                res += stk.pop()
            stk.pop()
        elif c == "(":
            stk.append(c)
        elif len(stk) == 0 or stk[-1] == "(" or compPrecedence(c, stk[-1]):
            stk.append(c)
        else:
            while len(stk) > 0 and stk[-1] != "(" and not compPrecedence(c, stk[-1]):
                res += stk.pop()
            stk.append(c)

    while len(stk) > 0:
        res += stk.pop()

    return res


def polish_regex(regex):
    """
    Converts a regular expression to Polish notation.

    Args:
        regex (str): The regular expression.

    Returns:
        str: The regular expression in Polish notation.
    """
    reg = add_concat(regex)
    regg = compute_postfix(reg)
    return regg


def load_regex():
    """
    Loads the regular expression from a JSON file.

    Returns:
        dict: The JSON object containing the regular expression.
    """
    with open(sys.argv[1], 'r') as inpjson:
        regex = json.loads(inpjson.read())
    return regex

def output_nfa():
    """
    Outputs the NFA to a JSON file.
    """
    global nfa
    with open(sys.argv[2], 'w') as outjson:
        outjson.write(json.dumps(nfa, indent = 4))

if __name__ == "__main__":
    r = load_regex()
    reg = r['regex']
    
    pr = polish_regex(reg)
    et = make_exp_tree(pr)
    fa = compute_regex(et)
    arrange_nfa(fa)
    output_nfa()
