# Constraint setup for linear system: A·x ≥ a and B·x = b

NUM_EQUALITY_CONSTRAINTS = 3
INDEX_LINSEN = 0
INDEX_SALZ = 7


#   Inequality Constraints (2D - 1 total):
# * all variables should be >0: (D inequality constraints)
# * the i-th variable is larger than the i+1-th variable, for all i in [1,D-1] (D-1 inequalities)

A = np.zeros((D + D - 1, D))
a = np.zeros(D + D - 1)

# creating the >=0 inequality
A[0:D, 0:D] = -np.eye(D)  # note the minus, for the >= equality
a[0:D] = 0

# ordering the constraints
for i in range(D - 1):
    A[D + i, i + 1] = 1
    A[D + i, i] = -1
    a[D + i] = 0


#   Equality Constraints:
# * all variables should sum to 1 (the D-simplex, 1 equality)
# * the first variable (gek. Linsen) is 0.63 (1 equality)
# * the 8th variable (Salz) is equal to 0.016 (1 equality)

B = np.zeros((NUM_EQUALITY_CONSTRAINTS, D))
b = np.zeros(NUM_EQUALITY_CONSTRAINTS)

# sum to 1:
B[0, :] = 1
b[0] = 1

# linsen constraint:
B[1, INDEX_LINSEN] = 1
b[1] = 0.63

# salz constraint:
INDEX_SALZ = 7
B[2, INDEX_SALZ] = 1
b[2] = 0.016