from EMBED import EmbedHelper


def Greedy(helpers):
    QCircuit = helpers.QCircuit
    Coupling = helpers.Coupling

    qreg_name = list(QCircuit.get_qregs())[0]
    numQubits = QCircuit.regs[qreg_name].size

    instructions = helpers.Instructions
    segments = helpers.Segments


    for start in range(0, len(instructions)):
        end = start
        # greedily grow segement
        segment = helpers.getSegment(start, end)

        while len(segment.global_maps) > 0:
            end = end + 1
            segment = helpers.getSegment(start, end, segment)

        start = segment.end + 1
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


