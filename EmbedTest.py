"""
This File is used to test/debug Embed.py

"""
#////////////////////////////////////////////////////////////////////

import sys
from EMBED.Embed import Embed
if sys.version_info < (3, 5):
    raise Exception('Please use Python version 3.5 or greater.')

#////////////////////////////////////////////////////////////////////

# Importing QISKit
from qiskit import QuantumCircuit, QuantumProgram
import Qconfig

# Quantum program setup
Q_program = QuantumProgram()
# set the APIToken and API url
Q_program.set_api(Qconfig.APItoken, Qconfig.config["url"])

#////////////////////////////////////////////////////////////////////
#Test 1

testCoupling1 = {0: (3,), 1: (0,3), 2: (1,), 3: (4,5), 4: (2,6), 5:(6,)}
q1 = Q_program.create_quantum_register("qubits", 11)
c1 = Q_program.create_classical_register("bits", 11)
embedtest1 = Q_program.create_circuit("QCircuit1", [q1], [c1])

embedtest1.cx(q1[0], q1[1])
embedtest1.cx(q1[1], q1[2])
embedtest1.cx(q1[1], q1[3])
embedtest1.cx(q1[3], q1[4])
embedtest1.cx(q1[3], q1[5])

embedtest1.cx(q1[4], q1[6])
embedtest1.cx(q1[4], q1[7])
embedtest1.cx(q1[6], q1[9])
embedtest1.cx(q1[6], q1[10])
embedtest1.cx(q1[7], q1[8])

#////////////////////////////////////////////////////////////////////
#Test 1

testCoupling2 = {0: (1,2,3,4,5)}

q2 = Q_program.create_quantum_register("q2", 6)
c2 = Q_program.create_classical_register("c2", 6)

embedtest2 = Q_program.create_circuit("QCircuit2", [q2], [c2])

embedtest2.cx(q2[0], q2[1])
embedtest2.cx(q2[1], q2[2])
embedtest2.cx(q2[2], q2[3])
embedtest2.cx(q2[3], q2[4])
embedtest2.cx(q2[4], q2[5])

#////////////////////////////////////////////////////////////////////





result1 = Embed(embedtest1, testCoupling1)
result2 = Embed(embedtest2, testCoupling2)