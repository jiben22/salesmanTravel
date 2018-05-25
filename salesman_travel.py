#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 11:25:21 2018

@authors: LE GALLO Benjamin - PELLIET Steven
"""

import numpy as np
from random import shuffle
from random import randint


"""
Create a map
@param n: number of cities to travel

@return D: matrix represent distance bewteen cities  
"""
def carto(n):
    #Create matrix (n*n) with zeros
    D = np.zeros((n, n), dtype=np.int) #dtype -> size in memory
    #Complete matrix with random int
    for i in range(1, n):
        for j in range(0, i):
            D[i,j] = randint(0,100)
            D[j,i] = D[i,j]
    return D

"""
Create solutions
@param n: number of cities to travel
@param m: number of solutions (individual)

@return P: matrix represent base population
""" 
def populat(n, m):
    m = 2*m
    #Create matrix (n*m) with ones
    P = np.ones((n, m), dtype=np.int)
    l = []
    for i in range(2, n+1):
        #Create a list of cities
        l.append(i)
    for i in range(0, m):
        #Shuffle cities and append in matrix
        l2 = l[:] #Copy list as an independant list
        shuffle(l2)
        for j in range(1, n):
            P[j,i] = l2[j-1]
    return P

"""
Give total distance traveled
@param D: matrix with distances for each city
@param sol: solution (individual)

@return: total distance traveled
""" 
def calculAdapt(D, sol):
    n = len(sol) #Get number of cities
    dist = 0
    for i in range(0, n-1):
        #Make sum of distance bewteen each city of travel
        dist += D[sol[i]-1, sol[i]-1] #-1 because of start at 1 !
    return dist + D[0, sol[n-1]-1] #Add distance between first and last city


"""
Give best selection of the half solutions
@param D: matrix with distances for each city
@param P: matrix which represent base population

@return: best of half of base population
""" 
def selectElit(D, P):
    #Get size of matrices
    (n,p) = np.shape(D) 
    (q,r) = np.shape(P) #r: number of solutions
    
    #Create matrix n * r/2 with zeros
    halfPop = np.zeros((n, int(r/2) ))
    dist = []
    
    for i in range(0, r):
        #Create array 2D which contains solution index and his distance
        dist.append([])

    for i  in range(0, r):
        dist[i].append(i)
        dist[i].append(calculAdapt(D, P[:,i]))
    for i in range(0, int(r/2) ):
        #Removing half of the solutions (longer)
        (maxim, iMax) = maxi(dist)
        del dist[iMax]
    for i in range(0, int(r/2) ):
        #ajout des solutions dans la matrice
        halfPop[:,i] = P[:,dist[i][0]]
    
    return halfPop

"""
Give the highest solution
"""
def maxi(l):
    maxim = l[0][1]
    iMax = 0
    for i in range(1, len(l)):
        if(maxim<l[i][1]):
            maxim = l[i][1]
            iMax = i
    return maxim, iMax

"""
TEST
"""

try:
    nbCity=int(raw_input("write the number of cities to travel :"))
    nbSol=int(raw_input("write the number of solutions you want :"))
except:
    print("This isn't a figure, try again")

Map = carto(nbCity)
print("the travel map", Map)

BasePop = populat(nbCity, nbSol)
Sol = BasePop
Sol = Sol[:, 1]
print("The basic population", Sol)

halfPop = selectElit(Map, BasePop)
print("Selected population:", halfPop)

dist = calculAdapt(Map, Sol)
print("Distance traveled:", dist,"kms")    


"""
END TEST
"""