#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 11:25:21 2018

@authors: LE GALLO Benjamin - PELLIET Steven
"""

import numpy as np
np.set_printoptions (threshold=np.nan)
from random import shuffle
from random import randint
import copy


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
    m = n*m
    #Create matrix (n*m) with ones
    P = np.ones((n, m), dtype=np.int)
    
    l = []
    for i in range(2, n+1):
        #Create a list of cities
        l.append(i)
    for i in range(0, m):
        #Shuffle cities and append in matrix
        l2 = l[:]
        shuffle(l2)
        #Copy list as an independant list
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
@param D: matrix with distances for each83 city
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
Subfunction: To give the highest solution
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
Take random solutions and give best selection of these solutions
@param D: matrix with distances for each city
@param P: matrix which represent base population

@return P: best of half of base population
""" 
def selectRoulette(D, P):
    #Take dimension of cities matrix
    (n,p) = np.shape(D)
    #The midle of base population matrix
    halfPop = int(p/2)
    
    #Foreach solution in two half: choose random solution 
    for i in range(0, halfPop):
        (n,p) = np.shape(P)
        #Random selection
        sol = randint(0, p-1)
        sol2 = randint(0, p-1)
        #If sma esolution then choose another random solution
        while(sol2 == sol):
            sol2 = randint(0, p-1)
            #Calcul best distance
        if(calculAdapt(D, P[:, sol]) > calculAdapt(D, P[:, sol2])):
            #Delete the worst solution
            P = np.delete(P, sol, axis=1)
        else:
            P = np.delete(P, sol2, axis=1)
    return P
    
    """
Take a solution and give a new solution with a permutation between 2 cities
@param P: matrix which represent a population

@return P: best of half of base population
""" 
def mutate(P):
    print (P)
    (n,p) = np.shape(P)
    
    #Get index
    i = randint(2,n)
    j = randint(2,n)
    
    
    #Choose random solutions to mutation 
    indexSol = randint(1,n)
    tempI=P[indexSol-1,i-1]
    tempJ=P[indexSol-1,j-1]
    print ("Mutate on i:",tempI,"and j:",tempJ)
    print ("line :",indexSol)
    P[indexSol-1,i-1]=tempJ
    P[indexSol-1,j-1]=tempI
    return P
"""
Crossover two parents and return two children
@param sol: first solution (individual)
@param sol2: second solution (individual)

@return children: couple of two children (crossover of parents)
""" 
def crossover(sol, sol2):
    #Take dimensions of solution matrices
    p = len(sol)
    
    #Choose random i and j
    i = randint(1, p-1) #Beginning of crossing (start after city '1')
    j = randint(1, p-i) #Crossover width

    #Create two temporary children
    child = copy.copy(sol) #Copy solution 1 in child 1
    child2 = copy.copy(sol2) #Copy solution 2 in child 2

    #Change specific cities to begin i of width j
    for iterator in range(0, j):
        #Replace cities of second solution in first temporary child
        child[i+iterator] = sol2[i+iterator]        
        #Replace cities of first solution in second temporary child
        child2[i+iterator] = sol[i+iterator]
        
    #Search numbers missing bewteen parent of his child
    cityDifference = list(set(sol) - set(child))
    indexDifference = 0
    
    cityDifference2 = list(set(sol2) - set(child2))
    indexDifference2 = 0
    #Foreach number in array (check if number not exist several time)
    for iterator in range(1, p):
        for subiterator in range(iterator+1, p):
            #CHILD 1: Check if city already exist
            if(child[iterator] == child[subiterator]):
                #Replace city already exist by a city which don't exist
                child[subiterator] = cityDifference[indexDifference]
                #Increment index difference
                indexDifference+= 1
                
            #CHILD 2: Check if city already exist
            if(child2[iterator] == child2[subiterator]):
                #Replace city already exist by a city which don't exist
                child2[subiterator] = cityDifference2[indexDifference2]
                #Increment index difference
                indexDifference2+= 1
    
    #Create couple of child
    children = ([child, child2])
    return children
                

"""
Principal function which resolve salesman travel issue dynamically !
"""
def main():
    try:
        nbCity=int(input("Write the number of cities to travel\n> "))
        nbSol=int(input("Write the number of solutions you want\n> "))
        
        Map = carto(nbCity)
        #print("the travel map", Map)
        
        BasePop = populat(nbCity, nbSol)
        print("Population:", populat(nbCity, nbSol))
        Sol = BasePop
        Sol = Sol[:, 1]
        #print("The basic population", Sol)
        
        halfPop = selectElit(Map, BasePop)
        #halfPop = selectRoulette(Map, BasePop)
        print("Selected population:", halfPop)
        
        Mutation=mutate(halfPop)
        print("mutation Select population:",Mutation)
        
        dist = calculAdapt(Map, Sol)
        print("Distance traveled:", dist,"kms")          
       
        
        
        
        #TEST
        individu = halfPop[:, 1]
        individu2 = halfPop[:, 5]
        print(individu)
        print(individu2)
        crossover(individu, individu2)
        #END TEST
    except Exception as e:
        print("This isn't a figure, try again") 
        print('Failed to upload to ftp: '+ str(e))

    return exit

"""
Execute Main
"""
main()