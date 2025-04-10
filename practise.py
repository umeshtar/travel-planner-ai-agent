import itertools
from random import choice

print({'5'} or {'1'})
print({} or {'1'})

a, b = [5, 7]
print(a, b)

print(len({'a': 1, 'b': 2}))

for i in range(10):
    print(choice([11, 23, 32]))

a = [1,2,4]
b = a.copy()
b.remove(2)
print(a)
print(b)

interest_cycle = itertools.cycle(['a', 'b', 'c', 'd'])
tag = next(interest_cycle)
print(tag)
tag = next(interest_cycle)
print(tag)
tag = next(interest_cycle)
print(tag)
