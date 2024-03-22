#Computing First and Follow, given Production Rules

'''
This function accepts the production rules and stores them in a structured way using dictionary.
Keys are non-terminals and values might contain both terminals and non-terminals.
'''

def accept_rules():
    rules = {}
    non_terminals = []
    y = 'y'

    while (y == 'y'):
        string = input("Enter production rule : ")
        for i in range(len(string)):
            if string[i] == '=':
                antecedent = string[0:i]
                non_terminals.append(antecedent)
                get_cons = string[i+1:]
                consequent = get_cons.split('|')
                #Creating key value pair
                rules[antecedent] = consequent
        y = input("Continue?y/n : ")
    return rules, non_terminals

'''
This function is used to find the non-terminals in the production rules.
'''
def update_terminals(rules):
    terminals = []
    operator = ['+', '-', '/', '*', '(', ')']
    for key in rules.keys():
        get_values = rules[key]
        print (get_values)
        for i in get_values:
            try:
                for j in i:
                    if j.islower():
                        terminals.append(j)
            except:
                print ("Exception")
            else:
                for char in i:
                    if char in operator:
                        terminals.append(char)
    return list(set(terminals))

'''
This function computes FIRST of all the non-terminals present in the left side of the production rules.
Do recursive calls to compute FIRST.
'''

def compute_first(state, rules, terminals, non_terminals, fixed, first):
    if state in terminals:
        return state
    elif state in non_terminals:
        get_all_consequents = rules[state]
        for i in range(len(get_all_consequents)):
            get = compute_first(get_all_consequents[i][0], rules, terminals, non_terminals, fixed, first)
            #print "Getting ", get
            if get != None:
                first.append(get)
                #print first
        if state == fixed:
            return first
        else:
            return None

'''
This function computes FOLLOW of all the non-terminals present in the right side of the production rules.
'''
def comp(state, rules, start_state, terminals, non_terminals, first, fol):
    follow = []

    for antecedent in non_terminals:
        consequent = rules[antecedent]
        for val in consequent:
            if state == start_state and state in val:
                follow.append('$')
            if state in val:
                get_index = val.index(state) + 1
                try:
                    if val[get_index] in terminals:
                        follow.append(val[get_index])
                    else:
                        if first[val[get_index]] not in follow:
                            follow.append(first[val[get_index]])
                except:
                    #follow.append(fol[antecedent])
                    print ("Exception thrown")

    return follow



#Control function
def main():

    rules, non_terminals = accept_rules()
    terminals = update_terminals(rules)

    print ("Rules ", rules)
    print ("Terminals ", terminals)
    print ("Non-terminals ", non_terminals)

    #Dictionary for storing non terminals and their FIRTS's
    first = {}
    for i in non_terminals:
        get_first = compute_first(i, rules, terminals, non_terminals, i, [])
        first[i] = get_first

    print ("FIRST : ")
    print (first)

    #Dictionary for storing non terminals and their FOLLOW's
    fol = {}
    start_state = input("Enter start state : ")
    for i in non_terminals:
        get_follow = comp(i, rules, start_state, terminals, non_terminals, first, fol)
        try:
            get_follow = set(get_follow)
            fol[i] = get_follow
        except:
            fol[i] = get_follow
    #fol['K'] = [['$', ')']]
    #fol['L'] = [['+', 'q']]

    print ("FOLLOW : ")
    print (fol)

main()