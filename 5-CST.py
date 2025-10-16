
from oxidd.bdd import BDDManager



class BDD:
	def __init__(self, filename):
		print(f"PARSING {filename}")
		with open(f"conf-dimacs/{filename}.dimacs") as file:
		        raw = file.read().split("\n")

		self.varCount = int(raw[0].split(" ")[2])
		self.clauseCount = int(raw[0].split(" ")[3])

		self.varOrder = [int(i)-1 for i in raw[1].split(" ")[2:]]
		self.manager = BDDManager(1_000_000_000, 100_000_000, 12)
		self.vars = [self.manager.var(i) for i in self.manager.add_vars(self.varCount)]
		self.manager.set_var_order(self.varOrder)

		print(f"{self.varCount} Variables | {self.clauseCount} Clauses")

		a = []
		clauses = [[int(j) for j in i.split(" ")[:-1]] for i in raw[2:-1]]

		for v in clauses:
			a.append(self.vars[v[0] - 1] if v[0] > 0 else ~self.vars[-v[0]-1])
			for j in v[1:]:
				if j > 0:
					a[-1] |= self.vars[j-1]
				else:
					a[-1] |= ~self.vars[-j-1]

		print("Clauses parsed")


		self.bdd = a[0]
		for i in a[1:]:
			self.bdd &= i

		print("Built full BDD")
		if self.bdd.satisfiable():
			print("Satisfiability verified")
		else:
			print("BDD IS NOT SATISFIABLE!!!!")
		print(f"{self.bdd.node_count()} Nodes")

#
#		self.pairs = set()
#
#		for i in range(self.varCount):
#			for j in range(i):
#				if (self.bdd & self.vars[i] & self.vars[j]).satisfiable():
#					self.pairs.add((i, True, j, True))
#				if (self.bdd & self.vars[i] & ~self.vars[j]).satisfiable():
#					self.pairs.add((i, True, j, False))
#				if (self.bdd & ~self.vars[i] & self.vars[j]).satisfiable():
#					self.pairs.add((i, False, j, True))
#				if (self.bdd & ~self.vars[i] & ~self.vars[j]).satisfiable():
#					self.pairs.add((i, False, j, False))
#			if i % 100 == 0:
#				self.manager.gc()
#
#		print(f"Found {len(self.pairs)} Interaction pairs")
#
#
#		self.cover = []
#
#		#greedy cover algorithm
#		for p in self.pairs:
#			covered = False
#			fits = None
#			for c in self.cover:
#				if c[p[0]] == p[1] and c[p[2]] == p[3]: #already covered
#					covered = True
#					break
#				elif (c[p[0]] == p[1] or c[p[0]] == None) and (c[p[2]] == p[3] or c[p[3]] == None): #could be covered here
#					fits = c
#
#			if not covered:
#				if fits == None:
#					fits = [None for _ in range(self.varCount)]
#					self.cover.append(fits)
#
#				fits[p[0]] = p[1]
#				fits[p[2]] = p[3]
#
#		print(f"Created cover of size {len(self.cover)}")


		self.manager.export_dddmp(f"dddmps/{filename}.dddmp", [self.bdd])
		print("Exported dddmp file, use 5-CST-URS.py for more data")



for i in ["buildroot", "busybox", "embtoolkit", "toybox", "uClinux"]:
	BDD(i)
