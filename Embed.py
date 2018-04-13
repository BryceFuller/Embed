# Checself=Noneversion of PYTHON; we only support > 3.5
import sys

from EMBED import EmbedHelper, EmbedAlgorithm


if sys.version_info < (3, 5):
    raise Exception('Please use Python version 3.5 or greater.')
#ALL QUBITS MUST HAVE A DICTIONARY ENTRY IN COUPLING,
# IF A QUBIT HAS ONLY INCOMING EDGES, IT SHOULD POINT TO AN EMPTY TUPLE
#TODO: write code to reformat any coupling to satisfy this property.
def Embed(QCircuit, coupling):
    helpers = EmbedHelper.EmbedHelper(QCircuit, coupling)
    segments = EmbedAlgorithm.Greedy(helpers)
    optSegments = helpers.localSelect(segments)
    NewCircuit = helpers.RebuildCircuit(optSegments,segments)
    return NewCircuit


