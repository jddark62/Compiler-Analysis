#Program that does left factoring on production rules

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

#Function for getting the terminals in production rules.
def get_terminals(rules):
    normalised_text = '(terminal)'
    normalised_list = []
    terminals = []
    rules_copy = rules.copy()
    for i in rules.keys():
        get_list = rules[i]
        for element in get_list:
            copy = element
            for index in range(len(element)):

                #Normalizing the non_terminal by replacing it with the string normalized_text.
                #Makes it easier for comparison purposes
                if element[index].islower():
                    copy = element[0:index] + normalised_text + element[(index+1):]
                    normalised_list.append(copy)
                    terminals.append(element[index])
        rules_copy[i] = normalised_list
        normalised_list = []

    #Returns the list of terminals present in the production rules and the dictionary of rules with normalized terminals.
    return terminals, rules_copy


def get_term_nonterm_from_rule(rules, antecedent, terminals, non_terminals):
    get_consequent = rules[antecedent]
    term_store = ''
    non_term_store = ''
    for i in get_consequent:
        for j in i:
            if j in terminals:
                term_store = term_store + j + '|'
            elif j.isupper() and (j not in non_term_store):
                non_term_store = non_term_store + j

    return non_term_store, term_store[:len(term_store)-1] #slicing to remove the last | present in the string.

#Function that does left factoring
def left_factoring(rules, rules_norm, terminals, non_terminals):
    copy_rules = rules.copy()
    for antecedent in rules_norm.keys():
        get_consequent = rules_norm[antecedent]
        flag = True
        if len(get_consequent) > 1 :
            store = get_consequent[0]

            #Loop to check if the consequents are similar. Normalizing the terminals helps in this comparison.
            for element in range(1, len(get_consequent)):
                temp = get_consequent[element]
                if temp != store:
                    flag = False
                    break

            if flag == True:
                non_term, term = get_term_nonterm_from_rule(rules, antecedent, terminals, non_terminals)
                copy_rules[antecedent+'\''] = term.split('|')
                copy_rules[antecedent] = antecedent + '\'' + non_term

    return copy_rules

#Control function
def main():
    rules, non_terminals = accept_rules()
    terminals, rules_norm = get_terminals(rules)
    #print (rules, non_terminals, terminals, rules_norm)
    new_rules = left_factoring(rules, rules_norm, terminals, non_terminals)
    print ("After left factoring : ")
    print (new_rules)

main()