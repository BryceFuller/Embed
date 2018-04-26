import copy
#from qiskit import QuantumCircuit, QuantumProgram

#import EmbedHelper.Verbose


def Greedy(helpers):
    QCircuit = helpers.QCircuit
    Coupling = helpers.Coupling

    qreg_name = list(QCircuit.get_qregs())[0]
    numQubits = QCircuit.regs[qreg_name].size

    instructions = helpers.Instructions
    segments = helpers.Segments

    cutoff = len(instructions);

    end = 0
    start = 0

    while(end < cutoff):

        # greedily grow segment
        segment = helpers.getSegment(start, end)
        end = end + 1

        while (end < cutoff):

            backup = copy.deepcopy(segment)
            segment = helpers.getSegment(start, end, segment)
            if(segment.endIndex != end):
                break
            else:
                end = end + 1

        start = segment.endIndex + 1
        segments.append(segment)
        if (helpers.Verbose): print("Segment ",len(segments)-1,"found with: ",len(segments[-1].global_maps) )

    return segments
    #Select a map for each segment (greedily)
    """
    return optSegments

    Q_program = QuantumProgram()
    q = Q_program.create_quantum_register("qubits", len(helpers.UndirectedCoupling.keys()))
    c = Q_program.create_classical_register("bits", len(helpers.UndirectedCoupling.keys()))
    NewCircuit = Q_program.create_circuit("NewCircuit", [q], [c])



    for segment in range(len(segments)):
        for i in range(segments[segment].startIndex,segments[segment].endIndex+1):
            command = QCircuit.data[i].name
            single = len(QCircuit.data[i].arg) == 1
            double = len(QCircuit.data[i].arg) == 2

            if( not single and not double):
                assert Exception #Undefined use case: 3-qubit gates


            if(single):
                arg0 = QCircuit.data[i].arg[0][1]
                if (arg0 not in optSegments[segment][0].keys()):
                    assert Exception
                arg0 = optSegments[segment][0][arg0]
                instr = "NewCircuit." + command + "(q[" + str(arg0) + "])"
                exec(instr)

            if(double):
                arg0 = QCircuit.data[i].arg[0][1]
                arg1 = QCircuit.data[i].arg[1][1]
                if(arg0 not in optSegments[segment][0].keys()) or (arg1 not in optSegments[segment][0].keys()):
                    assert Exception    #Something terrible happened.
                arg0 = optSegments[segment][0][arg0]
                arg1 = optSegments[segment][0][arg1] #TODO test this part, I never got to it
                instr = "NewCircuit." + command + "(q[" + str(arg0) + "], q[" + str(arg1) + "])"
                print(instr)
                exec(instr)
        print #NOW do all the swap gates.
        for swap in optSegments[segment][1]:
            print("swap(" + str(swap[0])+", "+str(swap[1])+")")
            helpers.swap(NewCircuit, q, swap[0], swap[1])

    return NewCircuit
    """
    #  ////////////////////////////////////////////////////////////////////
    # Cost Test

    #mapA = {2: 3, 4: 1, 5: 2}
    #mapB = {1: 2, 3: 4, 4: 1}
    #helpers.cost(mapA, mapB)

    # ////////////////////////////////////////////////////////////////////

    """
    mapA = {0: 2, 2: 3, 3: 4}
    InvA = {2: 0, 3: 2, 4: 3}
    mapB = {0: 0, 1: 5, 2: 4}
    InvB = {0: 0, 4: 2, 5: 1}
    """
    mapA = {0: 6, 1: 4, 2: 3, 3: 2}
    mapB = {0: 4, 1: 6, 3: 3, 4: 2}
    InvA = helpers.invertMap(mapA)
    InvB = helpers.invertMap(mapB)

    mapC = {0: 2, 2: 3, 3: 0}
    mapD = {0: 4, 1: 2, 3: 3}




    cost1, swaps, mapAprime, mapBprime = helpers.cost(mapA, mapB)

    cost2 = helpers.cost(mapC, mapD)
    #cost2 = helpers.cost(cost[1], mapC)
    print(cost1)
    print(cost2)

    return None

# Dynamically find the optimal permutation of global mappings for each segment
# such that the total cost of the circuit it minimized.
def bindSegments(segments):
    print("Remove angry error messages.")
    #OPT[i][j] = min( cost(segments[i].globals[j], segments[i-1].globals[k]]) , OPT[i-1][k] )
    #Here's the idea: Include each additional segment and re-optimize at each new addition.
    #Optimize over




