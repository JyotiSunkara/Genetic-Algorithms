from client_moodle import get_errors, submit
import numpy as np
import random 
from key import SECRET_KEY 
import json
import os

TOP  = 3
FILE_NAME = 'JSON/shradha.json'

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

        # vector = [
        #         -6.625422368668562,
        #         9.836601138162878,
        #         -5.698353847139546,
        #         0.05134871059461612,
        #         0.03783905579211601,
        #         8.111032225245027e-05,
        #         -6.016147135503486e-05,
        #         -1.270826147183366e-07,
        #         3.486275959063019e-08,
        #         4.080179509798645e-11,
        #         -6.7134167191713744e-12
        #     ]
    
        # submit_status = submit(SECRET_KEY, vector)
        # assert "submitted" in submit_status