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
Q_program = QuantumProgram()
testcoupling5 = {0: (1,2,3,4), 1:(5,9), 2:(6,10), 3:(7,11), 4:(8,12)}
q5 = Q_program.create_quantum_register("q5", 15)
c5 = Q_program.create_classical_register("c5", 15)
embedtest5 = Q_program.create_circuit("qcircuit5", [q5], [c5])

embedtest5.cx(q5[0],q5[1])
embedtest5.cx(q5[0],q5[2])
embedtest5.h(q5[0])
embedtest5.cx(q5[0],q5[3])
embedtest5.cx(q5[0],q5[5])
embedtest5.cx(q5[5],q5[6])
embedtest5.cx(q5[5],q5[7])
embedtest5.cx(q5[5],q5[8])
embedtest5.cx(q5[5],q5[10])
embedtest5.cx(q5[10],q5[11])
embedtest5.cx(q5[10],q5[12])
embedtest5.cx(q5[10],q5[13])

result, cost = Embed(embedtest5, testcoupling5)


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
