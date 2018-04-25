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

    # K = 0
    optSegments1, cost1 = helpers.localSelect(segments)

    #K > 0
    optSegments2, cost2 = helpers.selectSegments(segments,1)
    NewCircuit1 = helpers.RebuildCircuit(optSegments1,segments)

    NewCircuit2 = helpers.RebuildCircuit(optSegments2,segments)
    return NewCircuit2, cost2


