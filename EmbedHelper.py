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

    CXcost = 2
    Hcost = 1

    def __init__(self, QCircuit, coupling):
        print("init")
       # self.Instruction = Instruction
        self.Segment = Segment
        self.Coupling = coupling
        self.UndirectedCoupling = self.directedToUndirected(coupling)
        self.QCircuit = QCircuit
        self.Instructions = self.reformatInstructions(QCircuit)
        self.Segments = []

    #Go through the directed graph coupling, and return the
    # same graph with undirected edges
    def directedToUndirected(self, coupling):
        UndirectedCoupling = {}
        for key in coupling.keys():
            UndirectedCoupling[key] = list(coupling[key])
        for key in coupling.keys():
            for value in coupling[key]:
                UndirectedCoupling[value].append(key)
        for key in UndirectedCoupling.keys():
            UndirectedCoupling[key] = tuple(UndirectedCoupling[key])

        return UndirectedCoupling


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




    #inputs are found mappings mapA, mapB
    # as well as the inverted equivalent of mapA mapB
    #Output is a tuple containing the minimmized MapA' MapB' and cost
    #Calculates cost of transforming from mapA to mapB
    #TODO Test finalMapB functionality
    #TODO Test cost function
    def cost(self, startmapA, startmapB, startinvA, startinvB):

        cost = 0

        MapB = copy.deepcopy(startmapB)
        MapA = copy.deepcopy(startmapA)
        InvA = copy.deepcopy(startinvA)
        InvB = copy.deepcopy(startinvB)

        swapPaths = set()

        # get the keys, sort them as a list and make them into a queue
        #Akeys = set(MapA.keys())
        #Bkeys = set(MapB.keys())

        Keys = MapA.keys() | MapB.keys()

        print(type(Keys))
        #Create a set for these values to achieve O(1) time for checking membership
        #Avalues = set(MapA.values())
        #Bvalues = set(MapB.values())

        Accessible = set(self.UndirectedCoupling.keys())
        UnusedA = Accessible - InvA.keys()
        UnusedB = Accessible - InvB.keys()

        #Aval and Bval will hold elements as they are popped off of Akeys and Bkeys
        #Aval and Bval correspond to the indices of states being embedded. Not the indices of the physical qubits.
        #Aval = None
        #Bval = None

        revisit = set()

        while (len(Keys) > 0):
            NextKey = Keys.pop()
            Aval = None
            Bval = None

            #This handles each line of the intermediate mappings in the
            # manner specified by the Adef and Bdef flags
            #if ((NextKey in MapA) & (NextKey in MapB)):
                #Aval = MapA[NextKey]
                #Bval = MapB[NextKey]
               #revisit.add((Aval,Bval))
                #Make note that this key has been handled.

            # (#, U, None)
            if ((NextKey in MapA) & (NextKey not in MapB)):

                Aval = MapA[NextKey]
                U = Aval
                Ukey = NextKey
                #Get key of Aval = *u

                while (True):
                    # Is Aval in mapB.values?
                    if U in InvB:
                        Ukey = InvB[U]
                        #If MapA is defined for key = Ukey
                        if Ukey in MapA:
                            U = MapA[Ukey]
                            continue
                        else:
                            #revisit.add((Aval, None))
                            revisit.add((NextKey, Ukey))
                            Keys.remove(Ukey)

                            #MapB[NextKey] = -1-Ukey  #Add a placeholder here! Negative entries refer to the logical indices which a qubit would map from
                            #InvB[-1-Ukey] = NextKey  # Ex Map[num] = -1-key means that logical qubit key's location is undefined, but that it must have
                            #MapA[Ukey] = -1-Ukey               # been swapped with location of logical qubit num in the previous map
                            #InvA[-1-Ukey] = Ukey
                            break
                    else:
                        MapB[NextKey] = U
                        InvB[U] = NextKey
                        UnusedB.remove(U)
                        break

            # (#, None, V)
            elif ((NextKey not in MapA) & (NextKey in MapB)):

                Bval = MapB[NextKey]
                V = Bval
                Vkey = NextKey
                # Get key of Aval = *u

                while (True):
                    # Is Bval in mapA.values?
                    if V in InvA:
                        Vkey = InvA[V]
                        # If MapB is defined for key = Vkey
                        if Vkey in MapB:
                            V = MapB[Vkey]
                           # if(V < 0)
                            continue
                        else:
                            revisit.add((Vkey, NextKey))
                            Keys.remove(Vkey)

                            #revisit.add((None, V))
                            #MapA[NextKey] = (-1 - Vkey)  # Add a placeholder here! Negative entries refer to the logical indices which a qubit would map from
                            #InvA[-1-Vkey] = NextKey  # Ex Map[num] = -1-key means that logical qubit key's location is undefined, but that it must have
                            #MapB[Vkey] = (-1 - Vkey)                   # been swapped with location of logical qubit num in the previous map
                            #InvB[-1-Vkey] = Vkey
                            break
                    else:
                        MapA[NextKey] = V
                        InvA[V] = NextKey
                        UnusedA.remove(V)
                        break


                """#NOTE a choice was made here.
        # I could have decided that for pairs (None, #),(#, None) that # must be the same for both resulting in a single
        # swap (or swap path). Instead, this way allows values to be swapped to locations that may be occupied in the
        # other mapping. In the future I may be able to compute the minimum between these two.
        while (len(revisit) > 0):
            pair = revisit.pop()

            if( pair[0] == None ):
                # Find a suitable qubit to transform from
                path = self.shortestPath(pair[1], UnusedA)

                MapA[InvB[pair[0]]] = path[0]
                InvA[path[0]] = InvB[pair[0]]
                UnusedA.remove(path[0])

            elif( pair[1] == None ):
                # Find a suitable qubit to transform from
                path = self.shortestPath(pair[0], UnusedB)
                MapB[InvA[pair[1]]] = path[0]
                InvB[path[0]] = InvA[pair[1]]
                UnusedB.remove(path[0])

            elif(pair == (None, None)):
                #Something is seriously wrong if this happens
                assert Exception


                """#Handle cases where algorithm has a choice of where to swap qubit values
        #By handling non-ambiguous cases first we can know which qubits will be available to swap with
        while(len(revisit) > 0):
            keys = revisit.pop()

            Aval = MapA[keys[0]]
            Bval = MapB[keys[1]]

            #wont use this until I have shortest path modified to work for two target qubits
            #path1 = self.shortestPath(Aval, UnusedB)
            #path2 = self.shortestPath(Bval, UnusedA)

            if(Aval == Bval):
                path = self.shortestPath(Aval, (UnusedA & UnusedB))
                MapB[keys[0]] = path[0]
                InvB[path[0]] = keys[0]
                MapA[keys[1]] = path[0]
                InvA[path[0]] = keys[1]

            else:
                path1 = self.shortestPath(Aval, UnusedB)

                MapB[keys[0]] = path1[0]
                InvB[path1[0]] = keys[0]

                path2 = self.shortestPath(Bval, UnusedA)

                MapA[keys[1]] = path2[0]
                InvA[path2[0]] = keys[1]

            """
            if(ABval[0] == None):
                #Find a suitable qubit to transform from
                path = self.shortestPath(mapB[ABval[1]], UnusedA)
                cost += self.costOfPath(path)
                print()
            elif(ABval[1] == None):
                #Find a suitable qubit to transform to
                path = self.shortestPath(mapA[ABval[0]], UnusedB)
                finalMapB[ABval[0]] = path[0]
                cost += self.costOfPath(path)"""
        print()

        return (cost, MapA, MapB)

    def invertMap(self, map):
        invMap = {}
        for key in map.keys():
            invMap[map[key]] = key
        return invMap

    #Takes as input a list of adjacent nodes
    def costOfPath(self, path):
        cost = 0;
        node = path.pop()


        while path:
            nextNode = path.pop()

            if (len(path) == 0):
                if (nextNode in self.Coupling[node]) & (node in self.Coupling[nextNode]):
                    cost += (self.CXcost * 3)
                else:
                    cost += (self.CXcost * 3 + self.Hcost * 4)
                return cost

            if (nextNode not in self.Coupling[node]) & (node not in self.Coupling[nextNode]):
                raise Exception("Invalid Path")
            if (nextNode in self.Coupling[node]) & (node in self.Coupling[nextNode]):
                cost += (self.CXcost * 3) * 2
            else:
                cost += (self.CXcost * 3 + self.Hcost * 4) * 2


            node = nextNode




    #Take as input a start qubit and
    # either a single or tuple of potential ending qubits.
    # returns a list specifying the path from end to start
    def shortestPath(self, start, ends):
        visited = set()
        traceback = {start: None}
        discovered = [start]
        while discovered:
            vertex = discovered.pop(0)
            if vertex not in visited:

                #If a single endpoint is given
                if isinstance(ends, int):
                    #single end point
                    if vertex == ends:
                        path = list()
                        path.append(ends)
                        parent = traceback[ends]
                        while parent != None:
                            path.append(parent)
                            parent = traceback[parent]
                        return path

                #If a list of possible endpoints is given
                if isinstance(ends, set):
                    # single end point
                    if vertex in ends:
                        path = list()
                        path.append(vertex)
                        parent = traceback[vertex]
                        while parent != None:
                            path.append(parent)
                            parent = traceback[parent]
                        return path


                visited.add(vertex)
                for child in set(self.UndirectedCoupling[vertex]):
                    if (child not in visited) & (child not in discovered):
                        discovered.append(child)
                        traceback[child] = vertex

        return None

    def selectSegments(self, segments):


        traceback = []
        costs = []
        qubitMappings = []

        #Corner case, first mapping

        for segment in range(0, segments):

            qubitMappings[segment] = []
            costs[segment] = []
            traceback[segment] = []

            for mapping in segment.global_maps:

                if segment == 0:
                    costs[segment][mapping] = 0;
                    qubitMappings[mapping] = copy.deepcopy(segments[segment].global_maps[mapping])

                else:
                    qubitMappings[mapping] = copy.deepcopy(segments[segment].global_maps[mapping])
                    for previousMap in segments[segment-1].global_maps:
                        minCost = self.cost(previousMap, mapping, ) #TODO think about having cost return the cost and mapping
                        print()












