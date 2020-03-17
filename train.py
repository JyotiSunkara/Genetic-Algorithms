from client_moodle import get_errors, submit
import numpy as np


err = get_errors('dnLVLTHPAUOT2R1Ruj1sQvXxWBZZchp8u4WkyZGzaeTQCpyFXC', list(-np.arange(0,1.1,0.1)))
assert len(err) == 2
print(err)

# Population
# Fitness function
# Crossover
# Mutation
# Schema
# Instance


submit_status = submit('dnLVLTHPAUOT2R1Ruj1sQvXxWBZZchp8u4WkyZGzaeTQCpyFXC', list(-np.arange(0,1.1,0.1)))
assert "submitted" in submit_status
    