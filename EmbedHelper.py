import copy

"""
Instruction holds an intermediate representation of the quantum circuit operations.
This allows for easier manipulation of instruction data and allows this package to be extended
to other quantum circuit representations.

Instruction holds a string of the operation as well as the indices of the target and control qubits.
DOUBLECHECK: First qubit should be control, if list is longer the additional
 qubits are target qubits in order of appearance in instruction
EX: COMPLICATED_GATE(q[1], q[4], c[3], q[71])
 qubtis = (1,3,71)
 bits = (4)
"""


class Instruction(object):

    def __init__(self, instruction):
        operation = instruction.name
        qubits = []
        bits = []
        for i in len(instruction.arg):
            qubits[i] = instruction.arg[i][1];

        #TODO keep track of classical bits also
"""
The Circuit object Holds a list of Segment objects.
The information encoded in all of the segments allows EmbedAlgorithm
to reconstruct the reformatted quantum circuit.

segments initializes to having no elements
GlobalMap initializes to the identity
"""
class Segment(object):
    def __init__(self, start, global_map):
        #local_map = map
        global_map = []
        global_map.add(map)
        startIndex = start
        endIndex = start

    def extend(self):
        Segment.endIndex += 1


"""
The Circuit object Holds a list of Segment objects.
The information encoded in all of the segments allows EmbedAlgorithm
to reconstruct the reformatted quantum circuit.

segments initializes to having no elements
GlobalMap initializes to the identity
"""
class Circuit(object):

    def __init__(self, numQubits):
        currentGlobal = Circuit.getIdentityMap(numQubits);
        segments = []
        numSegments = 0


    #Applies rule mapping to target
    def reMap(self, target, rule):
        if(len(target) != len(rule)):
            print("Error in map dimensions")

        for i in range(0,len(target)):
            target[i] = rule[target[i]]

        return target

    def mapInstruction(self, instruction, map):
        result = copy.deepcopy(instruction)
        for i in len(instruction):
            result[i] = map[result[i]]
        return result

    def getSegment(self, start, end, subsegment=None):

        #Handle differences if extending a subsegment
        if(subsegment == None):
            subsegment = Segment(start,{})
            forwardStart = start
        else:
            if(subsegment.endIndex < end):
                forwardStart = subsegment.endIndex + 1


        if(forwardStart <= end):
            self.extendForward(forwardStart, end, subsegment)

        #Will never be called by Greedy
        if(start < subsegment.startIndex):
            self.extendBackward()

    def extendForward(self, start, end, subsegment):

        for instr in range(start, end):

            if (instr.operation != "CNOT"):
                continue

            startFixed = False
            endFixed = False

            control = instr.qubits[0]
            target = instr.qubits[1]


            for map in subsegment.globals:

                subsegment.globals.remove(map)

                # Set Flags
                if (map.keys().contains(control)):
                    startFixed = True
                if (map.keys().contains(target)):
                    endFixed = True


                #Get Embeddings
                if startFixed == False & endFixed == False:
                    for qubit1 in EmbedHelper.coupling:
                        for qubit2 in EmbedHelper.coupling[qubit1]:
                            if EmbedHelper.isValid(qubit1,qubit2):
                                map[control] = qubit1
                                map[target] = qubit2
                                subsegment.globals.add(map)
                    continue

                if startFixed == False & endFixed == True:
                    qubit1 = map[control]
                    for qubit2 in EmbedHelper.coupling[qubit1]:
                        if EmbedHelper.isValid(qubit1, qubit2):
                            map[target] = qubit2
                            subsegment.globals.add(map)
                    continue

                if startFixed == True & endFixed == False:
                    qubit2 = map[target]
                    for qubit1 in EmbedHelper.coupling:
                        if EmbedHelper.isValid(qubit1, qubit2):
                            map[control] = qubit1
                            subsegment.globals.add(map)
                    continue

                if startFixed == True & endFixed == True:
                    qubit1 = map[control]
                    qubit2 = map[target]
                    if EmbedHelper.isValid(qubit1, qubit2):
                        subsegment.globals.add(map)
                    continue

    def extendBackward(self):
        print()

"""
General tools needed by EmbedAlgorithm
"""
class EmbedHelper(object):

    def __init__(self, QCircuit, coupling):
        print("init")
        self.Instruction = Instruction
        self.Segment = Segment
        self.Circuit = Circuit
        self.coupling = coupling
        self.QCircuit = QCircuit
        self.Instructions = self.reformatInstructions(QCircuit)
        self.segments = []


    def isValid(self, qubit1, qubit2):
        print("HELPER")
        #TODO Fill this in.
        return True

    def reformatInstructions(self, QCircuit):
        result = []
        for i in range(0, len(QCircuit.data)):
            result[i] = Instruction(QCircuit.data[i])
        return result







