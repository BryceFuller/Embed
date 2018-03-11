import copy

from EMBED import EmbedHelper


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


    #Select a map for each segment (greedily)
    print(segments)
    segopt = helpers.selectSegments(segments, 1)# ////////////////////////////////////////////////////////////////////
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




