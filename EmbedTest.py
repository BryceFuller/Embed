"""
This File is used to test/debug Embed.py

"""
#////////////////////////////////////////////////////////////////////

import sys
from EMBED.Embed import Embed, EmbedHelper
if sys.version_info < (3, 5):
    raise Exception('Please use Python version 3.5 or greater.')

#////////////////////////////////////////////////////////////////////

# Importing QISKit
from qiskit import QuantumCircuit, QuantumProgram
import Qconfig

# Quantum program setup
Q_program = QuantumProgram()
# set the APIToken and API url
#Q_program.set_api(Qconfig.APItoken, Qconfig.config["url"])

#////////////////////////////////////////////////////////////////////
#Test 1

testCoupling1 = {0: (3,), 1: (0,3), 2: (1,), 3: (4,5), 4: (2,6), 5:(6,), 6: ()}
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
#Cost Test

testCoupling3 = {0: (1,), 1: (2,3), 2: (4,), 3: (4,), 4: (5,9), 5: (6,7,8), 6: (), 7: (), 8: (), 9: (10,), 10: (11,), 11: ()}
q3 = Q_program.create_quantum_register("q3", 11)
c3 = Q_program.create_classical_register("c3", 11)
embedtest3 = Q_program.create_circuit("QCircuit3", [q3], [c3])

embedtest3.cx(q3[1], q3[2])
embedtest3.cx(q3[3], q3[2])
embedtest3.cx(q3[2], q3[4])
embedtest3.cx(q3[2], q3[5])
embedtest3.cx(q3[5], q3[6])
embedtest3.cx(q3[6], q3[7])
embedtest3.cx(q3[7], q3[8])
embedtest3.cx(q3[7], q3[9])
embedtest3.cx(q3[7], q3[10])


mapA = {0: 2, 2: 3, 3: 4}
mapB = {0: 0, 1: 5, 2: 4}

#////////////////////////////////////////////////////////////////////

testCoupling4 = {0: (1,2,3,4,5,6,7), 1:(8,), 2:(9,), 3:(10,), 4:(11,), 5:(12,), 6:(13,), 7:(14,)}
q4 = Q_program.create_quantum_register("q4", 15)
c4 = Q_program.create_classical_register("c4", 15)
embedtest4 = Q_program.create_circuit("QCircuit4", [q4], [c4])

embedtest4.cx(q4[0],q4[1])
embedtest4.cx(q4[0],q4[2])
embedtest4.cx(q4[0],q4[3])
embedtest4.cx(q4[0],q4[4])
embedtest4.cx(q4[4],q4[5])
embedtest4.cx(q4[5],q4[6])
embedtest4.cx(q4[5],q4[7])
embedtest4.cx(q4[5],q4[8])
embedtest4.cx(q4[5],q4[9])
embedtest4.cx(q4[9],q4[10])
embedtest4.cx(q4[10],q4[11])
embedtest4.cx(q4[10],q4[12])
embedtest4.cx(q4[10],q4[13])

#result = Embed(embedtest4, testCoupling4)



#////////////////////////////////////////////////////////////////////

testCoupling5 = {0: (1,2,3,4), 1:(5,9), 2:(6,10), 3:(7,11), 4:(8,12)}
q5 = Q_program.create_quantum_register("q5", 15)
c5 = Q_program.create_classical_register("c5", 15)
embedtest5 = Q_program.create_circuit("QCircuit5", [q5], [c5])

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

result = Embed(embedtest5, testCoupling5)

print(result)



#result1 = Embed(embedtest1, testCoupling1)
#result2 = Embed(embedtest2, testCoupling2)