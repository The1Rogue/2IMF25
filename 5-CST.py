
from oxidd.bdd import BDDManager


with open("conf-dimacs/toybox.dimacs") as file:
        raw = file.read().split("\n")

n = int(raw[0].split(" ")[2])
m = int(raw[0].split(" ")[3])

ovars = [int(i)-1 for i in raw[1].split(" ")[2:]]


manager = BDDManager(1_000_000_000, 100_000_000, 12)
vars = [manager.var(i) for i in manager.add_vars(n)]
manager.set_var_order(ovars)

print(manager.num_vars())

#vars.reverse()

print("VARS MADE")

a = []
for i in raw[2:-1]:
	v = [int(j) for j in i.split(" ")[:-1]]
	a.append(vars[v[0] - 1] if v[0] > 0 else ~vars[-v[0]-1])
	for j in v[1:]:
		if j > 0:
			a[-1] |= vars[j-1]
		else:
			a[-1] |= vars[-j-1]

print("MADE CLAUSES")

b = a[0]
c = 0
for i in a[1:]:
	b &= i
	c += 1


print("BUILT")


print(b.satisfiable())
print(b.node_count())

manager.export_dddmp("tmp.dddmp", [b])
print("EXPORTED, use 5-CST-URS.py for more data")
