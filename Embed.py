# Checself=Noneversion of PYTHON; we only support > 3.5
import sys

from EmbedHelper import EmbedHelper
from EmbedAlgorithm import Greedy


if sys.version_info < (3, 5):
    raise Exception('Please use Python version 3.5 or greater.')
#ALL QUBITS MUST HAVE A DICTIONARY ENTRY IN COUPLING,
# IF A QUBIT HAS ONLY INCOMING EDGES, IT SHOULD POINT TO AN EMPTY TUPLE
#TODO: write code to reformat any coupling to satisfy this property.
def Embed(QCircuit, coupling):
    helpers = EmbedHelper(QCircuit, coupling)
    segments = Greedy(helpers)

    #Testing stuff!

    swaps1 = [(4, 0), (9, 1), (5, 1), (1, 0), (0, 2), (1, 0), (5, 1)]
    swaps2 = [(0,1),(0,2),(0,1),(0,1),(0,3),(0,2),(0,3)]
    #sw = helpers.distillSwaps(swaps2)

    #End of Testing Stuff


    if len(segments) == 1:
        NewCircuit3 = helpers.RebuildCircuit([[segments[0].global_maps[0]]],segments)
        return NewCircuit3, 0

    # K = 0
    optSegments1, cost1 = helpers.localSelect(segments)
    NewCircuit1 = helpers.RebuildCircuit(optSegments1, segments)

    #K > 0
    optSegments2, cost2 = helpers.selectSegments(segments,1)
    NewCircuit2 = helpers.RebuildCircuit(optSegments2,segments)

    print()
    return NewCircuit2, cost2


