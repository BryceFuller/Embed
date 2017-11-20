from EMBED import EmbedHelper
from EMBED.EmbedHelper import Circuit


class EmbedAlgorithm(object):


    def GreedyAlgorithm(self, QCircuit, Coupling):

        numQubits = QCircuit.regs['q'].size
        instructions = EmbedHelper.reformatInstruction(QCircuit)
        global_map = Circuit.getValidMap(instructions[0], Coupling);
        result = Circuit(numQubits);

        #Build Intermediate representation of reformatted circuit
        result.addSegment(0, global_map);
        segmentIndex = 0;


        for i in range(1, len(instructions)):
            currentSegment = result.segments[segmentIndex]
            global_map = currentSegment.global_map
            ReMappedInstr = EmbedHelper.reMap(i, global_map)

            if(EmbedHelper.isValid(ReMappedInstr)):
                currentSegment.extend()
            else:
                local_map = Circuit.getValidMap(instructions[i], Coupling)
                result.addSegment(i,local_map)
                segmentIndex += 1
                print("newSegment")



        #Convert intermediate representation back into quantum circuit.
        #Return reconstructed circuit
        print("Algorithm")