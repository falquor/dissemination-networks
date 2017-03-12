# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 14:03:03 2016

@author: Quentin
"""

from numpy.random import rand
import numpy as np
import scipy.sparse as sc
import random as rd
import matplotlib.pyplot as plt

N = 2000
k = 10
p = 1
v = 0.5
i = 0.05

def create_matrix(k,N):
    list_input = []
    
    for i in range(N): #creation de la liste des arcs entrant 
        l = k*[i]
        list_input+=l
    
    list_output = []
    
    for i in range(N): #creation de la liste des arcs sortant
        k2 = rd.randint(1,2*k)
        l = k2*[i]
        list_output += l
    
    list_edge = []
    print(len(list_output),len(list_input))
    for n in range(N):
        chosen = [list_input[n*k]] #pour eviter la redondance des arcs,
        #on memorise les arcs deja crees et cela evite les boucles aussi
        for i in range(k):
            l = len(list_output)-1
            r = rd.randint(0,l)
            while list_output[r] in chosen: #on rechoisit aleatoirement un arc si il a deja ete choisi precedemment
                r = rd.randint(0,l)
            a = list_output.pop(r) #on enleve l'output
            edge = (list_input[n*k+i],a)    
            chosen.append(a)
            list_edge.append(edge)
        
    
    list_row = [ elt[0] for elt in list_edge ] #liste des lignes contenant les elements non nuls
    list_col = [ elt[1] for elt in list_edge ] #liste des colonnes contenant les elements non nuls
    
    A = sc.csr_matrix(([1]*len(list_edge),(list_row,list_col)), shape=(N,N)).toarray()
    
    return A
    
    
def next_step(S,I,R,A,p,v): #p = proba d'infection et v = proba de soin
    V = I*(rand(N)>=(1-p)) #noeud infectant à l'étape n+1
    I_1 = np.dot(V,A) #noeud infectable
    for elt in range(N):
        if I_1[0,elt] !=0:
            I_1[0,elt] = 1
    I_1 = I_1*S #noeud infecté
    
    nR = I*(rand(N)>=(1-v)) #noeud nouvellement soigné
    R_1 = R + nR #noeud soigné à l'étape n+1
    
    I_1 = I_1 + I - nR #noeud infecté à l'étape n+1
    
    S_1 = np.ones((1,N)) - I_1 - R_1 #noeud susceptible à l'étape n+1
    
    return S_1,I_1,R_1
    
def first_step(A,i): #i = proba initiale d'infection
    I_0 = np.ones((1,N))*(rand(N)>=(1-i))  #i% de noeudsinfectes initialement
    S_0 = np.ones((1,N)) - I_0
    R_0 = np.zeros((1,N))
    
    return S_0,I_0,R_0
    
def count(I,N):  #compte la fraction de noeuds infectes
    n = np.sum(I)
    return n/N

def graph(A):    
#    A = create_matrix(k,N)
    S,I,R = first_step(A,i)
    L = []
    L.append(count(I,N))
    m = 1
    while(np.sum(I)>0 and m < 100):  #condition d'arret:plus de noeuds infectes ou m=100
        m +=1
        print(m)
        S,I,R = next_step(S,I,R,A,p,v)
        L.append(count(I,N))
        
        
    plt.plot(range(m),L)

