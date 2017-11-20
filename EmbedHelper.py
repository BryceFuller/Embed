import copy

"""
Instruction holds an intermediate representation of the quantum circuit operations.
This allows for easier manipulation of instruction data and allows this package to be extended
to other quantum circuit representations.

Instruction holds a string of the operation as well as the indices of the target and control qubits.
"""
class Instruction(object):

    def __init__(self, instruction):
        operation = instruction.name
        qubits = []
        for i in len(instruction.arg):
            qubits[i] = instruction.arg[i][1];
"""
The Circuit object Holds a list of Segment objects.
The information encoded in all of the segments allows EmbedAlgorithm
to reconstruct the reformatted quantum circuit.

segments initializes to having no elements
GlobalMap initializes to the identity
"""
class Segment(object):
    def __init__(self, start, local_map, global_map):
        local_map = map
        global_map = map
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

    def addSegment(self, index, local_map):

        self.currentGlobal = Circuit.reMap(self.currentGlobal, local_map)
        self.segments.add(Segment(index, local_map, self.currentGlobal))
        self.numSegments += 1

    def getIdentityMap(self, numQubits):
        map = {}
        # Return empty map for 0 qubits
        if (numQubits == 0): return map

        for i in range(0, numQubits):
            map[i] = i;
        return map

    #TODO Figure out neccesary arguments and design optimal algorithm for this.
    def getValidMap(self, instruction, coupling):

        for keys in coupling:
            #TODO find a valid mapping
        

        print("Do Magic")


    #Permutes the map target according to the mapping rule
    def reMap(self, target, rule):
        if(len(target) != len(rule)):
            print("Error in map dimensions")

        for i in range(0,len(target)):
            target[i] = rule[target[i]]

        return target

    def mapInstruction(self, instruction, map):
        result = copy.deepcopy(instruction)
        for i in len(instruction):
            result[1] = map[result[1]]
        return result

"""
General tools needed by EmbedAlgorithm
"""

class EmbedHelper(object):

    def __init__(self):
        print("init")


    def isValid(self):
        print("HELPER")
        #TODO Fill this in.
        return True

    def reformatInstructions(self, QCircuit):
        result = []
        for i in range(0,len(QCircuit.data)):
            result[i] = Instruction(QCircuit.data[i])
        return result







