

from random import randrange

with open("tmp.dddmp") as file:
	raw = file.read().split("\n")

nodes = raw[11:-2]

levelCount = int(raw[5].split(" ")[1])

varCount = int(raw[4].split(" ")[1])

unimportantVars = varCount - levelCount #amount of flags that can be turned on or off no matter what

sats = [0 for i in nodes]
varMap = [int(i)+1 for i in raw[7].split(" ")[1:]]
vars = [0 for i in nodes]
tree = [() for i in nodes]
levels = [levelCount for i in nodes]

for n in range(len(nodes)):
	node = nodes[n].split(" ")
	if node[1] == "F": #false has no solutions
		pass #LEVEL[n] = node[1]

	elif node[1] == "T": #true has one solution
		sats[n] = 1

	else:	#otherwise, sum solution count of both children
		a, b = int(node[2])-1, int(node[3])-1
		l = int(node[1])
		levels[n] = l

		#difference in level implies levels are skipped and can be arbitrarily assigned
		sats[n] = sats[a] * 2 ** (levels[a] - l - 1) + sats[b] * 2 ** (levels[b] - l - 1)

		if sats[n] != int(sats[n]):
			print("FUCK")
			print(n)
			print(sats[n])

		sats[n] = int(sats[n])

		vars[n] = varMap[int(node[1])]
		tree[n] = (a, sats[a], b, sats[b])




s = sats[-1] * 2 ** unimportantVars
print(f"total sats: {s} ({s:.3E})")

def rng(a, b):
	return randrange(a+b) < a


def sample():
	s = [None for i in range(varCount)]
	i = len(nodes) - 1
	while i > 1:
		t = tree[i]
		x = rng(t[1], t[3])
		s[vars[i]-1] = x
		i = t[0] if x else t[2]

	#fill vars that dont matter with 50/50
	for i in range(len(s)):
		if s[i] == None: s[i] = rng(1, 1)

	return s


def ratio(i, k):
	tmp = [sample()[i] for _ in range(k)]
	return sum(tmp)


print(f"x42 selected {ratio(41, 10_000)} / 10_000 times")
