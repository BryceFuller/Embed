# Checself=Noneversion of PYTHON; we only support > 3.5
import sys
import re

from EMBED import EmbedHelper, EmbedAlgorithm
from qiskit import QuantumCircuit, QuantumProgram
import Qconfig


if sys.version_info < (3, 5):
    raise Exception('Please use Python version 3.5 or greater.')

def Embed(QCircuit, coupling):
    circuit = object;

