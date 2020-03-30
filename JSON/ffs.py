import json
import requests
import numpy as np

######### DO NOT CHANGE ANYTHING IN THIS FILE ##################
API_ENDPOINT = 'http://10.4.21.147'
PORT = 3000
MAX_DEG = 11

#### functions that you can call
def get_errors(id, vector):
    """
    returns python array of length 2 
    (train error and validation error)
    """
    for i in vector: assert -10<=abs(i)<=10
    assert len(vector) == MAX_DEG

    return json.loads(send_request(id, vector, 'geterrors'))

def submit(id, vector):
    """
    used to make official submission of your weight vector
    returns string "successfully submitted" if properly submitted.
    """
    for i in vector: assert -10<=abs(i)<=10
    assert len(vector) == MAX_DEG
    return send_request(id, vector, 'submit')

#### utility functions
def urljoin(root, port, path=''):
    root = root + ':' + str(port)
    if path: root = '/'.join([root.rstrip('/'), path.rstrip('/')])
    return root

def send_request(id, vector, path):
    api = urljoin(API_ENDPOINT, PORT, path)
    vector = json.dumps(vector)
    response = requests.post(api, data={'id':id, 'vector':vector}).text
    if "reported" in response:
        print(response)
        exit()

    return response


if __name__ == "__main__":
    """
    Replace "test" with your secret ID and just run this file 
    to verify that the server is working for your ID.
    """
    sec_key = 'dnLVLTHPAUOT2R1Ruj1sQvXxWBZZchp8u4WkyZGzaeTQCpyFXC'
    
    vec = [
                0.0,
                0.1294576399995665,
                -6.251834521909177,
                0.0683415947621368,
                0.03800463398050018,
                8.290537316789934e-05,
                -5.9584920882499065e-05,
                -1.2696176209277764e-07,
                3.4902816984505686e-08,
                3.8912045496089703e-11,
                -6.7278487946327235e-12
            ]
   
    # vector = [0e+00,-2e-03,-8e-03,1e-02,-3e-07,3e-12,-1e-09,4e-13,-3e-13,1e-12,-3e-16]
    # vector = [ i * (1+ np.random.uniform(-1,1,1)[0]) for i in vector]
    
    # err = get_errors(sec_key , vec2)
    # print(err, err[0] + err[1])
    # assert len(err) == 2

    submit_status = submit(sec_key, vec)
    assert "submitted" in submit_status
    
