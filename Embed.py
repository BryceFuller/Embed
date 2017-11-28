# Checself=Noneversion of PYTHON; we only support > 3.5
import sys

from EMBED import EmbedHelper, EmbedAlgorithm


if sys.version_info < (3, 5):
    raise Exception('Please use Python version 3.5 or greater.')

def Embed(QCircuit, coupling):
    helpers = EmbedHelper.EmbedHelper(QCircuit, coupling)
    segments = EmbedAlgorithm.Greedy(helpers)
    #TODO get local maps for segments, parse into swap gates

