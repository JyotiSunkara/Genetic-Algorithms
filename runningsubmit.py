from client_moodle import get_errors, submit
import numpy as np
import random 
from key import SECRET_KEY 
import json
import os
TOP  = 13
FILE_NAME = 'JSON/restart.json'
def where_json(fileName):
    return os.path.exists(fileName)

population_fitness = [[],[],[],[]]

if where_json(FILE_NAME):
        with open(FILE_NAME) as json_file:
            data = json.load(json_file)
            population = [dict_item["Vector"] for dict_item in data["Storage"]]
            train = [dict_item["Train Error"] for dict_item in data["Storage"]]
            valid = [dict_item["Validation Error"] for dict_item in data["Storage"]]
            fitness = [dict_item["Fitness"] for dict_item in data["Storage"]]
    
            population_fitness = np.column_stack((population, train, valid, fitness))
            population_fitness = population_fitness[np.argsort(population_fitness[:,-2])]
            # print(population_fitness[0][:11])
            # print(population_fitness[1])
            # print(population_fitness[2])

        
        for i in range(0, TOP):
            submit_status = submit(SECRET_KEY, population_fitness[i][:11].tolist())
            assert "submitted" in submit_status