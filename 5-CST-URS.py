

from random import randrange
from math import log


class BDD:
	def __init__(self, filename):
		print(f"PARSING {filename}")
		with open(f"dddmps/{filename}.dddmp") as file:
			raw = file.read().split("\n")

		self.nodes = raw[11:-2]

		levelCount = int(raw[5].split(" ")[1])

		self.varCount = int(raw[4].split(" ")[1])

		unimportantVars = self.varCount - levelCount #amount of flags that can be turned on or off no matter what


		self.sats = [0 for _ in self.nodes]
		varMap = [int(i)+1 for i in raw[7].split(" ")[1:]]
		self.vars = [0 for _ in self.nodes]
		self.tree = [() for _ in self.nodes]
		self.levels = [levelCount for _ in self.nodes]

		for n in range(len(self.nodes)):
			node = self.nodes[n].split(" ")
			if node[1] == "F": #false has no solutions
				pass

			elif node[1] == "T": #true has one solution
				self.sats[n] = 1

			else:	#otherwise, sum solution count of both children
				a, b = int(node[2])-1, int(node[3])-1
				l = int(node[1])
				self.levels[n] = l

				#difference in level implies levels are skipped and can be arbitrarily assigned
				self.sats[n] = self.sats[a] * 2 ** (self.levels[a] - l - 1) + self.sats[b] * 2 ** (self.levels[b] - l - 1)

				self.sats[n] = int(self.sats[n])

				self.vars[n] = varMap[self.levels[n]]
				self.tree[n] = (a, self.sats[a], b, self.sats[b])




		s = self.sats[-1] * 2 ** unimportantVars
#		print(f"total sats: {s} ({s:.3E})")
		print(f"total sats: {s} (E+{int(log(s,10))})")

		K = 10_000
		r = self.ratio(42, K)
		x = 42

		print(f"x{x} selected {r} / 10_000 random samples (k1/k0 = {r / (K-r):.3F})")


	def sample(self):
		s = [None for i in range(self.varCount)]
		i = len(self.nodes) - 1
		while i > 1:
			t = self.tree[i]
			x = rng(t[1], t[3])
			s[self.vars[i]-1] = x
			i = t[0] if x else t[2]

		#fill vars that dont matter with 50/50
		for i in range(len(s)):
			if s[i] == None: s[i] = rng(1, 1)

		return s

	def ratio(self, i, k):
		return sum([self.sample()[i] for _ in range(k)])



def rng(a, b):
	return randrange(a+b) < a







for i in ["buildroot", "busybox", "embtoolkit", "toybox", "uClinux"]:
        BDD(i)
#for i in ["toybox", "uClinux"]:
 #       BDD(i)
