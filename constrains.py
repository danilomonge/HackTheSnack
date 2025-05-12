# Constraint setup for linear system: A·x ≥ a and B·x = b

#   D = number_of_ingredients
#   Inequality Constraints (2D - 1 total):
# * all variables should be >0: (D inequality constraints)
# * the i-th variable is larger than the i+1-th variable, for all i in [1,D-1] (D-1 inequalities)

def build_inequality_contstraints(number_of_ingredients):
   """
    Creates the matrix A and vector a. Then it creates the >=0 inequality constraint and after that is ordering the constraints.

    Args:
        number_of_ingredients = length ingredients

    """
   A = np.zeros((number_of_ingredients + number_of_ingredients - 1, number_of_ingredients))
   a = np.zeros(number_of_ingredients + number_of_ingredients - 1)

   A[0:number_of_ingredients, 0:number_of_ingredients] = -np.eye(number_of_ingredients)
   a[0:number_of_ingredients] = 0
   
   for i in range(number_of_ingredients - 1):
    A[number_of_ingredients + i, i + 1] = 1
    A[number_of_ingredients + i, i] = -1
    a[number_of_ingredients + i] = 0
  

#   Equality Constraints:
# * all variables should sum to 1 (the D-simplex, 1 equality)
# * the first variable (gek. Linsen) is 0.63 (1 equality)
# * the 8th variable (Salz) is equal to 0.016 (1 equality)

  
def build_equality_contraints(fixed_values_dict, number_of_ingredients):
 """
    Creates matrix B and vector b. Then it sets the values in the matrices B and b for the given constraint.

    Args:
        number_of_ingredients = lenghth ingredients
        fixed_values_dict = dictionary that contains all ingredients

 """
num_equality_constraints = len(fixed_values_dict)
B = np.zeros((num_equality_constraints, number_of_ingredients))
b = np.zeros(num_equality_constraints)
B[0, :] = 1
b[0] = 1

 equality_constraints_index = 1
 for ingredient_index, ingredient_amount in fixed_values_dict.items():
    B[equality_constraints_index, ingredient_index] = 1
    b[equality_constraints_index] = ingredient_amount
    equality_constraints_index += 1
    