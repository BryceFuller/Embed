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

        # greedily grow segement
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
        """
        # make sure segment only contain one global map
        prv_global_map = segments[-1].global_maps[0]
        # get best global map relative to previous global map
        #TODO implement cost()
        best_global_map = segment.global_maps[0]
        best_cost = helpers.localmap(prv_global_map, segment.global_maps[0])
        for i in range(1, len(segment.global_maps)):
            cost = helpers.localmap(prv_global_map, segment.global_maps[i])
            if cost < best_cost:
                best_global_map = segment.global_maps[i]

        segment.global_maps = [best_global_map]
        """
        segments.append(segment)



    #Convert intermediate representation back into quantum circuit.
    #Return reconstructed circuit
    print("Algorithm")
    return None


