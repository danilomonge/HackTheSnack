# WE NEED 2D - 1 INEQUALITIES:
# * all variables should be >0: (D inequality constraints)
# * the i-th variable is larger than the i+1-th variable, for all i in [1,D-1] (D-1 inequalities)
#
# AND 3 EQUALITIES:
# * all variables should sum to 1 (the D-simplex, 1 equality)
# * the first variable (gek. Linsen) is 0.63 (1 equality)
# * the 8th variable (Salz) is equal to 0.016 (1 equality)

# inequalities
A = np.zeros((D + D - 1, D))
a = np.zeros(D + D - 1)

# first, the >=0 inequality
A[0:D, 0:D] = -np.eye(D)  # note the minus, for the >= equality
a[0:D] = 0

# then the ordering:
for i in range(D - 1):
    A[D + i, i + 1] = 1
    A[D + i, i] = -1
    a[D + i] = 0

# equalities
B = np.zeros((3, D))
b = np.zeros(3)

# they all sum to 1:
B[0, :] = 1
b[0] = 1

# the first variable (Linsen) is 0.63:
B[1, 0] = 1
b[1] = 0.63

# * the 8th variable (Salz) is equal to 0.016 (1 equality)
B[2, 7] = 1
b[2] = 0.016