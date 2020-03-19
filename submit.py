from client_moodle import get_errors, submit
import numpy as np
import random 
from key import SECRET_KEY 
from csv import DictWriter

population = [ 7.52619363, -4.08910716, -2.57554439,  4.39919855,  0.75059582, -5.53895851,
 -1.98168411, 1.99506066,  6.66976948, -6.3939873,   9.07245625]
submit_status = submit(SECRET_KEY, population)
assert "submitted" in submit_status
