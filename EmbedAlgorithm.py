from EMBED import EmbedHelper
from EMBED.EmbedHelper import Circuit


class EmbedAlgorithm(object):


    def Greedy(self, helpers):
        QCircuit = helpers.QCircuit
        Coupling = helpers.Coupling

        numQubits = QCircuit.regs['q'].size
        instructions = helpers.Instructions
        segments = helpers.segments

        #Instantiate first segment object


        for start in range(1, len(instructions)):



            # greedily grow segement
            segment = result.getSegment(start, end)

            while len(segment.global_maps) > 0:
                end = end + 1
                segment = helpers.getSegment(start, end, segment)

            start = segment.end + 1

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

            segments.append(segment)



        #Convert intermediate representation back into quantum circuit.
        #Return reconstructed circuit
        print("Algorithm")