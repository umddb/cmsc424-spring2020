from relationalalgebrafunctions import *

r = Relation('r', ['A', 'B', 'C'])
r.addTuples([[1, 2, 3], [2, 2, 3], [2, 2, 4]])
s = Relation('s', ['C', 'D'])
s.addTuples([[3, 4], [3, 5], [5, 5]])
DisplayMultipleTables([r, s])


r1 = sigma(r, 'A', '==', 1)
DisplayMultipleTables([r, r1])

r2 = pi(r, ['A', 'B'])
DisplayMultipleTables([r, r2])

r3 = cartesian(r, s)
DisplayMultipleTables([r, s, r3])

ru1 = Relation('ru1', ['A', 'B', 'C']).addTuples([[1, 2, 3], [2, 2, 3]])
ru2 = Relation('ru2', ['A', 'B', 'C']).addTuples([[1, 2, 3], [2, 3, 3]])
ru3 = union(ru1, ru2, "ru1 union ru2")
DisplayMultipleTables([ru1, ru2, ru3])

ru4 = minus(ru1, ru2)
DisplayMultipleTables([ru1, ru2, ru4])

r4 = join(r, s, "r.C", "==", "s.C")
DisplayMultipleTables([r, s, r4])

