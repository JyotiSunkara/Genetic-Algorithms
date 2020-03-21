from client_moodle import get_errors, submit
import numpy as np
import random 
from key import SECRET_KEY 
from csv import DictWriter


first_parent = [0.0, 0.1240317450077846, -6.211941063144333, 0.04933903144709126, 0.03810848157715883, 8.132366097133624e-05, -6.018769160916912e-05, -1.251585565299179e-07, 3.484096383229681e-08, 4.1614924993407104e-11, -6.732420176902565e-12]
error = get_errors(SECRET_KEY, first_parent)
fitness = error[0]*0.7 + error[1]
population_errors = np.empty((10, 2))

population_errors[0] = error
print(error, population_errors[0])
print(fitness)
