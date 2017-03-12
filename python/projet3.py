# -*- coding: utf-8 -*-
"""
Created on Thu May 19 11:29:20 2016

@author: Quentin
"""
from numpy.random import rand
import numpy as np
import scipy.sparse as sc
import random as rd
import matplotlib.pyplot as plt
import math

N = 2000
p = 0.9
v = 0.5
init = 0.05

def f_test():
    f = np.zeros((20,20))
    f[10] = [1/20]*20
    return f

def first_step_2(N,f,i):
    I_0 = f*init  #i% de noeuds infectes initialement
    R_0 = np.zeros((N,N))
    return I_0,R_0
    
def binomial(k,n,p):
    return math.factorial(n)/(math.factorial(k)*math.factorial(n-k))*math.pow(p,k)*math.pow(1-p,n-k)

def f_erdos(k,l,p):
    f = np.zeros((k,l))
    for i in range(k):
        for j in range(l):
            f[i][j] = binomial(j,l-1,p)/k
        
    return f
    
def somme(M):
        k = len(M)
        l = len(M[0])
        s = 0
        for i in range(k):
            for j in range(l):
                s += j*M[i][j]
        
        return s

def equa_dif(f,I,R,p,v):
        I_1 = np.copy(I)
        R_1 = np.copy(R)
        k = len(f)
        l = len(f[0])
        
        for i in range(k):
            for j in range(l):
                I_1[i][j] = p*i*(f[i][j]-I[i][j]-R[i][j])*somme(I)/somme(f) - I[i][j]*v + I[i][j]
                R_1[i][j] = I[i][j]*v + R[i][j]
                
        return I_1,R_1

#def func1(y,i,j):
#        return p*i*(f[i][j]-I[i][j]-R[i][j])*somme(I)/somme(f) - I[i][j]*v



def graph2(f):    

    I,R = first_step_2(N,f,init)
    m = 1
    L = [np.sum(I)]
    while(np.sum(I)>0 and m < 100):  #condition d'arret:plus de noeuds infectes ou m=100
        m +=1
        print(m)
        I,R = equa_dif(f,I,R,p,v)
        L.append(np.sum(I))
        
    
    print(L)
    plt.plot(range(m),L)
    
