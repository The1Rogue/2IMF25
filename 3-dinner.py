


from z3 import *

s = Solver()

#matrix[time][house][person] = [person] is at [house] during course [time]
#[person] and [person] + 5 are a couple, living at the house with the same index
matrix = [[[Bool(f"H{house}_P{person}_T{time}")
	for person in range(10)]
	 	for house in range(5)]
			for time in range(5)]


#every house hosts twice (we know a house hosts if the owner is home)
for i in range(5):
	s.add(PbEq([(matrix[time][i][i], 1) for time in range(5)], 2))

#couples host together
for house in range(5):
	for time in range(5):
		s.add(matrix[time][house][house] == matrix[time][house][house+5])

#every person can only be at one place at a time
for person in range(10):
	for time in range(5):
		s.add(PbEq([(matrix[time][house][person], 1) for house in range(5)], 1))

#every person can only be in a house where there is a course
for person in range(10):
	for time in range(5):
		for house in range(5):
			s.add(Implies(matrix[time][house][person], matrix[time][house][house]))

#theres exactly 5 or 0 people in a house at any time
for house in range(5):
	for time in range(5):
		s.add(Or(
			PbEq([(matrix[time][house][person],1) for person in range(10)], 5),
			PbEq([(matrix[time][house][person],1) for person in range(10)], 0),
		))




#property 1:
#every pair meets at least once
for person1 in range(10):
	for person2 in range(person1):
		s.add(Or([And(matrix[time][house][person1], matrix[time][house][person2])
			for time in range(5)
				for house in range(5)
		]))


#property 2:
for person1 in range(10):
	for person2 in range(person1):
		s.add(PbLe(
			[(And(matrix[time][house][person1], matrix[time][house][person2]),1)
				for time in range(5)
					for house in range(5)
		], 3))

#property 3:
#couples dont meet outside their own home, ie, if one of the couples is in another home, that implies the other is not
for person in range(5):
	for time in range(5):
		for house in range(5):
			if house != person:
				s.add(Implies(matrix[time][house][person], Not(matrix[time][house][person+5])))

#property 4:
#all guests at a house are unique, ie, every person visits any house thats not their own at most once
for person in range(5):
	for house in range(5):
		if house != person:
			s.add(PbLe([(matrix[time][house][person], 1) for time in range(5)], 1))
			s.add(PbLe([(matrix[time][house][person+5], 1) for time in range(5)], 1))






if s.check() != sat:
	print("UNSATISFIABLE")
	exit()

m = s.model()
for time in range(5):
	print(f"\nTIME {time}")
	for house in range(5):
		if m[matrix[time][house][house]]:
			print(f"\tHOUSE {house}:")
			for person in range(10):
				if m[matrix[time][house][person]]:
					print(f"\t\tPERSON {person}")





