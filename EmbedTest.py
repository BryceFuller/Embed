# Checking the version of PYTHON; we only support > 3.5
import sys
import re

if sys.version_info < (3, 5):
    raise Exception('Please use Python version 3.5 or greater.')

# Importing QISKit
from qiskit import QuantumCircuit, QuantumProgram
import Qconfig

# Import basic plotting tools
from qiskit.tools.visualization import plot_histogram

# Quantum program setup
Q_program = QuantumProgram()
Q_program.set_api(Qconfig.APItoken, Qconfig.config["url"])  # set the APIToken and API url

#/////////////////
#Define Local Parameters
#
#Game Plan:
# import QASM DATA,
# format into
#/////////////////

numQubits = 5;
coupling_map = {1: [0], 2: [0, 1, 4], 3: [2, 4]};
inputQASM = ["qreg q[2];", "creg c[2];","h q[0];","cx q[1],q[0];","z q[0];","cx q[0],q[1];","h q[0];","measure q[0] -> c[0];","measure q[1] -> c[1];"];

#/////////////////
#

class localMapping:
    def __init__(self, start):
        startIndex = start;
        finalIndex = 0;
        localMap = {};

def parseQASM():
    print("AAAAAH");

def isLegal(targets):

    if(targets[0] in coupling_map):
        if(coupling_map[targets[0]].__contains__(targets[1])):
            print("true");
            return True;
    else:
        print("false");
        return False;

#isLegal(inputQASM[3]);

for x in inputQASM:
    print(x);
    operation = x.partition(' ')[0];
    targets = (re.findall('\d+', x));
    targets = [int(y) for y in targets];
    if(operation == "cx"):
        print("Is Checking:")
        isLegal(targets);

#/////////////////
# Creating registers
q = Q_program.create_quantum_register("q", 2)
c = Q_program.create_classical_register("c", 2)

# Quantum circuit to make the shared entangled state
superdense = Q_program.create_circuit("superdense", [q], [c])

# For Running this on qx2
superdense.h(q[0])
superdense.cx(q[0], q[1])

# For Running on qx4
# superdense.h(q[1])
# superdense.cx(q[1], q[0])
