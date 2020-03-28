from client_moodle import get_errors, submit
import numpy as np
import random 
from key import SECRET_KEY 
import json
import os

# Each TOP submits 6 vectors so comment/ choose TOP accordingly
TOP  = 1
FILE_NAME = 'JSON/restart.json'
train_factor = 0.8
valid_factor = 0.8

def where_json(fileName):
    return os.path.exists(fileName)

population_fitness = [[],[],[],[]]

if where_json(FILE_NAME):
        with open(FILE_NAME) as json_file:
            data = json.load(json_file)
            generation = [dict_item["Generation"] for dict_item in data["Storage"]]
            population = [dict_item["Vector"] for dict_item in data["Storage"]]
            train = [dict_item["Train Error"] for dict_item in data["Storage"]]
            valid = [dict_item["Validation Error"] for dict_item in data["Storage"]]

            fitness = [(dict_item["Train Error"] + dict_item["Validation Error"]) for dict_item in data["Storage"]]
            valid_fitness = [(dict_item["Train Error"] + dict_item["Validation Error"]*valid_factor) for dict_item in data["Storage"]]
            train_fitness = [(dict_item["Train Error"]*train_factor + dict_item["Validation Error"]) for dict_item in data["Storage"]]
            difference = [abs(dict_item["Train Error"] - dict_item["Validation Error"]) for dict_item in data["Storage"]]

    
            population_fitness = np.column_stack((generation, population, train, valid, fitness, valid_fitness, train_fitness, difference))
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
            print("Difference: ", sort_difference[i][17], " Generation: ", sort_difference[i][0])
            print(sort_difference[i][1:12].tolist())
            print()

            print("Train Factor: ", sort_trainfit[i][16], " Generation: ", sort_trainfit[i][0])
            print(sort_trainfit[i][1:12].tolist())
            print()

            print("Valid Factor: ", sort_validfit[i][15], " Generation: ", sort_validfit[i][0])
            print(sort_validfit[i][1:12].tolist())
            print()

            print("Fitness: ", sort_fitness[i][14], " Generation: ", sort_fitness[i][0])
            print(sort_fitness[i][1:12].tolist())
            print()

            print("Valid: ", sort_valid[i][13], " Generation: ", sort_valid[i][0])
            print(sort_valid[i][1:12].tolist())
            print()

            print("Train: ", sort_train[i][12], " Generation: ", sort_train[i][0])
            print(sort_train[i][1:12].tolist())
            print()
            