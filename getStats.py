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
import json, os
import random, time

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

def doRun(todo):
    n,m,cn = todo

    # init circuit
    Q_program = QuantumProgram()
    qreg = Q_program.create_quantum_register("qreg", n)
    creg = Q_program.create_classical_register("creg", 1)
    embedtest = Q_program.create_circuit("QCircuit", [qreg], [creg])

    # generate random coupling

    connectfails = 0

    while True:
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
                return
        break

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
        print(str(len(data[key]["costs"])) + " of "+ str(runs) +" at: "+ str(time.asctime()))
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

        return (dt, cost, segnum)

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

        return (None, None, None)

#////////////////////////////////////////////////////////////////////
fname = "data.json"
if os.path.exists("data.json"):
    data = json.loads(open("data.json", "r").read())
else:
    data = {}

params = [(15,m,20,1) for m in range(30,38)]

todo  = []

#(n,m,cn,runs)
for param in params:
    n,m,cn,runs = param

    key = "%d_%d_%d" % (n,m,cn)
    if key not in data:
        data[key] = {
            "n":n,
            "m":m,
            "cx":cn,
            "costs":[],
            "times":[],
            "segs":[],
        }

    for i in range(runs - len(data[key]["costs"])):
        todo.append((n,m,cn))


print(todo)
# from multiprocessing import Pool
# p = Pool(8)
output = list(map(doRun ,todo))


for i in range(len(todo)):
    n,m,cn = todo[i]
    dt,cost,segnum = output[i]

    key = "%d_%d_%d" % (n,m,cn)
    data[key]["times"].append(dt)
    data[key]["costs"].append(cost)
    data[key]["segs"].append(segnum)

f = open(fname, "w+")
f.write(json.dumps(data))
f.close()
