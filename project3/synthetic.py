import random

print("create table R(A integer, B integer);")
print("create table S(B integer, C integer);")
print("create table T(C integer, D integer);")

weights_b = [i for i in range(0, 1000)]
weights_c = [i * i  for i in range(0, 50)]


for i in range(0, 100000):
    print("insert into R values({}, {})".format(i, random.choices(range(0, 1000), weights=weights_b)[0]))

for i in range(0, 1000):
    #print("insert into S values({}, {})".format(i, random.choices(range(0, 50), weights=weights_c)[0]))
    print("insert into S values({}, {})".format(i, int(math.sqrt(i) * 50/32)))


for i in range(0, 50):
    print("insert into T values({}, {})".format(i, i))
