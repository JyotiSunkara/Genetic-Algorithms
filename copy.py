import json
import os

READ_FILE = 'JSON/new.json'
WRITE_FILE = 'JSON/remain.json'


def where_json(fileName):
    return os.path.exists(fileName)

if where_json(READ_FILE):
    with open(READ_FILE) as readObj:
        getData = json.load(readObj)
        temporary  = []
        length = len(getData["Storage"])
        for i in range (2400, length):
            rowDict = { 
                            "Generation": getData["Storage"][i]["Generation"], 
                            "Vector": getData["Storage"][i]["Vector"], 
                            "Train Error": getData["Storage"][i]["Train Error"], 
                            "Validation Error": getData["Storage"][i]["Validation Error"],
                            "Fitness": getData["Storage"][i]["Fitness"]
            }
            temporary.append(rowDict)

    putData = {"Storage": temporary}
    with open(WRITE_FILE, 'w') as writeObj:
        json.dump(putData, writeObj, indent=4)
