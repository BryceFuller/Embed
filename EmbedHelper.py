import copy
from qiskit import QuantumCircuit, QuantumProgram
import qiskit
import inspect
import heapq as H
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
        #print(inspect.getfile(qiskit))
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
        self.Segment = Segment
        self.Coupling = self.cleanCoupling(coupling)
        self.UndirectedCoupling = self.directedToUndirected(coupling)
        self.QCircuit = QCircuit
        self.Instructions = self.reformatInstructions(QCircuit)
        self.Segments = []
        self.Verbose = True
        self.HasCycles = self.hasCycles()


    #Change all values of a dict to be tuples
    def cleanCoupling(self, coupling):
        NewCoupling = {}
        for key in coupling.keys():
            for value in coupling[key]:
                if key not in NewCoupling.keys():
                    NewCoupling[key] = (value,)
                elif value not in NewCoupling[key]:
                    NewCoupling[key] = NewCoupling[key] + (value,)
        return NewCoupling

    #Go through the directed graph coupling, and return the
    # same graph with undirected edges
    def directedToUndirected(self, coupling):
        UndirectedCoupling = {}
        for key in coupling.keys():
            UndirectedCoupling[key] = tuple(coupling[key])
        for key in coupling.keys():
            for value in coupling[key]:
                if value in UndirectedCoupling:
                    if key not in UndirectedCoupling[value]:
                        UndirectedCoupling[value] = UndirectedCoupling[value] + (key,)
                else:
                    UndirectedCoupling[value] = (key,)
        return UndirectedCoupling

    #Indicate whether or not this graph has cycles
    def hasCycles(self):
        available = set()
        visited = set()
        traceback = {}

        node = list(self.UndirectedCoupling)[0]
        for i in self.UndirectedCoupling[node]:
            available.add(i)
            traceback[i] = node
        visited.add(node)

        while len(available) > 0:
            node = available.pop()
            visited.add(node)
            for i in self.UndirectedCoupling[node]:
                if (i in visited):
                    if (traceback[node] != i):
                        return True
                else:
                    available.add(i)
                    traceback[i] = node
            node = available.pop()

        return False

    #Can qubit1 control onto qubit2, returns boolean value
    def isValid(self, qubit1, qubit2):
        if qubit1 in self.Coupling and qubit2 in self.Coupling[qubit1]:
            return True
        return False

    #Convert QCircuit object to intermediate representation
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

            #TODO make this for single qubit gates only
            if (Instruction.operation != "cx"):
                subsegment.endIndex = subsegment.endIndex + 1
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
                        if qubit1 in map.values():
                            continue
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

    def extendBackward(self, start, end, subsegment):
        for instr in range(start - 1, end):

            Instruction = self.Instructions[instr];

            if (len(Instruction.qubits) == 1):
                subsegment.endIndex = subsegment.endIndex + 1
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
                        if qubit1 in map.values():
                            continue
                        for qubit2 in self.Coupling[qubit1]:
                            if qubit2 in map.values():
                                continue
                            if self.isValid(qubit1, qubit2):
                                newMap = copy.deepcopy(map)
                                newMap[control] = qubit1
                                newMap[target] = qubit2
                                newMaps.append(newMap)
                                subsegment.startIndex = instr;
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
                            subsegment.startIndex = instr;
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
                            subsegment.startIndex = instr;
                    continue

                if (startFixed == True) & (endFixed == True):
                    qubit1 = map[control]
                    qubit2 = map[target]
                    if self.isValid(qubit1, qubit2):
                        newMaps.append(map)
                        subsegment.startIndex = instr;
                    continue
            if(len(newMaps) != 0):
                subsegment.global_maps = newMaps;




    #inputs are mappings mapA, mapB
    # as well as the inverted versions of mapA mapB
    #Output is a tuple containing the minimmized MapA' MapB',
    # MapA and MapB's inverses, the cost, and the swap sequence
    # which transforms from MapA to MapB
    #Calculates cost of transforming from mapA to mapB

    def cost(self, prevcost, traceback,  startmapA, startmapB):

        cost = 0
        #Maps logial qubit to physical qubit
        MapB = copy.deepcopy(startmapB)
        MapA = copy.deepcopy(startmapA)
        InvA = self.invertMap(MapA)
        InvB = self.invertMap(MapB)

        Keys = MapA.keys() | MapB.keys()

        Accessible = self.UndirectedCoupling.keys()
        UnusedA = Accessible - InvA.keys()
        UnusedB = Accessible - InvB.keys()

        revisit = set()

        while (len(Keys) > 0):
            NextKey = Keys.pop()
            Aval = None
            Bval = None

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
                            revisit.add((NextKey, Ukey))
                            Keys.remove(Ukey)

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
        while(len(revisit) > 0):
            keys = revisit.pop()

            Aval = MapA[keys[0]]
            Bval = MapB[keys[1]]

            if(Aval == Bval):
                targets = (UnusedA & UnusedB)
                if len(targets) > 0:
                    path = self.shortestPath(Aval, targets)
                    MapB[keys[0]] = path[0]
                    InvB[path[0]] = keys[0]
                    UnusedB.remove(path[0])
                    MapA[keys[1]] = path[0]
                    InvA[path[0]] = keys[1]
                    UnusedA.remove(path[0])
                elif len(targets) == 0:
                    pathA = self.shortestPath(Aval, UnusedA)
                    MapA[keys[1]] = pathA[0]
                    InvA[pathA[0]] = keys[1]
                    UnusedA.remove(pathA[0])
                    pathB = self.shortestPath(Bval, UnusedB)
                    MapB[keys[0]] = pathB[0]
                    InvB[pathB[0]] = keys[0]
                    UnusedB.remove(pathB[0])
            else:
                path1 = self.shortestPath(Aval, UnusedB)
                MapB[keys[0]] = path1[0]
                InvB[path1[0]] = keys[0]
                UnusedB.remove(path1[0])

                path2 = self.shortestPath(Bval, UnusedA)
                MapA[keys[1]] = path2[0]
                InvA[path2[0]] = keys[1]
                UnusedA.remove(path2[0])


        #If somehow both maps are not defined for the same set of keys then something is horribly wrong.
        #Program should implode so it does not output nonsense.
        if(MapA.keys() != MapB.keys()):
            assert Exception

        #Now we will generate a list of swap paths, and convert this into a list of swap gates.
        #From here we can return a cost based upon the solution we have found
        valid = 0
        swapPaths = []
        InvKeys = InvA.keys() | InvB.keys()

        if self.HasCycles == True:
            mst = self.MST(MapA.values())
        else:
            mst = None

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
            path = self.shortestPath(sp[0],sp[1],mst)
            if(len(path) == 2):
                swaps.append(tuple(path))
            else:
                for i in range(len(path)-2):
                    swaps.append((path[i],path[i+1]))
                for i in range(len(path)-1):
                    swaps.append((path[-i-2],path[-i-1]))

        #DISTILL SWAP GATES
        #oldswaps = copy.deepcopy(swaps)
        #swaps = self.distillSwaps(swaps)

        #if not self.verifySwapDistillation(oldswaps, swaps):
        #    assert Exception

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



    def distillSwaps(self, swaps):
        a = None
        b = None
        c = None

        #Debugging stuff
        swaps2 = copy.deepcopy(swaps)
        swaps3 = copy.deepcopy(swaps)
        #/////////

        while True:
            swaps4 = copy.deepcopy(swaps3)
            self.simplifyOnce(swaps3)
            if not self.verifySwapDistillation(swaps2,swaps3):
                print("not good")
                assert Exception
                print("should be unreachable")
                return swaps4
            if not self.simplifyOnce(swaps):
                break
            if not self.verifySwapDistillation(swaps2, swaps):
                assert Exception
        # print("-> " + str(len(swaps)))
        return swaps



    def simplifyOnce(self, swaps):

        for sw in range(len(swaps)):

            T1Elems = set()
            T1Elems.add(swaps[sw][0])
            T1Elems.add(swaps[sw][1])

            # If there's an identity mapping...
            if len(T1Elems) == 1:
                assert Exception
                print("HANDLE THIS")

            # If there's room for permutations
            if sw + 1 < len(swaps):
                permutable1, elems1 = self.canPermute(swaps[sw],swaps[sw+1])

                # These two cancel
                if len(elems1) == 2:
                    swaps.pop(sw + 1)
                    swaps.pop(sw)
                    return True

            else:
                permutable1 = False

            # i, i+1 can be permuted
            if permutable1:

                if sw+3 < len(swaps):
                    permutable2, elems2 = self.canPermute(swaps[sw+2], swaps[sw+3])

                    #i+2, i+3 can be permuted
                    if permutable2:

                        ComElems = set(elems1) & set(elems2)

                        if len(ComElems) >= 2:
                            cancel = set()
                            cancel.add(ComElems.pop())
                            cancel.add(ComElems.pop())
                            remainder1 = ()
                            remainder2 = ()
                            if elems1[0] in cancel and elems1[1] in cancel: remainder1 = (elems1[1], elems1[2])
                            if elems1[0] in cancel and elems1[2] in cancel: remainder1 = (elems1[1], elems1[0])
                            if elems1[1] in cancel and elems1[2] in cancel: remainder1 = (elems1[2], elems1[0])
                            if elems2[0] in cancel and elems2[1] in cancel: remainder2 = (elems2[2], elems2[0])
                            if elems2[0] in cancel and elems2[2] in cancel: remainder2 = (elems2[2], elems2[1])
                            if elems2[1] in cancel and elems2[2] in cancel: remainder2 = (elems2[0], elems2[1])
                            swaps[sw] = remainder1
                            swaps[sw + 3] = remainder2
                            swaps.pop(sw + 2)
                            swaps.pop(sw + 1)
                            return True


                # i+2, i+3 are not permutable
                else:
                    if self.checkTranslation(swaps, (elems1[0],elems1[1]), sw, True):
                        swaps[sw - 1] = (elems1[0],elems1[2])
                        return True
                    if self.checkTranslation(swaps, (elems1[0], elems1[2]), sw, True):
                        swaps[sw - 1] = (elems1[1], elems1[2])
                        return True
                    if self.checkTranslation(swaps, (elems1[1], elems1[2]), sw, True):
                        swaps[sw - 1] = (elems1[0], elems1[1])
                        return True
                    if self.checkTranslation(swaps, (elems1[0], elems1[1]), sw+1, False):
                        swaps[sw-2] = (elems1[1], elems1[2])
                        return True
                    if self.checkTranslation(swaps, (elems1[0], elems1[2]), sw+1, False):
                        swaps[sw-2] = (elems1[1], elems1[2])
                        return True
                    if self.checkTranslation(swaps, (elems1[1], elems1[2]), sw+1, False):
                        swaps[sw-2] = (elems1[0], elems1[1])
                        return True

            else: #i,i+1 cannot be permuted, so check for translations
                if self.checkTranslation(swaps, swaps[sw], sw, True): return True
                if self.checkTranslation(swaps, swaps[sw], sw, False): return True
        return False

    def canPermute(self, swap1, swap2):
        Elems1, Elems2 = set(), set()
        Elems1.add(swap1[0])
        Elems1.add(swap1[1])
        Elems2.add(swap2[0])
        Elems2.add(swap2[1])
        Elems = Elems1 | Elems2
        if len(Elems) == 3:
            a = (Elems1 & Elems2)
            b = (Elems1 - a).pop()
            c = (Elems2 - a).pop()
            a = a.pop()
            if c in self.UndirectedCoupling[b]:
                return True, [a,b,c]
            else:
                return False, [a,b,c]
        return False, list(Elems)

    #Check if a swap sw at index i can be translated up, or down (Up=False) to get a cancellation
    #If a cancellation is found, it is removed,
    def checkTranslation(self, swaps, sw, i, Up=True):
        if Up:
            for j in range(1,i):
                elems = set()
                elems.add(swaps[i - j][0])
                elems.add(swaps[i - j][1])
                if sw[0] in elems and sw[1] in elems:
                    swaps.pop(i)
                    swaps.pop(i-j)
                    return True
                if sw[0] not in elems and sw[1] not in elems:
                    continue
                return False

        else: #For Down
            for j in range(1, len(swaps)-i):
                elems = set()
                elems.add(swaps[i + j][0])
                elems.add(swaps[i + j ][1])
                if sw[0] in elems and sw[1] in elems:
                    swaps.pop(i + j)
                    swaps.pop(i)
                    return True
                if sw[0] not in elems and sw[1] not in elems:
                    continue
                return False

    #def cancel(self,):
    def verifySwapDistillation(self, init, final):
        map1 = {}
        map2 = {}
        for sw in init:
            if sw[0] not in map1:
                map1[sw[0]] = sw[0]
            if sw[1] not in map1:
                map1[sw[1]] = sw[1]
            temp = map1[sw[0]]
            map1[sw[0]] = map1[sw[1]]
            map1[sw[1]] = temp

        for sw in final:
            if sw[0] not in map2:
                map2[sw[0]] = sw[0]
            if sw[1] not in map2:
                map2[sw[1]] = sw[1]
            temp = map2[sw[0]]
            map2[sw[0]] = map2[sw[1]]
            map2[sw[1]] = temp

        if map1 != map2:
            return False
        return True

    def score(self, coupling, targets, node):
        score = 0
        # print(coupling, targets, node)
        for i in self.UndirectedCoupling[node]:
            if i in targets:
                score = score + 1
        return score

    #Takes in a list of target nodes and returns an undirected MST between those nodes.
    def MST(self, targs):
        MST = {}
        UC = self.UndirectedCoupling
        if len(targs) == 0:
            assert Exception

        accessible = []
        visited = set()
        targets = set(targs)
        target = targets.pop()
        while len(targets) > 0:

            visited.add(target)
            tscore = self.score(UC, targs, target)

            for i in UC[target]:
                if i not in visited:
                    Score = float(1 / (self.score(UC, targs, i) + tscore))
                    H.heappush(accessible, (Score, (i, target)))

            Min = H.heappop(accessible)
            VisitedNode = Min[1][1]
            NewNode = Min[1][0]

            if NewNode not in MST.keys():
                if VisitedNode not in MST:
                    MST[VisitedNode] = (NewNode,)
                else:
                    MST[VisitedNode] = MST[VisitedNode] + (NewNode,)
                MST[NewNode] = (VisitedNode,)

            target = Min[1][0]
            if target in targets:
                targets.remove(target)

        return MST

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
    def shortestPath(self, start, ends, connectivity=None):
        visited = set()
        traceback = {start: None}
        discovered = [start]
        if connectivity == None:
            connectivity = self.UndirectedCoupling
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

    def memoize(self, nodemap, sources, k):
        # """     print(k)
        if type(sources) == dict:
            # node.append(self.cost(sources, nodemap))
            return self.cost(0, -1, sources, nodemap)
            # Note, the -1 traceback serves as an indicator that this tuple needs no additional information
            # to describe it's predecessor. This was not the max tuple for an array of possible source

        if k == 0:
            costs = []
            min = None

            if (type(sources) == list):
                if (type(sources[0]) == tuple):
                    # DO actual memoization with costs
                    for source in range(len(sources)):
                        # costs = (self.cost(sources[source][0], source, sources[source][4], nodemap))
                        if sources[source] == None:
                            continue
                        costs = (self.cost(sources[source][0], source, sources[source][4], nodemap))

                        # costs[0] = costs[0] + sources[source][0]
                        if min == None:
                            min = costs
                        if min[0] > costs[0]:
                            min = costs
                    return min
                if (type(sources[0]) == dict):
                    for source in range(len(sources)):
                        if sources[source] == None:
                            continue
                        costs = self.cost(0, source, sources[source], nodemap)
                        # costs[0] = costs[0] + sources[source][0]
                        if min == None:
                            min = costs
                        if min[0] > costs[0]:
                            min = costs
                    return min
                if (type(sources[0]) == list):
                    for source in range(len(sources)):
                        if sources[source] == None:
                            continue
                        costs = self.memoize(nodemap, sources[source], 0);
                        if min == None:
                            min = costs
                        if min[0] > costs[0]:
                            min = costs
                    return min
            else:
                if (type(sources) == tuple):
                    return self.cost(sources[0], -1, sources[4], nodemap)

                if (type(sources) == dict):
                    return self.cost(0, -1, sources, nodemap)
                #assert Exception("Memoize called with type(sources) != list of tuples or dicts")

        else:
            nodeArray = []
            for targetnode in range(len(sources)):
                nodeArray.append(self.memoize(nodemap, sources[targetnode], k - 1))
            return nodeArray

    def getMin(self, node):
        if node == None:
            return None
        if type(node) == tuple:
            return node, ()
        if type(node) == list:
            minI = 0
            min = None
            for i in range(len(node)):
                if node[i] == None:
                    continue
                mapping, prevI = self.getMin(node[i])
                if mapping == None:
                    continue
                if min == None:
                    min = mapping
                    minI = (i,) + prevI
                    continue
                elif min[0] > mapping[0]:
                    min = mapping
                    minI = (i,) + prevI
            return min, minI

    def grabElement(self, searchSpace, location):
        # print()
        if len(location) == 1:
            if type(searchSpace[location[0]]) != tuple:
                assert Exception  # something is wrong with traceback. Misaligned data structures.
            return searchSpace[location[0]]
        elif (len(location) == 2) & (location[-1] == -1):
            # return searchSpace[location[0]]
            assert Exception  # Should never get here. Tracebacks of -1 are not appended.
        else:

            element = self.grabElement(searchSpace[location[0]], location[1:])
            return element


    #Traceback written for k=0 only
    def traceback1(self, qubitMappings):
        optSegs = [] #Room to optimize by making this a deque
        end = self.getMin(qubitMappings[-1])
        prevSeg = end
        optSegs.append(end[0])
        for segment in range(len(qubitMappings) - 1, 0, -1):
            index = prevSeg[0][1]
            node = qubitMappings[segment][index]

    def traceback2(self, qubitMappings):
        optSegs = []  # Room to optimize by making this a deque
        prevSeg, nextIndex = self.getMin(qubitMappings[-1])
        cost = prevSeg[0]
        #prevSeg = end
        # index = end[1]
        optSegs.append((prevSeg[4],[]))
        optSegs.append((prevSeg[3], prevSeg[2]))
        for segment in range(len(qubitMappings) - 2, 0, -1):

            nextIndex = tuple(list(nextIndex)[1:])
            #if type(prevSeg) == list:
            if prevSeg[1] == -1:
                # nextIndex contains all relevant information.
                prevSeg = self.grabElement(qubitMappings[segment], nextIndex)
                optSegs.append((prevSeg[3], prevSeg[2]))
                continue

            else:
                nextIndex = nextIndex + (prevSeg[1],)
                prevSeg = self.grabElement(qubitMappings[segment], nextIndex)
                optSegs.append((prevSeg[3], prevSeg[2]))
                continue

            assert Exception("Unexpected Type")
        return optSegs, cost


    def localSelect(self, segments):

        qubitMappings = []

        # Corner case, only one segment
        if len(segments) == 1:
            return [segments[0].global_maps[0]], 0

        # Fill out the memoization table
        for segment in range(0, len(segments)):
            #if (self.Verbose): print("Generating layer ", segment, " in memoization table")
            qubitMappings.append([])

            if segment == 0:
                for node in range(len(segments[segment].global_maps)):
                    qubitMappings[segment].append(segments[segment].global_maps[node])
                continue

            for node in range(len(segments[segment].global_maps)):

                endmap = segments[segment].global_maps[node]
                qubitMappings[segment].append([])
                qubitMappings[segment][node] = self.memoize(endmap, qubitMappings[segment - 1],0)

        #Find end node that minimizes cost
        minCost, minIndex = 0, 0
        minCost = qubitMappings[-1][0][0]
        for map in range(len(qubitMappings[-1])):
            if qubitMappings[-1][map][0] < minCost:
                minCost = qubitMappings[-1][map][0]
                minIndex = map

        optSegments = []
        optSegments.append( (qubitMappings[-1][minIndex][4],list()) )
        optSegments.append((qubitMappings[-1][minIndex][3],qubitMappings[-1][minIndex][2]))
        childIndex = qubitMappings[-1][minIndex][1]

        # Traceback through the table
        for segment in range(len(segments)-2, 0, -1):
            child = qubitMappings[segment][childIndex]
            optSegments.append((child[3], child[2]))
            if type(child) != dict:
                childIndex = child[1]

        #Backpropogate qubit assignments

        for mapping in range(1,len(optSegments)):
            mapB = optSegments[mapping-1][0]
            mapA = optSegments[mapping][0]

            for key in mapB.keys():
                if key in mapA.keys():
                    if mapA[key] != mapB[key]:
                        assert Exception
                else:
                    mapA[key] = mapB[key]

        optSegments.reverse()
        return optSegments, minCost

    def selectSegments(self, segments, k=None):

       # if (self.Verbose): print("Selecting Segment Mappings")
        # if k==None
        # traceback = []
        # costs = []

        qubitMappings = []

        # Corner case, only one mapping
        if len(segments) == 1:
            return segments[0].global_maps[0]
        # Fill out the memoization table
        for segment in range(0, len(segments)):
            #if(self.Verbose): print("Generating layer ", segment, " in memoization table")
            qubitMappings.append([])
            # costs[segment] = []
            # traceback[segment] = []

            if segment == 0:
                # qubitMappings[segment] = []
                for node in range(len(segments[segment].global_maps)):
                    qubitMappings[segment].append(segments[segment].global_maps[node])
                continue

            # qubitMappings[segment] = []
            for node in range(len(segments[segment].global_maps)):
                nodemap = segments[segment].global_maps[node]
                qubitMappings[segment].append([])

                #keff = min(k, segment - 1)
                keff = min(k, segment)

                qubitMappings[segment][node] = self.memoize(nodemap, qubitMappings[segment - 1], keff)


        optSegments, cost = self.traceback2(qubitMappings)

        for mapping in range(1,len(optSegments)):
            mapB = optSegments[mapping-1][0]
            mapA = optSegments[mapping][0]

            for key in mapB.keys():
                if key in mapA.keys():
                    if mapA[key] != mapB[key]:
                        assert Exception
                else:
                    mapA[key] = mapB[key]

        optSegments.reverse()
        return optSegments, cost


    def swap(self, Circuit,q, arg0, arg1):
        forward = False
        backward = False
        if arg0 in self.Coupling.keys():
            if arg1 in self.Coupling[arg0]:
                forward = True
        if arg1 in self.Coupling.keys():
            if arg0 in self.Coupling[arg1]:
                backward = True

        if forward and not backward:
            Circuit.cx(q[arg0], q[arg1])
            Circuit.h(q[arg0])
            Circuit.h(q[arg1])
            Circuit.cx(q[arg0], q[arg1])
            Circuit.h(q[arg1])
            Circuit.h(q[arg0])
            Circuit.cx(q[arg0], q[arg1])
        if backward and not forward:
            Circuit.cx(q[arg1], q[arg0])
            Circuit.h(q[arg0])
            Circuit.h(q[arg1])
            Circuit.cx(q[arg1], q[arg0])
            Circuit.h(q[arg1])
            Circuit.h(q[arg0])
            Circuit.cx(q[arg1], q[arg0])
        if backward and forward:
            Circuit.cx(q[arg0], q[arg1])
            Circuit.cx(q[arg1], q[arg0])
            Circuit.cx(q[arg0], q[arg1])
        if not backward and not forward:
            assert Exception


    def RebuildCircuit(self,optSegments, segments):
        QCircuit = self.QCircuit
        Q_program = QuantumProgram()
        q = Q_program.create_quantum_register("qubits", len(self.UndirectedCoupling.keys()))
        c = Q_program.create_classical_register("bits", len(self.UndirectedCoupling.keys()))
        NewCircuit = Q_program.create_circuit("NewCircuit", [q], [c])

        for segment in range(len(segments)):
            for i in range(segments[segment].startIndex, segments[segment].endIndex + 1):
                command = QCircuit.data[i].name
                single = len(QCircuit.data[i].arg) == 1
                double = len(QCircuit.data[i].arg) == 2

                if (not single and not double):
                    assert Exception  # Undefined use case: 3-qubit gates

                if (single):
                    arg0 = QCircuit.data[i].arg[0][1]
                    if (arg0 not in optSegments[segment][0].keys()):
                        assert Exception
                    arg0 = optSegments[segment][0][arg0]
                    instr = "NewCircuit." + command + "("
                    instr += ",".join(list(map(str,QCircuit.data[i].param))+[""])
                    instr += "q[" + str(arg0) + "])"
                    exec(instr)

                if (double):
                    arg0 = QCircuit.data[i].arg[0][1]
                    arg1 = QCircuit.data[i].arg[1][1]
                    if (arg0 not in optSegments[segment][0].keys()) or (arg1 not in optSegments[segment][0].keys()):
                        assert Exception  # Something terrible happened.
                    arg0 = optSegments[segment][0][arg0]
                    arg1 = optSegments[segment][0][arg1]  # TODO test this part, I never got to it

                    if isinstance(QCircuit.data[i], qiskit._measure.Measure):
                        instr = "NewCircuit." + command + "(q[" + str(arg0) + "], c[" + str(arg1) + "])"
                    else:
                        instr = "NewCircuit." + command + "(q[" + str(arg0) + "], q[" + str(arg1) + "])"

                    #print(instr)
                    exec(instr)


            print  # NOW do all the swap gates.
            if len(optSegments) > 1:
                for swap in optSegments[segment][1]:
                    #print("swap(" + str(swap[0]) + ", " + str(swap[1]) + ")")
                    self.swap(NewCircuit, q, swap[0], swap[1])

        return NewCircuit

