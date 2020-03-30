from client_moodle import get_errors, submit
import numpy as np
import random 
from key import SECRET_KEY 
import json
import os

TOP  = 3
FILE_NAME = 'JSON/remain.json'

def where_json(fileName):
    return os.path.exists(fileName)

if where_json(FILE_NAME):
        with open(FILE_NAME) as json_file:
            data = json.load(json_file)
            index = 0
            length = len(data["Storage"])
            while True:
                if (index < length):
                    generation = data["Storage"][index]["Generation"] 
                else:
                    break

                for i in range(0, TOP):

                    submit_status = submit(SECRET_KEY, data["Storage"][index + i]["Vector"])
                    assert "submitted" in submit_status
                    # print(data["Storage"][index + i]["Vector"])
                
                while (index < length and data["Storage"][index]["Generation"]  == generation):
                    index = index + 1
