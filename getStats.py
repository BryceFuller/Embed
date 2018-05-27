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
import json
import random, time

runs = 30 # number of random circuits

# prevent infinite looping due to failure to connect
connectfails = 0
maxconnectfails = 10

seed = 2
random.seed(seed)

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

params = [(15,m,20) for m in range(30,70,2)]

data = []

#(n,m,cn)
for param in params:

    f = open("stats/15_30-70_20.json", "w+")
    n = param[0]
    m = param[1]
    cn = param[2]

    costs = []
    times = []
    segs = []
    print("Testing Embed on", n, "qubits with", cn, "random CNOTs")
    while len(costs) < runs:

        # init circuit
        Q_program = QuantumProgram()
        qreg = Q_program.create_quantum_register("qreg", n)
        creg = Q_program.create_classical_register("creg", 1)
        embedtest = Q_program.create_circuit("QCircuit", [qreg], [creg])

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
                if j not in coupling[i]:
                    coupling[i].append(j)
                    l += 1

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
        circtext = []
        for l in range(cn):
            i, j = 0,0
            while i == j:
                i = random.randint(0, n-1)
                j = random.randint(0, n-1)

            embedtest.cx(qreg[i],qreg[j])
            circtext.append("embedtest.cx(qreg["+str(i)+"],qreg["+str(j)+"])")

        start = time.time()

        try:
            print(str(len(costs)) + " of "+ str(runs) +" at: "+ str(time.asctime()))
            result, cost, segnum = Embed(embedtest, coupling)
            print("cost = " +  str(cost))
            dt = time.time() - start

            embedValid = True
            for gate in result.data:
                if gate.name not in ["cx", "CX"]: continue
                ctl = gate.arg[0][1]
                trg = gate.arg[1][1]
                if ctl not in coupling or trg not in coupling[ctl]:
                    print("Disallowed CNOT:", ctl, "->", trg)
                    embedValid = False
            if not embedValid: raise Exception("Embedding uses disallowed CNOT")


            #ADD code here to open stats file, read in data structure, and store data.

            times.append(dt)
            costs.append(cost)
            segs.append(segnum)



        except Exception as e:
            print("\nEmbed crashed. Test case:")
            print("Q_program = QuantumProgram()")
            print("qreg = Q_program.create_quantum_register('qreg',", n ,")")
            print("creg = Q_program.create_classical_register('creg', 1)")
            print("embedtest = Q_program.create_circuit('QCircuit', [qreg], [creg])")
            print("coupling =", coupling)
            for c in circtext: print(c)

            print("\nException:")
            raise e

    data.append({
        "n":n,
        "m":m,
        "cx":cn,
        "costs":costs,
        "times":times,
        "segs":segs,
    })



f = open("stats/15_30-70_20.json", "w+")
f.write(json.dumps(data))
f.close()
