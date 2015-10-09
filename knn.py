#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on Sun Jun  8 19:39:36 2014

@author: Guilherme Castro Diniz
guizao.seri@gmail.com
"""

import sys as arg
import numpy as np
import scipy.spatial.distance as distance
import time
import collections

def resultado(Classificacao):
	acerto = 0
		
	for ClassificReal,ClassificKnn in Classificacao:
		ClassificReal = int(ClassificReal)
		ClassificKnn = int(ClassificKnn)
		if ClassificReal == ClassificKnn:
			acerto = acerto + 1
	return acerto


def instancias(Arq):
	_linhas = np.loadtxt(Arq, dtype=float, delimiter=" ")
	_instancias = []
	for linha in _linhas:
		_instancias.append((linha[0], np.array(linha[1:])))
	return _instancias
 

def Knn(treino,teste,k,tipo):
    _Classific = []
    aux = 0.0
    
    for i,ii in teste:
        _distancias = []
        for j,jj in treino:
                dist = Distancia(ii,jj,tipo)
                if len(_distancias) == k:
                    if (dist,j) < _distancias[k-1]:
                        _distancias[k-1] = (dist,j)
                        q = 2
                        while (_distancias[k-q+1] < _distancias[k-q]):
                            aux = _distancias[k-q+1]
                            _distancias[k-q+1] = _distancias[k-q]
                            _distancias[k-q] = aux
                            q = q + 1
                            if q > k:
                                break
                else:
                    _distancias.append((dist,j))
                    _distancias.sort()
        _Classific.append((i,Classificar(_distancias)))
    return _Classific
   
    
def Distancia(i,j,tipo):
	if tipo == 1:
		return distance.euclidean(i,j)
	elif tipo == 2:
		return distance.cityblock(i,j)
	elif tipo == 3:
        	return distance.cosine(i,j)  
		
def Classificar(_dist):
	_classes = []
	for i,j in _dist:
		_classes.append(j)
	QtdClasses = collections.Counter(_classes) #Qtd de cada classe
	return QtdClasses.most_common()[0][0] #Moda

if __name__ == "__main__":
    if len(arg.argv) != 3:
        print("Argumentos: Treino Teste")
        exit(1)
    
    ArqTreino = open(arg.argv[1],'r')
    ArqTeste = open(arg.argv[2],'r')
    
    k = [1,3,5]
    
    treino = instancias(ArqTreino)
    teste = instancias(ArqTeste)
    
    ArqTreino.close()
    ArqTeste.close()
     
    for j in range(1,4):
        if j == 1:
            print "-- Euclidean --"
        elif j == 2:
            print "-- Manhattan --"
        elif j == 3:
            print "-- Cosine --"
        for i in range(len(k)):
            ini = time.clock()
            x = Knn(treino,teste,k[i],j)
            y = resultado(x)
            perc = y*100/len(x)
            
            print "K = ",k[i]
            print "Acertos = {0}%".format(perc)
            print "Tempo = ",time.clock()-ini
            print "\t"
        print "\n"        