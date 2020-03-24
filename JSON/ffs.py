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
    vec = [
    -7.0181426278850925,
    9.840838325772234,
    -5.898353847139546,
    0.0494005418683377,
    0.037836708577746896,
    8.111032225245027e-05,
    -6.016147135503486e-05,
    -1.2706995546461015e-07,
    3.486275959063019e-08,
    3.822179974214149e-11,
    -6.7142900295387635e-12
]

    err = get_errors('dnLVLTHPAUOT2R1Ruj1sQvXxWBZZchp8u4WkyZGzaeTQCpyFXC', vec)
    print(err)
    assert len(err) == 2

    # submit_status = submit('dnLVLTHPAUOT2R1Ruj1sQvXxWBZZchp8u4WkyZGzaeTQCpyFXC', list(-np.arange(0,1.1,0.1)))
    # assert "submitted" in submit_status
    
