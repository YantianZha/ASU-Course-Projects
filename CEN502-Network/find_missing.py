def missing_elements(L):
    start, end = L[0], L[-1]
    return sorted(set(xrange(start, end + 1)).difference(L))

print "L = [10,11,13,14,15,16,17,18,20]:"
L = [10,11,13,14,15,16,17,18,20]
L2 = [0, 1, 2, 3]

print "missing:", missing_elements(L)
print "missing:", missing_elements(L2)
# http://stackoverflow.com/questions/16974047/efficient-way-to-find-missing-elements-in-an-integer-sequence

