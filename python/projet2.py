# -*- coding: utf-8 -*-
"""
Created on Wed May  4 15:59:42 2016

@author: Quentin
"""

from numpy.random import rand
import numpy as np
import scipy.sparse as sc
import random as rd
import matplotlib.pyplot as plt
import math



def create_matrix_f(f,N): #creation de la matrice a partir de f (f[k][l]=nombre de noeuds a k inputs l outputs)
#    N = 0         #Calcul de N nombre de noeuds
#    for k in range(len(f)): #k input
#        for l in range(len(f[k])): #l output
#            N+= f[k][l]
    
    list_input = []
    list_output = []
    list_node = [0 for k in range(N)]    
    f2 = np.copy(f)
    
    list_noeud = [k for k in range(N)] #On choisit f[k][l] noeuds parmi les noeuds restant
    for k in range(len(f2)):
        for l in range(len(f2[k])):
            while f2[k][l] > 0:
                r = rd.randint(0,len(list_noeud)-1)
                x = list_noeud.pop(r)
                list_node[x] = (k,l)
                list_input += k*[x] # Ces noeuds auront k inputs
                list_output += (l+1)*[x] #Ces noeuds auront l outputs
                f2[k][l] -=1
                                
                
 #   print(list_output,list_input)
    print(len(list_output),len(list_input))
            
    list_edge = []  #Creation de la liste des arcs
    precedent = -1
    for elt in list_input:
        if elt != precedent : #Permet de reinitialiser la liste des noeuds deja choisis
            chosen = [elt] #pour eviter la redondance des arcs, on memorise les arcs deja crees et cela evite les boucles aussi            
        l = len(list_output)-1
        r = rd.randint(0,l)
        while list_output[r] in chosen: #on rechoisit aleatoirement un arc si il a deja ete choisi precedemment
            r = rd.randint(0,l)
        a = list_output.pop(r) #on enleve l'output
        edge = (elt,a)    
        chosen.append(a)
        list_edge.append(edge)
            
    list_row = [ elt[0] for elt in list_edge ] #liste des lignes contenant les elements non nuls
    list_col = [ elt[1] for elt in list_edge ] #liste des colonnes contenant les elements non nuls
    
    A = sc.csr_matrix(([1]*len(list_edge),(list_row,list_col)), shape=(N,N)).toarray()
    
    return A
    
def f_entiere(f,N):
    
    f_non_entiere = []
    for i in range(len(f)):
        f_non_entiere.append(f[i]*N) #on multiplie la matrice de f par la distribution en input
        
    for i in range(len(f)): #on rend la matrice entière en arrondissant chaque élément de la matrice
        for j in range(len(f[0])):
            if f_non_entiere[i][j] - math.floor(f_non_entiere[i][j]) >= 0.5:
                f_non_entiere[i][j] = int(math.floor(f_non_entiere[i][j]) +1)
            else:
                f_non_entiere[i][j] = int(math.floor(f_non_entiere[i][j]))
                
    return f_non_entiere #on obtient une matrice à éléments entiers où l'élément k,l correspond au nombre de noeud à k input et l output
#on peut alors appliquer la fonction create_matrix_f à f_non_entiere
    
def histo_nb_output(A):
    N = len(A)
    nb_output = [] # on compte le nombre d'output de chaque noeud : le noeud i aura nb_output[i] output
    for k in range(N):
        s = 0
        for i in range(N):
            s+= A[i][k]
        nb_output.append(s)
    
    plt.hist(nb_output) # on construit l'histogramme donnant le nombre de noeud pour un nombre d'output donné
    plt.show()
        
    
    