# Checself=Noneversion of PYTHON; we only support > 3.5
import sys

from EmbedHelper import EmbedHelper
from EmbedAlgorithm import Greedy


if sys.version_info < (3, 5):
    raise Exception('Please use Python version 3.5 or greater.')

def Embed(QCircuit, coupling, f=None, k=None):


    helpers = EmbedHelper(QCircuit, coupling)
    segments = Greedy(helpers)


    if len(segments) == 1:
        NewCircuit3 = helpers.RebuildCircuit([[segments[0].global_maps[0]]],segments)
        print("ONE SEG")
        return NewCircuit3, 0, 1

    # K = 0
    optSegments1, cost0 = helpers.localSelect(segments)
    NewCircuit1 = helpers.RebuildCircuit(optSegments1, segments)

    print("cost1 = " +  ", "+str(cost0))
    return NewCircuit1, cost0, len(segments)


