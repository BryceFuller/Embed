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

    #Convert intermediate representation back into quantum circuit.
    #Return reconstructed circuit
    print("Algorithm")
    return None

# Dynamically find the optimal permutation of global mappings for each segment
# such that the total cost of the circuit it minimized.
def bindSegments(segments):
    print("Remove angry error messages.")
    #OPT[i][j] = min( cost(segments[i].globals[j], segments[i-1].globals[k]]) , OPT[i-1][k] )
    #Here's the idea: Include each additional segment and re-optimize at each new addition.
    #Optimize over




