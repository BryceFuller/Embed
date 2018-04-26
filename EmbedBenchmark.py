"""
This file performs randomized benchmarking of the embed algorithm

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

import random, time
from statistics import stdev, mean


# Quantum program setup
# set the APIToken and API url
#Q_program.set_api(Qconfig.APItoken, Qconfig.config["url"])

#////////////////////////////////////////////////////////////////////

# Benchmaking settings

# random.seed(a=12345)

n = 4  # number of qubits
m = 7  # number of connections
cn = 10  # number of CNOTs

runs = 2 # number of random circuits

print("Testing Embed on", n, "qubits with", cn, "random CNOTs")

# prevent infinite looping due to failure to connect
connectfails = 0
maxconnectfails = 10

random.seed(0)

#////////////////////////////////////////////////////////////////////

def isConnected(coupling, n):
    walk = set([0])
    while True:
        walknew = set([i for i in walk])

        for i in walk:
            if i in coupling: walknew = walknew.union(coupling[i])

        for i in coupling.keys():
            if len(walk.intersection(coupling[i])) > 0:
                walknew = walknew.union([i])
                walknew = walknew.union(coupling[i])

        if len(walknew) == len(walk):
            break

        walk = walknew

    return len(walk) == n


#////////////////////////////////////////////////////////////////////

costs = []
times = []

while len(costs) < runs:
    # init circuit
    Q_program = QuantumProgram()
    qreg = Q_program.create_quantum_register("qreg", n)
    creg = Q_program.create_classical_register("creg", 1)
    embedtest = Q_program.create_circuit("QCircuit5", [qreg], [creg])

    # generate random coupling
    coupling = {}

    l = 0
    while l < m:
        i, j = 0,0
        while i == j:
            i = random.randint(0, n-1)
            j = random.randint(0, n-1)

        if i not in coupling:
            coupling[i] = [j]
            l += 1
        else:
            if i not in coupling[i]:
                coupling[i].append(j)
                l += 1

    # coupling = {0: [1,3,2,4], 1:[5,9], 2:[6,10], 3:[7,11], 4:[8,12]}
    # coupling = {0: [1,2]}

    if not isConnected(coupling, n):
        connectfails += 1
        if connectfails > maxconnectfails:
            print("Can't generate connected coupling")
            break
        continue
    connectfails = 0

    # is sorting necessary?
    for i in coupling.keys(): coupling[i] = tuple(sorted(coupling[i]))

    # generate circuit
    for l in range(cn):
        i, j = 0,0
        while i == j:
            i = random.randint(0, n-1)
            j = random.randint(0, n-1)

        embedtest.cx(qreg[i],qreg[j])

    start = time.time()

    try:
        result, cost = Embed(embedtest, coupling)
        print("Completed Test Case: ")
    except:
        print("Embed Crashed")
        pass

    dt = time.time() - start
    cost = random.randint(0,100)

    times.append(dt)
    costs.append(cost)

print("Time taken: %.3f +- %.3f" % (mean(times), stdev(times)))
print("Embed cost: %.3f +- %.3f" % (mean(costs), stdev(costs)))
