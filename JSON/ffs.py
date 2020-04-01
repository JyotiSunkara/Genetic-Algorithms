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
    
    vec =[
                0.0,
                0.12392067479379225,
                0.004910276900238874,
                0.04517024906772224,
                -2.7921150307495363e-10,
                4.4453478379407066e-06,
                1.358446347820901e-12,
                -6.886438764090438e-09,
                -1.5406067578304758e-12,
                3.1332846646775037e-12,
                2.5409413278556993e-17
            ]
   
    # [0.0, 0.1240317450077846, -6.211941063144333, 0.04933903144709126, 0.03810848157715883, 8.132366097133624e-05, -6.018769160916912e-05, -1.251585565299179e-07, 3.484096383229681e-08, 4.1614924993407104e-11, -6.732420176902565e-12]
    # vector = [0e+00,-2e-03,-8e-03,1e-02,-3e-07,3e-12,-1e-09,4e-13,-3e-13,1e-12,-3e-16]
    # vector = [ i * (1+ np.random.uniform(-1,1,1)[0]) for i in vector]
    # for i in range(11):
    #     if i == 3:
    #         continue
    #     vec[i] = vec[i]*0.37

    # print(vec)
    err = get_errors(sec_key , vec)
    print(err, err[0] + err[1])
    # assert len(err) == 2

    submit_status = submit(sec_key, vec)
    assert "submitted" in submit_status
    
