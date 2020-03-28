from client_moodle import get_errors, submit
import numpy as np
import random 
from key import SECRET_KEY 
import json
import os


parent1 = [2.123, 2.123, 2.123, 3.123, 4.123, 5.123, 6.123, 7.123, 8.123, 9.123, 10.09]
parent2 = [9.123, 8.123, 7.123, 3.123, 4.123, 5.123, 6.123, 7.123, 8.123, 9.123, 10.97]


child1 = np.empty(11)
child2 = np.empty(11)

u = random.random() 
    
# Distribution index that determines how far children go from parents
# Should ideally be updated every generation
# Some crazy complex updation that I did not understand
# If n_c is greater children are closer to parents
# Mostly n is between 2 to 5
# n_c can be kept constant as well
n_c = 5
    
if (u < 0.5):
    beta = (2 * u)**((n_c + 1)**-1)
else:
    beta = ((2*(1-u))**-1)**((n_c + 1)**-1)

parent1 = np.array(parent1)
parent2 = np.array(parent2)
child1 = 0.5*((1 + beta) * parent1 + (1 - beta) * parent2)
child2 = 0.5*((1 - beta) * parent1 + (1 + beta) * parent2)

# print(child1)
# print(child2)
# print((parent1 + parent2)/2)
# print((child1 + child2)/2)

