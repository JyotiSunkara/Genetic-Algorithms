from client_moodle import get_errors, submit
import numpy as np
import random 
from key import SECRET_KEY 
import json
import os

# Each TOP submits 6 vectors so comment/ choose TOP accordingly
TOP  = 33
FILE_NAME = 'JSON/shradha.json'
train_factor = 0.8
valid_factor = 0.8

def where_json(fileName):
    return os.path.exists(fileName)

population_fitness = [[],[],[],[]]

if where_json(FILE_NAME):
        with open(FILE_NAME) as json_file:
            data = json.load(json_file)
            population = [dict_item["Vector"] for dict_item in data["Storage"]]
            train = [dict_item["Train Error"] for dict_item in data["Storage"]]
            valid = [dict_item["Validation Error"] for dict_item in data["Storage"]]

            fitness = [(dict_item["Train Error"] + dict_item["Validation Error"]) for dict_item in data["Storage"]]
            valid_fitness = [(dict_item["Train Error"] + dict_item["Validation Error"]*valid_factor) for dict_item in data["Storage"]]
            train_fitness = [(dict_item["Train Error"]*train_factor + dict_item["Validation Error"]) for dict_item in data["Storage"]]
            difference = [abs(dict_item["Train Error"] - dict_item["Validation Error"]) for dict_item in data["Storage"]]

    
            population_fitness = np.column_stack((population, train, valid, fitness, valid_fitness, train_fitness, difference))
            sort_difference = population_fitness[np.argsort(population_fitness[:,-1])]
            sort_trainfit = population_fitness[np.argsort(population_fitness[:,-2])]
            sort_validfit = population_fitness[np.argsort(population_fitness[:,-3])]
            sort_fitness = population_fitness[np.argsort(population_fitness[:,-4])]
            sort_valid = population_fitness[np.argsort(population_fitness[:,-5])]
            sort_train = population_fitness[np.argsort(population_fitness[:,-6])]


            # print(population_fitness[0][:11])
            # print(population_fitness[1])
            # print(population_fitness[2])

        
        for i in range(0, TOP):
            submit_status = submit(SECRET_KEY, sort_difference[i][:11].tolist())
            assert "submitted" in submit_status

            submit_status = submit(SECRET_KEY, sort_trainfit[i][:11].tolist())
            assert "submitted" in submit_status

            submit_status = submit(SECRET_KEY, sort_validfit[i][:11].tolist())
            assert "submitted" in submit_status

            submit_status = submit(SECRET_KEY, sort_valid[i][:11].tolist())
            assert "submitted" in submit_status

            submit_status = submit(SECRET_KEY, sort_train[i][:11].tolist())
            assert "submitted" in submit_status

            submit_status = submit(SECRET_KEY, sort_fitness[i][:11].tolist())
            assert "submitted" in submit_status


        # Worst and middle fitness
        # submit_status = submit(SECRET_KEY, sort_fitness[-1][:11].tolist())
        # assert "submitted" in submit_status

        submit_status = submit(SECRET_KEY, sort_fitness[int(len(sort_fitness)/2)][:11].tolist())
        assert "submitted" in submit_status

        # Worst and middle valid
        # submit_status = submit(SECRET_KEY, sort_valid[-1][:11].tolist())
        # assert "submitted" in submit_status

        submit_status = submit(SECRET_KEY, sort_valid[int(len(sort_fitness)/2)][:11].tolist())
        assert "submitted" in submit_status