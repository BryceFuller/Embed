"""
This File is used to test/debug Embed.py

"""
#////////////////////////////////////////////////////////////////////

import sys
from Embed import Embed
from EmbedHelper import EmbedHelper
if sys.version_info < (3, 5):
    raise Exception('Please use Python version 3.5 or greater.')

#////////////////////////////////////////////////////////////////////

# Importing QISKit
from qiskit import QuantumCircuit, QuantumProgram
import Qconfig

# Quantum program setup
#Q_program.set_api(Qconfig.APItoken, Qconfig.config["url"])

#////////////////////////////////////////////////////////////////////

if True:
    Q_program = QuantumProgram()
    qreg = Q_program.create_quantum_register('qreg', 10)
    creg = Q_program.create_classical_register('creg', 1)
    embedtest = Q_program.create_circuit('QCircuit', [qreg], [creg])
    coupling = {9: (2,), 8: (5, 7), 2: (4,), 5: (0, 8), 6: (1, 2), 3: (6,), 0: (1, 3), 1: (2, 4, 7)}
    embedtest.cx(qreg[1],qreg[6])
    embedtest.cx(qreg[9],qreg[3])
    embedtest.cx(qreg[7],qreg[5])
    embedtest.cx(qreg[5],qreg[7])
    embedtest.cx(qreg[1],qreg[3])
    embedtest.cx(qreg[6],qreg[9])
    embedtest.cx(qreg[2],qreg[7])
    embedtest.cx(qreg[2],qreg[0])
    embedtest.cx(qreg[3],qreg[6])
    embedtest.cx(qreg[9],qreg[4])

result, cost = Embed(embedtest, coupling)

print(result, cost)
