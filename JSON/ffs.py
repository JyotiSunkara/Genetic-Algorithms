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
    # key = 'I22KGMKf3ZqtxxvxklykgAlk1dQZvVqhgfZT1i8NWjOgBC4ntl'
    vec = [
                -6.47437705313709,
                9.915031282546686,
                -6.095379162998791,
                0.06116363487362357,
                0.037917049989923374,
                8.507648718298185e-05,
                -6.018147135503486e-05,
                -1.2761030001770375e-07,
                3.486378130484902e-08,
                3.911421279922079e-11,
                -6.706312927923882e-12
            ]

    # vector = [0e+00,-2e-03,-8e-03,1e-02,-3e-07,3e-12,-1e-09,4e-13,-3e-13,1e-12,-3e-16]
    # vector = [ i * (1+ np.random.uniform(-1,1,1)[0]) for i in vector]
    err = get_errors('dnLVLTHPAUOT2R1Ruj1sQvXxWBZZchp8u4WkyZGzaeTQCpyFXC', vec)
    print(err, err[0] + err[1])
    assert len(err) == 2

    # submit_status = submit('dnLVLTHPAUOT2R1Ruj1sQvXxWBZZchp8u4WkyZGzaeTQCpyFXC', list(-np.arange(0,1.1,0.1)))
    # assert "submitted" in submit_status
    
