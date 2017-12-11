# Checself=Noneversion of PYTHON; we only support > 3.5
import sys
import re

from EMBED.Embed import Embed

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
#Global Map initializes to identity map
GlobalMap = {i: i for i in range(0, numQubits)};


#The circuit will be 'cut' into individually embeddable
#segments. This structure holds the information relating
#each individual segment to it's previous segment.
#This includes the start and end indices, as well as the
#local qubit mapping from the previous segment to the current one.
class embeddableSegment:
    #finalIndex;
    def __init__(self, start, qubit_map):
        self.startIndex = start;
        self.finalIndex = 0;
        self.localMap = qubit_map;

#Returns an identity map of size numQubits.
def identityMap():
    identity = {}

    for i in numQubits:
        identity[i] = i;
    return identity;


#This function takes as input a mapping, and an invalid
#operation, and returns a local mapping which will render the
#operation valid.
def findLocalMapping(instruction):
    targets = (re.findall('\d+', x));
    targets = [int(y) for y in targets];
    localMap = identityMap();
    if(targets[0] in coupling_map):
        controlee = coupling_map[targets[0]][0]; #Room Here to implement smarter choice of swap qubit.
        localMap[controlee] = targets[1];
        localMap[targets[1]] = controlee;
    else:
        print();
        #see if there's a controller that can control target[1]
        #if there isn't, pick a new pair to map to.


#Takes in a QASM command and
#outputs true if this command is valid within
#the topology defined by
def isLegal(instruction):
    #print();
    #print(instruction);
    operation = instruction.partition(' ')[0];
    targets = (re.findall('\d+', x));
    targets = [int(y) for y in targets];
    #print("INPUT:" + operation + "–" + str(targets));
    #Run targets through global mapping
    if (operation == "cx"):

        if(targets[0] in coupling_map):
            if(coupling_map[targets[0]].__contains__(targets[1])):
                print("CX: valid");
                return True;
        else:
            print("CX: invalid");
            return False;

    else:
        return True;

#//////////////////////////////

CircuitMappings = {};
num_segments = 1;
QASMindex = 0;
currentMap = GlobalMap;
#initialize map to Identity


CircuitMappings[num_segments-1] = embeddableSegment(QASMindex, currentMap);
print("running");

'''for x in inputQASM:
    if(isLegal(x)):
        print("numsegments = " + str(num_segments));
        currentSegment = CircuitMappings[num_segments-1];
        currentSegment.finalIndex += 1;
    else: #Handle segment break
        print("ELSE!!!");
        #Get local map between previous and current segment
        #Upadte global map
        currentMap = currentMap.copy();
        #CircuitMappings = CircuitMappings + {num_segments: embeddableSegment};
        #print(CircuitMappings.values());
        print(" " + str(QASMindex) + " " + str(num_segments));
        CircuitMappings[num_segments-1] = embeddableSegment(QASMindex, coupling_map);
        num_segments += 1;

    QASMindex += 1;
'''


class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))

testCoupling = {0: (3,), 1: (0,3), 2: (1,), 3: (4,5), 4: (2,6), 5:(6,)}
q = Q_program.create_quantum_register("qubits", 11)
c = Q_program.create_classical_register("bits", 11)
embedtester = Q_program.create_circuit("QCircuit", [q], [c])

embedtester.cx(q[0], q[1])
embedtester.cx(q[1], q[2])
embedtester.cx(q[1], q[3])
embedtester.cx(q[3], q[4])
embedtester.cx(q[3], q[5])

embedtester.cx(q[4], q[6])
embedtester.cx(q[4], q[7])
embedtester.cx(q[6], q[9])
embedtester.cx(q[6], q[10])
embedtester.cx(q[7], q[8])


Embed(embedtester, testCoupling)

#/////////////////
'''
q = Q_program.create_quantum_register("q", 4)
c = Q_program.create_classical_register("c", 4)
superdense = Q_program.create_circuit("superdense", [q], [c])
# For Running this on qx2
superdense.h(q[3])
superdense.h(q[0])
superdense.cx(q[0], q[1])
superdense.z(q[0])
superdense.cx(q[0], q[1])
superdense.h(q[0])
superdense.measure(q[0], c[0])
superdense.measure(q[1], c[1])
circuits = ["superdense"]
var = superdense.regs['q'].size
print(Q_program.get_qasms(circuits)[0])

dict1 = {}
dict2 = {}
dict1[1] = (2, 1)
dict2[3] = 1

dict1[3] = 1
dict2[1] = (2, 1)

print(hash(hashabledict(dict1)))
print(hash(hashabledict(dict2)))
'''
