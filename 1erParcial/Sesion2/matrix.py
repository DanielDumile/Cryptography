import numpy as np
import math

size_alphabet = 26

def extendedEuclideanA(numberA,numberB):
	numberA = int(numberA)
	numberB = int(numberB)
	if numberB != 0:
		u0 = 1
		u1 = 0
		v0 = 0
		v1 = 1
		while numberB != 0:
			residue  = int(numberA) % int(numberB)
			quotient = (numberA - residue)/numberB
			u        = u0 - quotient * u1
			v        = v0 - quotient * v1
			numberA  = numberB
			numberB  = residue
			u0       = u1
			u1       = u
			v0       = v1
			v1       = v
		return numberA,u0,v0
	else:
		return 0,1,0

def getDeterminant(matrix):
	return round(np.linalg.det(matrix) % size_alphabet) 

def getAdjoint(matrix):
    cofactor = np.linalg.inv(matrix).T * np.linalg.det(matrix)
    aux = cofactor.transpose()
    for i in range(2):
    	for j in range(2):
    		aux[i][j] = round(aux[i][j]%size_alphabet)
    return aux

def getEuclidean(a):
	tupleValues = extendedEuclideanA(a,size_alphabet)
	return tupleValues[0],tupleValues[1]

def getMatrixInverse(matrix):
	inverse = np.array([[-1,-1,-1], [-1,-1,-1],[-1,-1,-1]])
	determinant = getDeterminant(matrix)
	gcd,multiplicativeInverse = getEuclidean(determinant)
	if gcd == 1:
		adjoint = getAdjoint(matrix)
		inverse = (multiplicativeInverse*adjoint)%size_alphabet
	return inverse

#Lo que hay que hacer es dividir el texto original en bloques de tres y sol multiplicar por la matriz inicial
def main():
	matrix = np.array([[10,5,12],[3,14,21],[8,9,11]])
	#matrix = np.array([[11,8],[3,7]])
	print(getMatrixInverse(matrix))
	#uno = np.array([9,20])
	#dot
	#res = (np.dot(uno,matrix)%size_alphabet)
	#print(res)

main()