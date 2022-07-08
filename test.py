from pyrsistent import l


from copy import deepcopy

ls = [[1, 2], [3, 4]]
x = deepcopy(ls)
x[1][0] = 5
print(x)
print(ls)
