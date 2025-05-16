import constraints
from Input.validation import validate
#from Input.check_input_existence import ...
from Input.constraints_preparation import prepare_constraints_dict
import os
import sys
sys.path.append(os.path.dirname(computation.__file__))
import computation

def main():
    test_dict = {'ingredient1': 0.2, 'ingredient2': 0.3, 'ingredient3': 0.5}
    number_of_ingredients = len(test_dict)

    if validate(test_dict) == True:
        print("Valid input") #for testing purposes
        # next check if the product already exists in the database

        # if not prepare constraints:
        fixed_value_dict= prepare_constraints_dict(test_dict)

        # build the constraints
        A,a=constraints.build_inequality_constraints(number_of_ingredients)
        B,b=constraints.build_equality_constraints(fixed_value_dict, number_of_ingredients)

        # start the computation
        computation.MCMC(A, a, B, b, num_iter=int(1e6), thinning=int(1e4))

        # results now need to be sent to output


    else:
        print("Invalid input")
        # return error message to user