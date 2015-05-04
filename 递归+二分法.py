__author__ = 'Eric Chan'
def search (deq , i , lower = 0 ,upper = None):
    if upper == None : upper = len(deq)
    n = (upper + lower) / 2
    if i == deq[n]:return n
    else:

        if i < deq[n]:
            return search(deq , i , lower , n)
        else:
            return search(deq , i , n , upper)



import random
b = []
for i in range(100):
    a = random.randint(-10000,10000)
    b.append(a)
b.append(5555)
b.sort()
print b
dd=search(b,5555)
print dd