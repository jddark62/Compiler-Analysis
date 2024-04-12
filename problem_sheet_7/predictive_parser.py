gram = {
	"E":["ET'","T"],  # Grammar rule for E
	"T":["T*F","F"],  # Grammar rule for T
	"F":["(E)","i"],  # Grammar rule for F
	# "S":["CC"],  # Grammar rule for S
	# "C":["eC","d"],  # Grammar rule for C
}

def removeDirectLR(gramA, A):
	"""Remove direct left recursion from the grammar"""
	temp = gramA[A]
	tempCr = []
	tempInCr = []
	for i in temp:
		if i[0] == A:
			# Direct left recursion found, replace with A' production
			tempInCr.append(i[1:]+[A+"'"])
		else:
			# No left recursion, keep the production as it is
			tempCr.append(i+[A+"'"])
	tempInCr.append(["e"])  # Add epsilon production for A'
	gramA[A] = tempCr  # Update grammar with new productions
	gramA[A+"'"] = tempInCr  # Add A' productions to the grammar
	return gramA

def checkForIndirect(gramA, a, ai):
	"""Check if there is indirect left recursion from a to ai
	ai is the non-terminal symbol to check for indirect left recursion"""
	if ai not in gramA:
		return False 
	if a == ai:
		return True
	for i in gramA[ai]:
		if i[0] == ai:
			return False
		if i[0] in gramA:
			return checkForIndirect(gramA, a, i[0])
	return False

def rep(gramA, A):
	"""Replace indirect left recursion in the grammar"""
	temp = gramA[A]
	newTemp = []
	for i in temp:
		if checkForIndirect(gramA, A, i[0]):
			# Indirect left recursion found, replace with new productions
			for k in gramA[i[0]]:
				t=[]
				t+=k
				t+=i[1:]
				newTemp.append(t)
		else:
			# No indirect left recursion, keep the production as it is
			newTemp.append(i)
	gramA[A] = newTemp  # Update grammar with new productions
	return gramA

def rem(gram):
	"""Remove left recursion from the grammar"""
	c = 1
	conv = {}
	gramA = {}
	revconv = {}
	for j in gram:
		conv[j] = "A"+str(c)  # Create new non-terminal symbols
		gramA["A"+str(c)] = []  # Initialize new grammar productions
		c+=1
	for i in gram:
		for j in gram[i]:
			temp = []	
			for k in j:
				if k in conv:
					temp.append(conv[k])  # Replace terminals with new non-terminals
				else:
					temp.append(k)
			gramA[conv[i]].append(temp)  # Update grammar with new productions
	for i in range(c-1,0,-1):
		ai = "A"+str(i)
		for j in range(0,i):
			aj = gramA[ai][0][0]
			if ai!=aj :
				if aj in gramA and checkForIndirect(gramA,ai,aj):
					gramA = rep(gramA, ai)  # Replace indirect left recursion
	for i in range(1,c):
		ai = "A"+str(i)
		for j in gramA[ai]:
			if ai==j[0]:
				gramA = removeDirectLR(gramA, ai)  # Remove direct left recursion
				break
	op = {}
	for i in gramA:
		a = str(i)
		for j in conv:
			a = a.replace(conv[j],j)  # Convert new non-terminals back to original symbols
		revconv[i] = a
	for i in gramA:
		l = []
		for j in gramA[i]:
			k = []
			for m in j:
				if m in revconv:
					k.append(m.replace(m,revconv[m]))  # Convert new non-terminals back to original symbols
				else:
					k.append(m)
			l.append(k)
		op[revconv[i]] = l
	return op

result = rem(gram)

terminals = []
for i in result:
	for j in result[i]:
		for k in j:
			if k not in result:
				terminals+=[k]  # Collect terminals from the grammar
terminals = list(set(terminals))  # Remove duplicates
#print(terminals)

def first(gram, term):
	"""Compute the FIRST set for a given non-terminal symbol"""
	a = []
	if term not in gram:
		return [term]  # If term is a terminal, return itself
	for i in gram[term]:
		if i[0] not in gram:
			a.append(i[0])  # If the first symbol is a terminal, add it to the FIRST set
		elif i[0] in gram:
			a += first(gram, i[0])  # If the first symbol is a non-terminal, compute its FIRST set recursively
	return a

firsts = {}
for i in result:
	firsts[i] = first(result,i)
	# print(f'First({i}):',firsts[i])

def follow(gram, term):
	"""Compute the FOLLOW set for a given non-terminal symbol"""
	a = []
	for rule in gram:
		for i in gram[rule]:
			if term in i:
				temp = i
				indx = i.index(term)
				if indx+1!=len(i):
					if i[-1] in firsts:
						a+=firsts[i[-1]]  # If the next symbol is a non-terminal, add its FIRST set to the FOLLOW set
					else:
						a+=[i[-1]]  # If the next symbol is a terminal, add it to the FOLLOW set
				else:
					a+=["e"]  # If the term is at the end of the production, add epsilon to the FOLLOW set
				if rule != term and "e" in a:
					a+= follow(gram,rule)  # If there is epsilon in the FOLLOW set, compute the FOLLOW set of the rule
	return a

follows = {}
for i in result:
	follows[i] = list(set(follow(result,i)))
	if "e" in follows[i]:
		follows[i].pop(follows[i].index("e"))
	follows[i]+=["$"]
	# print(f'Follow({i}):',follows[i])

# Modify the result to store the productions as strings
resMod = {}
for i in result:
	l = []
	for j in result[i]:
		temp = ""
		for k in j:
			temp+=k
		l.append(temp)
	resMod[i] = l

# Create predictive parsing table
tterm = list(terminals)
tterm.pop(tterm.index("e"))
tterm+=["d"]
pptable = {}
for i in result:
	for j in tterm:
		if j in firsts[i]:
			pptable[(i,j)]=resMod[i[0]][0]  # Fill the table with the corresponding production
		else:
			pptable[(i,j)]=""
	if "e" in firsts[i]:
		for j in tterm:
			if j in follows[i]:
				pptable[(i,j)]="e"  # Fill the table with epsilon
pptable[("F","i")] = "i"  # Fill the table with specific production
toprint = f'{"": <10}'
for i in tterm:
	toprint+= f'|{i: <10}'
print(toprint)
for i in result:
	toprint = f'{i: <10}'
	for j in tterm:
		if pptable[(i,j)]!="":
			toprint+=f'|{i+"->"+pptable[(i,j)]: <10}'
		else:
			toprint+=f'|{pptable[(i,j)]: <10}'
	print(f'{"-":-<76}')
	print(toprint)

