#Program that eliminates left recursion from production rules

#Function to accept rules
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

#Function to iterate over production rules and removing left recursion if present.
def left_recursion(rules):
    rules_copy = rules.copy()
    for antecedent in rules_copy.keys():
        get_consequent = rules[antecedent]
        consequent_1 = get_consequent[0]
        consequent_2 = get_consequent[1]
        #Checking if first term in consequent_1 is a non_terminal, i.e, if it is the antecedent
        if consequent_1[0] == antecedent:
            new_var = antecedent + '\''
            new_consequent_1 = consequent_2 + new_var
            new_consequent_2 = consequent_1[1:] + new_var + '|q'
            rules[antecedent] = new_consequent_1
            rules[new_var] = new_consequent_2
        elif consequent_2[0] == antecedent:
            new_var = antecedent + '\''
            new_consequent_1 = consequent_1 + new_var
            new_consequent_2 = consequent_2[1:] + new_var + '|q'
            rules[antecedent] = new_consequent_1
            rules[new_var] = new_consequent_2
    return rules


def main():
    rules, non_terminals = accept_rules()
    print (rules, non_terminals)
    updated_rules = left_recursion(rules)
    print ("Updated rules after eliminating left recursion  : ")
    for key in updated_rules.keys():
        print (key, '=', updated_rules[key])

main()