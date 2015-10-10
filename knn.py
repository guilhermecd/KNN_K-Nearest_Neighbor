"""    
    Copyright (C) 2014, Guilherme Castro Diniz.
    
    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation (FSF); in version 2 of the
    license.

    This program is distributed in the hope that it can be useful,
    but WITHOUT ANY IMPLIED WARRANTY OF ADEQUATION TO ANY
    MARKET OR APPLICATION IN PARTICULAR. See the
    GNU General Public License for more details.
    <http://www.gnu.org/licenses/>
"""
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys as arg
import sys
import numpy as np
import scipy.spatial.distance as distance
import time
import collections

def result(classification):
	hits = 0
		
	for ClassificReal,ClassificKnn in classification:
		ClassificReal = int(ClassificReal)
		ClassificKnn = int(ClassificKnn)
		if ClassificReal == ClassificKnn:
			hits = hits + 1
	return hits

def ReadArq(Arq):
	_lines = np.loadtxt(Arq, dtype=float, delimiter=" ")
	_instance = []
	for line in _lines:
		_instance.append((line[0], np.array(line[1:])))
	return _instance
 
		
def classifier(_dist):
	_class = []
	for i,j in _dist:
		_class.append(j)
	QtdClasses = collections.Counter(_class) #Qtd de cada classe
	return QtdClasses.most_common()[0][0] #Moda

def Distance(i,j,type):
	if type == 1:
		return distance.euclidean(i,j)
	elif type == 2:
		return distance.cityblock(i,j)
	elif type == 3:
        	return distance.cosine(i,j)  
def Knn(training,test,k,type):
    _Classific = []
    aux = 0.0
    
    for i,ii in test:
        _distance = []
        for j,jj in training:
                dist = Distance(ii,jj,type)
                if len(_distance) == k:
                    if (dist,j) < _distance[k-1]:
                        _distance[k-1] = (dist,j)
                        q = 2
                        while (_distance[k-q+1] < _distance[k-q]):
                            aux = _distance[k-q+1]
                            _distance[k-q+1] = _distance[k-q]
                            _distance[k-q] = aux
                            q = q + 1
                            if q > k:
                                break
                else:
                    _distance.append((dist,j))
                    _distance.sort()
        _Classific.append((i,classifier(_distance)))
    return _Classific

if __name__ == "__main__":
    if len(arg.argv) != 3:
        print("You need 2 inputs arguments: FileTraining and FileTest")
        exit(1)
    
    FileTraining = open(arg.argv[1],'r')
    FileTest = open(arg.argv[2],'r')
    
    k = [3]
    
    training = ReadArq(FileTraining)
    test = ReadArq(FileTest)
    
    FileTraining.close()
    FileTest.close()
     
    for j in range(1,2):
        if j == 1:
            print ("*** Distance Euclidian ***")
        elif j == 2:
            print ("*** Distance Cityblock ***")
        elif j == 3:
            print ("*** Distance Cosine ***")
        for i in range(len(k)):
            ini = time.clock()
            x = Knn(training,test,k[i],j)
            print (x)
            sys.exit()
            y = result(x)
            perc = y*100/len(x)
            
            print ("K = ",k[i])
            print ("Hits = {0}%".format(perc))
            #print "Tempo = ",time.clock()-ini
            print ("\t")
        print ("\n")        


