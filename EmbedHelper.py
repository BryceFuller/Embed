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
        self.operation = instruction.name


        self.qubits = []
        self.bits = []
        for i in range(0,len(instruction.arg)):
            self.qubits.append(instruction.arg[i][1])
        return
        #TODO keep track of classical bits also
"""
The Circuit object Holds a list of Segment objects.
The information encoded in all of the segments allows EmbedAlgorithm
to reconstruct the reformatted quantum circuit.

segments initializes to having no elements
GlobalMap initializes to the identity
"""
class Segment(object):
    def __init__(self, start, end, global_map):
        self.global_map = []
        self.global_map.append(global_map)
        self.startIndex = start
        self.endIndex = end




"""
General tools needed by EmbedAlgorithm
"""
class EmbedHelper(object):

    def __init__(self, QCircuit, coupling):
        print("init")
        self.Instruction = Instruction
        self.Segment = Segment
        self.Coupling = coupling
        self.QCircuit = QCircuit
        self.Instructions = self.reformatInstructions(QCircuit)
        self.Segments = []


    def isValid(self, qubit1, qubit2):
        print("HELPER")
        #TODO Fill this in.
        return True

    def reformatInstructions(self, QCircuit):
        result = []
        for i in range(0, len(QCircuit.data)):
            instr = Instruction(QCircuit.data[i])
            result.append(instr)
        return result

    # Applies rule mapping to target
    def reMap(self, target, rule):
        if (len(target) != len(rule)):
            print("Error in map dimensions")

        for i in range(0, len(target)):
            target[i] = rule[target[i]]

        return target

    def mapInstruction(self, instruction, map):
        result = copy.deepcopy(instruction)
        for i in len(instruction):
            result[i] = map[result[i]]
        return result

    def getSegment(self, start, end, subsegment=None):

        newSegment = Segment(start, end, {})
        forwardStart = start

        if subsegment != None:
            if subsegment.endIndex < end:
                forwardStart = subsegment.endIndex + 1

        if(forwardStart <= end):
            self.extendForward(forwardStart, end, newSegment)

        #Will never be called by Greedy
        if subsegment != None:
            if (start < subsegment.startIndex):
                self.extendBackward()


        return newSegment

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
                        if map.contains(qubit1):
                            continue
                        for qubit2 in EmbedHelper.coupling[qubit1]:
                            if map.contains(qubit2):
                                continue
                            if EmbedHelper.isValid(qubit1,qubit2):
                                map[control] = qubit1
                                map[target] = qubit2
                                subsegment.globals.add(map)
                    continue

                if startFixed == False & endFixed == True:
                    qubit1 = map[control]
                    for qubit2 in EmbedHelper.coupling[qubit1]:
                        if map.contains(qubit2):
                            continue
                        if EmbedHelper.isValid(qubit1, qubit2):
                            map[target] = qubit2
                            subsegment.globals.add(map)
                    continue

                if startFixed == True & endFixed == False:
                    qubit2 = map[target]
                    for qubit1 in EmbedHelper.coupling:
                        if map.contains(qubit1):
                            continue
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








