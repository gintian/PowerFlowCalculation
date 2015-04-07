﻿# -*- coding: UTF-8 -*-

# Name:         PowerFlowCalculation.py
# Func:         To calc the power flow of elecrtcal grid using Newton-Raphson method, this is the main file of this project
# Author:       Maples7
# Addr:         EE of SDU
# Time:         2015-04-07 
# Link:         http://www.cnblogs.com/maples7/

import globalVariable as gv
import numpy as np
from math import *

def read_data():
    """
    Read Data from input.txt, the global variables are in the globalVariable.py
    """
    try:
        fp = open("input.txt", "r+")

        firstLine = fp.readline().split(" ")
        gv.num_node = int(firstLine[0])
        gv.num_line = int(firstLine[1])
        gv.num_tran = int(firstLine[2])
        gv.num_gene = int(firstLine[3])
        gv.num_load = int(firstLine[4])
        gv.error = float(firstLine[5])

        for i in range(gv.num_line):
            nLine = fp.readline().split(" ")
            temp = gv.Line(int(nLine[0]), int(nLine[1]), float(nLine[2]), float(nLine[3]), float(nLine[4]))
            gv.line.append(temp)

        nLine = fp.readline()
        for i in range(gv.num_tran):
            nLine = fp.readline().split(" ")
            temp = gv.Tran(int(nLine[0]), int(nLine[1]), float(nLine[2]), float(nLine[3]), float(nLine[4]))
            gv.tran.append(temp)

        nLine = fp.readline()
        for i in range(gv.num_gene):
            nLine = fp.readline().split(" ")
            temp = gv.Gene(int(nLine[0]), int(nLine[1]), float(nLine[2]), float(nLine[3]), float(nLine[4]))
            gv.gene.append(temp)

        nLine = fp.readline()
        for i in range(gv.num_load):
            nLine = fp.readline().split(" ")
            temp = gv.Load(int(nLine[0]), float(nLine[1]), float(nLine[2]))
            gv.load.append(temp)

        fp.close()
    except:
        print "Error: Can't input Data into input.txt. (function read_data() error)"
        exit()

def admt_matrix():
    """
    Create admittance matrix
    """
    global Y
    Y = np.zeros_like((gv.num_node+1, gv.num_load+1), dtype = complex)
    for lineNum in range(gv.num_line):
        i = gv.line[lineNum].i
        j = gv.line[lineNum].j
        r = gv.line[lineNum].a
        x = gv.line[lineNum].b
        comp = 1/complex(r, x)
        if i==j:
            Y[i][i] += comp
        else:
            c = gv.line[lineNum].c
            Y[i][j] -= comp
            Y[j][i] = Y[i][j]
            Y[i][i] += (comp + complex(0, c))
            Y[j][j] += (comp + complex(0, c))
    for tranNum in range(gv.num_tran):
        i = gv.tran[tranNum].i
        j = gv.tran[tranNum].j
        r = gv.tran[tranNum].a
        x = gv.tran[tranNum].b
        c = gv.tran[tranNum].c
        comp = 1/complex(r, x)
        Y[i][i] += comp
        Y[i][j] -= comp/c
        Y[j][i] = Y[i][j]
        Y[j][j] += comp/c/c

def Um_and_Ua():
    """
    Set the amplitude and phase angle of voltage
    """
    global Um
    global Ua
    Um = np.ones(gv.num_node+1)
    Ua = np.zeros_like(gv.num_node+1)
    for i in range(1, gv.num_gene+1):
        if gv.gene[i].j <= 0:
            Um[gv.gene[i].i] = gv.gene[i].c

def form_Jacobian():
    """
    Form Jacobian Matrix & Calc the Power error
    """
    global Um
    global Ua
    global Y
    nu = 2*gv.num_node+1
    n2 = 2*gv.num_node
    for i in range(1, gv.num_node+1):
        vi = Um[i]
        di = Ua[i]
        dp = 0.0
        dq = 0.0
        for j in range(1, gv.num_node+1):
            if j != i:                  # when i <> j
                g = Y[i][j].real        # G        
                b = Y[i][j].imag        # B
                vj = Um[j]
                dj = Ua[j]
                dij = di - dj           # diff of Phase Angle
                Hij = -Um[i] * Um[j] * (g*sin(dij) - b*cos(dij))
                Lij = Hij
                Jacob[i][j] = Hij
                Jacob[i+gv.num_node][j+gv.num_node] = Lij
                Nij = -Um[i]*Um[j]*(g*cos(dij)+b*sin(dij))
                Mij = -Nij
                Jacob[i][j+gv.num_load]=Nij
                Jacob[i+gv.num_load][j] = Mij
                p = 

# main 
read_data()
admt_matrix()
Um_and_Ua()

Jocob = np.zeros_like((2*gv.num_node, 2*gv.num_load+1))
P = np.zeros_like(gv.num_node+1)
Q = np.zeros_like(gv.num_node+1)

while True:
    form_Jacobian();
