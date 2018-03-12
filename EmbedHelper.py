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
                if value in UndirectedCoupling:
                    UndirectedCoupling[value].append(key)
                else:
                    UndirectedCoupling[value] = (key,)
        #for key in UndirectedCoupling.keys():
        #    UndirectedCoupling[key] = tuple(UndirectedCoupling[key])

        return UndirectedCoupling


    def isValid(self, qubit1, qubit2):

        print("HELPER")

        if qubit1 in self.Coupling and qubit2 in self.Coupling[qubit1]:
            return True

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
    def cost(self, prevcost, traceback,  startmapA, startmapB):

        cost = 0
        #Maps logial qubit to physical qubit
        MapB = copy.deepcopy(startmapB)
        MapA = copy.deepcopy(startmapA)
        #Note, it is possible to pass in and store all of the inverted maps
        #Inv maps Physical Qubit to Logical Qubit
        InvA = self.invertMap(MapA)
        InvB = self.invertMap(MapB)


        # get the keys, sort them as a list and make them into a queue
        #Akeys = set(MapA.keys())
        #Bkeys = set(MapB.keys())
        Keys = MapA.keys() | MapB.keys()

        #Create a set for these values to achieve O(1) time for checking membership
        #Avalues = set(MapA.values())
        #Bvalues = set(MapB.values())

        Accessible = self.UndirectedCoupling.keys()
        UnusedA = Accessible - InvA.keys()
        UnusedB = Accessible - InvB.keys()


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


        #NOTE a choice was made here.
        # I decided that for pairs (None, #),(#, None) that # must be the same for both resulting in a single
        # swap (or swap path). If however, an incomplete cycle is broken by (None, #),(#', None) where #,#' are not
        # equivalent. Then the algorithm finds the closest available qubit to each value.
        #=======================================================================
        #Handle cases where algorithm has a choice of where to swap qubit values
        #By handling non-ambiguous cases first we can know which qubits will be available to swap with
        print()
        while(len(revisit) > 0):
            keys = revisit.pop()

            Aval = MapA[keys[0]]
            Bval = MapB[keys[1]]

            if(Aval == Bval):
                path = self.shortestPath(Aval, (UnusedA & UnusedB))
                MapB[keys[0]] = path[0]
                InvB[path[0]] = keys[0]
                MapA[keys[1]] = path[0]
                InvA[path[0]] = keys[1]
                UnusedA.remove(path[0])
                UnusedB.remove(path[0])

            #Note, this is where the bug is, need to fix this part.
            else:
                path1 = self.shortestPath(Aval, UnusedB)
                MapB[keys[0]] = path1[0]
                InvB[path1[0]] = keys[0]
                UnusedB.remove(path1[0])

                path2 = self.shortestPath(Bval, UnusedA)
                MapA[keys[1]] = path2[0]
                InvA[path2[0]] = keys[1]
                UnusedA.remove(path2[0])


        #If somehow both maps are not filled out then something is horribly awry.
        # Program should implode so it does not output nonsense.
        if(len(MapA.keys()) != (MapB.keys())):
            assert Exception

        #Now we will generate the list of swap paths, and convert this into the list of swap gates.
        #From here we can return a cost based upon the solution we have found
        valid = 0
        swapPaths = []
        InvKeys = InvA.keys() | InvB.keys()

        #Get a copy of InvA we can modify without destroying original
        TinvA = copy.deepcopy(InvA)

        while(valid < len(InvKeys)):
            for key in InvKeys:

                if(key in TinvA and key in InvB):
                    if(TinvA[key] != InvB[key]):
                        toSwap = MapB[TinvA[key]]
                        #Swap key and toSwap
                        swapPaths.append((key,toSwap))
                        if(toSwap in TinvA):
                            temp = TinvA[key]
                            TinvA[key] = TinvA[toSwap]
                            TinvA[toSwap] = temp
                        else:
                            TinvA[toSwap] = TinvA[key]
                            TinvA.pop(key)
                        break
                elif (key in TinvA and key not in InvB):
                    toSwap = MapB[TinvA[key]]
                    swapPaths.append((key, toSwap))
                    if (toSwap in TinvA):
                        temp = TinvA[key]
                        TinvA[key] = TinvA[toSwap]
                        TinvA[toSwap] = temp
                    else:
                        TinvA[toSwap] = TinvA[key]
                        TinvA.pop(key)
                    break
                elif (key not in TinvA and key in InvB):
                    toSwap = MapA[InvB[key]]
                    swapPaths.append((key, toSwap))
                    TinvA[key] = TinvA[toSwap]
                    TinvA.pop(toSwap)
                    break
            else:
                    break
            continue

        swaps = list()
        #Expand swapPaths into an actual sequence of swap gates.
        for sp in swapPaths:
            path = self.shortestPath(sp[0],sp[1])
            if(len(path) == 2):
                swaps.append(path)
            else:
                for i in range(len(path)-2):
                    swaps.append((path[i],path[i+1]))
                for i in range(len(path)-1):
                    swaps.append((path[-i-2],path[-i-1]))


        for swap in swaps:
            forward  = False
            backward = False
            if swap[0] in self.Coupling and swap[1] in self.Coupling[swap[0]]:
                forward = True
            if swap[1] in self.Coupling and swap[0] in self.Coupling[swap[1]]:
                backward = True

            if(forward and backward):
                cost += 3 * self.CXcost
            elif( forward or backward):
                cost += 3 * self.CXcost
                cost += 4 * self.Hcost
            else:
                assert Exception

        return (cost + prevcost, traceback, swaps, MapA, MapB)

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

    def memoize(self, nodemap, k, sources):
        #"""     print(k)
     if type(sources) == dict:
         #node.append(self.cost(sources, nodemap))
         return self.cost(0, -1, sources, nodemap)
         print()
     if k == 0:
         costs = []
         min = None

        #TODO Needs to be fixed to reflect accumulated costs
         if type(sources) == list:
             #DO actual memoization with costs
             for source in range(len(sources)):
                 costs = (self.cost(sources[source][0], source, sources[source][4], nodemap))
                 #costs[0] = costs[0] + sources[source][0]
                 if min == None:
                     min = costs
                 if min[0] > costs[0]:
                     min = costs
             return min
         else:
             assert Exception

     else:
         nodeArray = []
         for targetnode in range(len(sources)):
             nodeArray.append(self.memoize(nodemap, k-1, sources[targetnode]))
         return nodeArray
     print()
#"""
     print()

    def selectSegments(self, segments, k=None):

        if k==None: dim = 1
        #traceback = []
        #costs = []
        qubitMappings = {}

        #Corner case, only one mapping
        if len(segments) == 1:
            return segments[0].global_maps[0]
        #Fill out the memoization table
        for segment in range(0, len(segments)):
            qubitMappings[segment] = []
            #costs[segment] = []
            #traceback[segment] = []
            if segment == 0:
                #qubitMappings[segment] = []
                for node in range(len(segments[segment].global_maps)):
                    qubitMappings[segment].append(segments[segment].global_maps[node])
                continue

            #qubitMappings[segment] = []
            for node in range(len(segments[segment].global_maps)):

                nodemap = segments[segment].global_maps[node]
                qubitMappings[segment].append([])
                qubitMappings[segment][node] = self.memoize(nodemap, k, qubitMappings[segment - 1])
                print()
            print()
        #trace over the table and recover the best found mapping sequence.
        print()
        return qubitMappings





