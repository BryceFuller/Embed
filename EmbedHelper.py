import copy

import collections

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
        self.global_maps = []
        self.global_maps.append(global_map)
        self.startIndex = start
        self.endIndex = end


"""
General tools needed by EmbedAlgorithm
"""
class EmbedHelper(object):

    def __init__(self, QCircuit, coupling):
        print("init")
       # self.Instruction = Instruction
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


        forwardStart = start

        if subsegment != None:
            newSegment = copy.deepcopy(subsegment)
            if subsegment.endIndex < end:
                forwardStart = subsegment.endIndex + 1
        else:
            newSegment = Segment(start, end, {})

        if(forwardStart <= end):
            self.extendForward(forwardStart, end, newSegment)

        #Will never be called by Greedy
        if subsegment != None:
            if (start < subsegment.startIndex):
                self.extendBackward()


        return newSegment

    def extendForward(self, start, end, subsegment):


        for instr in range(start, end+1):

            Instruction = self.Instructions[instr];

            if (Instruction.operation != "cx"):
                continue

            #These two flags specify whether or not the target or control
            # qubit are constrained to a particular value for each mapping.
            startFixed = False
            endFixed = False


            control = Instruction.qubits[0]
            target = Instruction.qubits[1]
            newMaps = []

            for map in subsegment.global_maps:


                # Set Flags
                if (control in map.keys()):
                    startFixed = True
                if (target in map.keys()):
                    endFixed = True

                #Get Embeddings
                if (startFixed == False) & (endFixed == False):
                    for qubit1 in self.Coupling:
                        if qubit1 in map:
                            continue
                        if (qubit1 not in self.Coupling):
                            continue;
                        for qubit2 in self.Coupling[qubit1]:
                            if qubit2 in map.values():
                                continue
                            if self.isValid(qubit1, qubit2):
                                newMap = copy.deepcopy(map)
                                newMap[control] = qubit1
                                newMap[target] = qubit2
                                newMaps.append(newMap)
                                subsegment.endIndex = instr;
                    continue

                if (startFixed == False) & (endFixed == True):
                    qubit2 = map[target]

                    for qubit1 in self.Coupling:
                        if qubit1 in map.values():
                            continue
                        if self.isValid(qubit1, qubit2):
                            newMap = copy.deepcopy(map)
                            newMap[control] = qubit1
                            newMaps.append(newMap)
                            subsegment.endIndex = instr;
                    continue


                if (startFixed == True) & (endFixed == False):
                    qubit1 = map[control]
                    if(qubit1 not in self.Coupling):
                        continue;
                    for qubit2 in self.Coupling[qubit1]:
                        if qubit2 in map.values():
                            continue
                        if self.isValid(qubit1, qubit2):
                            newMap = copy.deepcopy(map)
                            newMap[target] = qubit2
                            newMaps.append(newMap)
                            subsegment.endIndex = instr;
                    continue

                if (startFixed == True) & (endFixed == True):
                    qubit1 = map[control]
                    qubit2 = map[target]
                    if self.isValid(qubit1, qubit2):
                        newMaps.append(map)
                        subsegment.endIndex = instr;
                    continue
            if(len(newMaps) != 0):
                subsegment.global_maps = newMaps;

    def extendBackward(self):
        print()



    def cost(self, mapA, mapB):

        cost = 0

        # get the keys, sort them as a list and make them into a queue
        Akeys = collections.deque(sorted(list(mapA.keys())))
        Bkeys = collections.deque(sorted(list(mapB.keys())))

        Avalues = set(mapA.values())
        Bvalues = set(mapB.values())

        #TODO: Currently, Accessible only stores the qubits that control onto another qubit,
        #TODO: but I need it to hold all qubits available in the topology. I will need to write a method for this.

        Accessible = set(self.Coupling.keys())
        UnusedA = Accessible - Avalues
        UnusedB = Accessible - Bvalues

        #Aval and Bval will hold elements as they are popped off of Akeys and Bkeys
        Aval = None
        Bval = None

        revisit = set()

        while (len(Akeys) > 0) | (len(Bkeys) > 0):
            # Boolean flags to indicate whether or not the A,B value is defined at a particular key
            Adef = False
            Bdef = False
            Aval = None
            Bval = None

            #This next block of code sets the Adef and Bdef flags
            #If both queues are nonempty
            if (len(Akeys) > 0) & (len(Bkeys) > 0):
                if Akeys[0] < Bkeys[0]:
                    Aval = Akeys.popleft()
                    Adef = True
                elif Akeys[0] > Bkeys[0]:
                    Bval = Bkeys.popleft()
                    Bdef = True
                elif Akeys[0] == Bkeys[0]:
                    Aval = Akeys.popleft()
                    Bval = Bkeys.popleft()
                    Adef = True
                    Bdef = True
            #If only Bkeys is empty
            elif (len(Akeys) > 0):
                Aval = Akeys.popleft()
                Adef = True
            # If only Akeys is empty
            elif (len(Bkeys) > 0):
                Bval = Bkeys.popleft()
                Bdef = True


            #This block of code calculates cost for a particular mapping in the
            # manner specified by the Adef and Bdef flags
            if (Adef & Bdef):
 #               UnusedA.remove(mapA[Aval])
 #               UnusedB.remove(mapB[Bval])
                cost += self.costOfPath(mapA[Aval], mapB[Bval])
                #Calculate shortest path, simple arithmetic required to find cost.
                print()
            elif (Adef & (Bdef == False)):
 #               UnusedA.remove(mapA[Aval])
                if(mapA[Aval] in Bvalues):
                    #Handle later
                    revisit.add((Aval, None))
                else:
                    UnusedB.remove(mapA[Aval])
                #else no cost incurred, mapping for mapA of this key value pair need not change.
            elif ((Adef == False) & Bdef):
#                UnusedB.remove(mapB[Bval])
                if (mapB[Bval] in Avalues):
                    # Handle later
                    revisit.add((None, Bval))
                else:
                    UnusedA.remove(mapB[Bval])
                #else no cost incurred, mapping for mapB of this key value pair can be propagated backward.

        while(len(revisit) > 0):
            ABval = revisit.pop()
            if(ABval[0] == None):
                #TODO: Get element from UnusedA, possibly using BFS to optimize
                cost += self.costOfPath(None, None)
                # Calculate shortest path, simple arithmetic required to find cost.
                print()
            elif(ABval[1] == None):
                # TODO: Get element from UnusedA, possibly using BFS to optimize
                cost += self.costOfPath(None, None)
                # Calculate shortest path, simple arithmetic required to find cost.
                print()

    def costOfPath(self, qubitA, qubitB):
        #get Shortest path
        path = self.shortestPath()
        #TODO: Traverse the path and determine cost
            #This is largely determined by whether or not there are
            # any undirected edges

    #Take as input a start qubit and a tuple of potential ending qubits.
    def shortestPath(self):
        print("Implement Dijkstra")

    def getIntermediateMapping(self, mapA, mapB):
        if(len(mapA) != len(mapB)):
            RuntimeError
        result = {}
        for i in range(0, len(mapA)):
            #key
            if( i in mapA.keys() ):


                print()






