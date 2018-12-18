# Embed

Embed is a quantum circuit placement algorithm.
Given a quantum circuit (currently given as a qiskit quantum circuit object), and a directed graph specifying the hardware topology, this algorithm relabeles indices and reformats the given quantum circuit to be embeddable into the given topology.

Entry point to the Algorithm is Embed.py,

EmbedAlgorithm.py contains high level implementations, currently the greedy approach is implemented.

EmbedHelper.py contains all subroutines related to reformatting and processing the quantum circuit.
This file is the majority of the codebase for this project. 



# Written by Bryce Fuller under the guidance of Doctoral Student Patrick Rall
# This original work is supported by Quantum Computing Initiative at UT Austin
# This work is made possible through collaboration with Dr. Scott Aaronson's Research group at UT Austin.
