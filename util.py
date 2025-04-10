import random

# Returns the max of 0 and the variable
def not_less_zero(variable):
    return max(0, variable)

# Returns a random element from a list
def pick_random_from(l):
    random_variable = random.randint(0, len(l))
    return l[random_variable]